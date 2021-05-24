import csv
import json


def load_file(source, func_id, key, path, type='csv'):
    with open(f"{path}", "r", encoding="utf-8-sig") as mfile:
        reader = False
        if type == 'csv':
            reader = csv.DictReader
        if type == 'json':
            reader = json.load
        data_file = reader(mfile)

        for line in data_file:
            _id = func_id(line)
            # _key = line[key]
            _key = key

            if not source.get(_id):
                source[_id] = {}

            if source[_id].get(_key):
                if not isinstance(source[_id][_key], list):
                    source[_id][_key] = [source[_id][_key]]
                source[_id][_key].append(line)
            else:
                source[_id][_key] = line


def get_std_id(std_line):
    return std_line['citizen_id']


def get_fac_id(fac_line):
    return fac_line['program_id']+fac_line['major_id']+fac_line['project_id']


def get_std_json_id(fac_line):
    _major_id = fac_line.get('major_id', '0')
    _major_id = _major_id if _major_id else '0'
    return fac_line['program_id']+_major_id+fac_line.get('project_id', '')


def get_fac_json_id(fac_line):
    _major_id = fac_line.get('major_id', '0')
    _major_id = _major_id if _major_id else '0'
    return fac_line['program_code']+_major_id+fac_line.get('project_id', '')


def to_list(item):
    if not isinstance(item, list):
        return [item]
    return item


def print_std(std):
    print('-------------------- appl --------------------')
    print(std['appl'])
    print('-------------------- gatpat --------------------')
    print(std['gatpat'])
    print('-------------------- udat --------------------')
    print(std['udat'])
    print('-------------------- onet --------------------')
    print(std['onet'])
    print('-------------------- extra --------------------')
    print(std['extra'])


def get_std_val(std, key, sub_key):
    if key not in std: return 0
    return float(std[key].get(sub_key, no_score))


def get_max_of(std, key, sub_key):
    if key not in std: return 0
    score = no_score
    for i in to_list(std[key]):
        score = max(score, float(i.get(sub_key, no_score)))
    return score


def get_score(std, subj):
    subj = subj.lower()
    if subj == 'gpax':
        return get_std_val(std, 'extra', 'gpax6_score')/4
    if subj == 'max(gpax,gpax5)':
        return max(
            get_std_val(std, 'extra', 'gpax6_score'),
            get_std_val(std, 'extra', 'gpax5_score')
        )/4
    if subj == 'pat_7':
        max_score = no_score
        for s in pat7_key:
            max_score = max(max_score, get_max_of(std, 'gatpat', s))
        return max_score/300
    if subj.startswith('pat_'):
        _key = subj[4:]
        return get_max_of(std, 'gatpat', f'pat{_key}')/300
    if subj == 'gat':
        return get_max_of(std, 'gatpat', 'gat')/300
    if subj.startswith('gat_'):
        _key = subj[4:]
        return get_max_of(std, 'gatpat', subj)/150
    if subj.startswith('vnet_'):
        return get_std_val(std, 'extra', subj)/100
    if subj.startswith('udat_') and len(subj) == 7:
        _key = subj[5:]
        return get_std_val(std, 'udat', f'u{_key}')/100
    if subj == 'onet_tha':
        return get_std_val(std, 'onet', onet_key[0])/100
    if subj == 'onet_soc':
        return get_std_val(std, 'onet', onet_key[1])/100
    if subj == 'onet_eng':
        return get_std_val(std, 'onet', onet_key[2])/100
    if subj == 'onet_mat':
        return get_std_val(std, 'onet', onet_key[3])/100
    if subj == 'onet_sci':
        return get_std_val(std, 'onet', onet_key[4])/100
    if subj == 'onet':
        return sum(get_std_val(std, 'onet', i) for i in onet_key)/500
    if subj == 'max(udat_39,udat_89)':
        return max(
            get_std_val(std, 'udat', 'u39'),
            get_std_val(std, 'udat', 'u89')
        )/100
    if subj == 'max(pat_7_1,pat_7_2,pat_7_3,pat_7_4,pat_7_7)':  # lazy code
        max_score = no_score
        for s in pat7_key[:4]+[pat7_key[-1]]:
            max_score = max(max_score, get_max_of(std, 'gatpat', s))
        return max_score/300
    if subj == 'max(pat_7_1,pat_7_2,pat_7_3,pat_7_4,pat_7_5,pat_7_6,pat_7_7)':  # lazy code
        max_score = no_score
        for s in pat7_key:
            max_score = max(max_score, get_max_of(std, 'gatpat', s))
        return max_score/300

    print('caution!!!', subj)
    if not score_map.get(subj):
        score_map[subj] = 0
    score_map[subj] += 1
    return -1

