from main21 import load_file, get_std_id, get_fac_json_id, to_list, get_std_json_id, write_file, get_fac_id

faculty_rank = {}

def add_score(_id, score):
    global faculty_rank
    if not faculty_rank.get(_id):
        faculty_rank[_id] = []
    faculty_rank[_id].append(score)


def get_id(fac_line):
    _major_id = fac_line.get('major_id', '0')
    _major_id = _major_id if _major_id else '0'
    return fac_line['program_id']+_major_id+fac_line.get('project_id', '')


def matching(stds, facs, join_map):
    for std in stds.values():
        for order in to_list(std['appl']):
            _id = get_std_json_id(order)
            fac = get_fac(facs[_id],facs, join_map)
            _id = get_fac_id(fac['json'])

            # if not facs.get(_id):
            #     print('not found ', _id)
            #     return False

            score = (float(order['score']),
                     order['citizen_id'], order['priority'])
            add_score(_id, score)


def reporter(std, priority, rank):
    for i in to_list(std['appl']):
        if i['priority'] == priority:
            i['ranking'] = rank
            # print(i['citizen_id'], i['ranking'])
            return True
    print('Error priority not found.', std, priority, rank)
    return False


def float_equal(a, b):
    return abs(a - b) <= 0.00001


def ranker(stds):
    for fac_id, pool in faculty_rank.items():
        pool.sort(reverse=True)
        # print(fac_id, len(pool))
        rank = 0
        pev = -1
        for score, _id, priority in pool:
            if score <= 0:
                break
            if not float_equal(score, pev):
                rank += 1
            pev = score
            reporter(stds[_id], priority, rank)
            if fac_id == '10020326620101BBC2701':
                print(score, _id, priority, rank)
        #     break
        # break

def make_join_map(facs, func_id, key, sub_key):
    join_map = {}
    for fac in facs.values():
        join_id = get_join_id(fac)
        if join_id == '0': join_id = False
        if join_id:
            _id = func_id(fac[key])
            if join_id not in join_map:
                join_map[join_id] = []
            join_map[join_id].append(_id)
    return join_map

def get_join_id(fac, key='csv', sub_key='join_id'):
    join_id = fac.get(key, {}).get(sub_key, False)
    if join_id == '0': return False
    if not join_id: return False
    return join_id

def get_fac(fac, facs, join_map , key='csv', sub_key='join_id'):
    join_id = get_join_id(fac)
    if join_id:
        return facs[join_map[join_id][0]]
    return fac


if __name__ == "__main__":
    students = {}  # student dict
    faculties = {}  # faculty dict

    std_appl_path = 'chay-out.csv'
    load_file(students, get_std_id, 'appl', std_appl_path)

    fac_json_path = 'data/tcas3-1-criterias-updated-20210513-with-projectid.json'
    load_file(faculties, get_fac_json_id, 'json', fac_json_path, 'json')

    fac_path = 'data/cupt-table-ad1.csv'
    load_file(faculties, get_fac_id, 'csv', fac_path)

    join_map = make_join_map(faculties, get_fac_id, 'csv', 'join_id')

    # print(join_map)

    # check duplicate json
    # for fac_id, fac in faculties.items():
    #     if isinstance(fac['json'], list):
    #         print(fac['json'])

    # print(faculty_join)

    matching(students, faculties, join_map)
    ranker(students)

    # print([print(i, len(faculty_rank[i])) for i in faculty_rank])

    # [print(i+1, j)
    #  for i, j in enumerate(faculty_rank['10020326620101BBC2701'])]
    write_file('chay-rank-out.csv', students)