def filter_score(std, fac, req):
    for subj in req:
        # exclude additional_condition
        if subj == 'additional_condition': continue



def calculate_score(std, fac):
    print(std)
    scale = 10000
    score_sum = 0
    sum_ratio = 0
    for criteria in fac['json']['scoring_score_criteria']:
        subj = criteria[0]
        ratio = criteria[1]
        score = get_score(std, subj)
        print(subj, ratio, score, score*(ratio))
        score_sum += score*(ratio)
        sum_ratio += (ratio)
    print(score_sum)
    score_sum = score_sum/sum_ratio*scale
    print(score_sum)
    return score_sum


def matching(stds, facs):
    for std in stds.values():
        for order in to_list(std['appl']):
            _id = get_std_json_id(order)
            if not facs.get(_id):
                print('not found ', _id)
                return False

            # filter(std, fac[_id])
            score = calculate_score(std, facs[_id])
            if spacial_case.get(_id):
                score = score if score > spacial_case[_id]*10000 else 0
            # order['calculated_score'] = score
            order['score'] = score


def write_file(file_name, stds):
    first = True
    with open(file_name, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow(std_appl_header)
        for std in stds.values():
            for line in to_list(std['appl']):
                if first:
                    first = False
                    csvwriter.writerow(line.keys())
                csvwriter.writerow(line.values())


if __name__ == '__main__':
    onet_key = ['x01', 'x02', 'x03', 'x04', 'x05']
    pat7_key = ['pat7_1', 'pat7_2', 'pat7_3',
                'pat7_4', 'pat7_5', 'pat7_6', 'pat7_7']
    udat_key = ['u09','u19','u29','u39','u49','u59','u69','u89','u99']

    students = {}  # student dict
    faculties = {}  # faculty dict

    no_score = 0

    std_appl_path = 'data/002-export-student-update-02-2021-5-18-randomized.csv'
    # std_appl_path = 'data/002-export-student-2021-5-16-randomized.csv'
    std_gatpat_path = 'data/scores-gatpat.csv'
    std_udat_path = 'data/scores-udat.csv'
    std_extra_path = 'data/scores-extra.csv'
    std_onet_path = 'data/scores-o-net.csv'

    # fac_path = 'data/cupt-table-ad1.csv'
    fac_json_path = 'data/tcas3-1-criterias-updated-20210513-with-projectid.json'

    load_file(students, get_std_id, 'appl', std_appl_path)
    load_file(students, get_std_id, 'gatpat', std_gatpat_path)
    load_file(students, get_std_id, 'udat', std_udat_path)
    load_file(students, get_std_id, 'extra', std_extra_path)
    load_file(students, get_std_id, 'onet', std_onet_path)

    # load_file(faculties, get_fac_id, 'csv', fac_path)
    load_file(faculties, get_fac_json_id, 'json', fac_json_path, 'json')

    score_map = {}

    # filter by sum score
    spacial_case = {
        '10020110501101E0C2700': 147/500,
        '10020110501102A0C2700': 140/500,
        '10020110501103A0C2700': 140/500,
        '10020110501104A0C2700': 145/500,
        '10020110501105A0C2700': 150/500,
        '10020110501105B0C2700': 120/500,
        '10020110501106A0C2700': 187/500,
        '10020110501106B0C2700': 147/500,
    }
    
    filter_case = {
        '10020104210601A0C2700': ['sum_udat_0,9', 220],
        '10020430210401A0C2700': [['u29','u39','u59','u69'], 50],
        '10020430300701A0C2700': ['sum_udat_2:5', 50],
        '10020430302101A0C2700': ['sum_udat_2:5', 50],
        '10020430301601A0C2700': ['sum_udat_2:5', 50],
        '10020430220201A0C2700': ['sum_udat_2:4', 50],
        '10020430300501A0C2700': ['sum_udat_2:5', 50],
        '10020430302801A0C2700': ['sum_udat_2:5', 50],
        '10020430303501A0C2700': ['sum_udat_2:5', 50]
    }

    # matching(students, faculties)

    # for i, j in score_map.items():
    #     print(i, j)

    # debug print
    # calculate_score(students['9611128787759'],
    #                 faculties['10020107611101D0C2700'])
    # print(faculties['10020107611101D0C2700'])
    calculate_score(students['9999999999901'],
                    faculties['10020104213301A0C2700'])
    # print(faculties['10020110501106A0C2700'])

    # write_file('chay-out.csv', students)
