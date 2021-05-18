import csv
import sys

FLOAT_DELTA = 0.00001

def get_row_key(row):
    return (row['citizen_id'], int(row['priority']))

def read_output(filename):

    results = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            results[get_row_key(r)] = r

    return results

def main():
    output1_filename = sys.argv[1]
    output2_filename = sys.argv[2]

    results1 = read_output(output1_filename)
    results2 = read_output(output2_filename)

    for k in results1:
        score_comparison =  ('calculated_score' in results1[k])
        
        if k not in results2:
            print(f'Result not found (in {output2_filename}): {k}')
        else:
            if score_comparison:
                error = False
                if float(results1[k]['calculated_score']) < 0:
                    error = float(results2[k]['calculated_score']) >= 0
                else:
                    if abs(float(results1[k]['calculated_score']) - float(results2[k]['calculated_score'])) > FLOAT_DELTA:
                        error = True

                if error:
                    print(f'NEQ - {k} - {results1[k]["program_id"]} {results1[k]["major_id"]} {results1[k]["project_id"]}: {float(results1[k]["calculated_score"]):.5f} and {float(results2[k]["calculated_score"]):.5f}')
            else:
                error = False
                if int(results1[k]['ranking']) != int(results2[k]['ranking']):
                    error = True
                if abs(float(results1[k]['score']) - float(results2[k]['score'])) > FLOAT_DELTA:
                    error = True
                if error:
                    print(f'NEQ - {k} - {results1[k]["program_id"]} {results1[k]["major_id"]} {results1[k]["project_id"]}: {results1[k]["ranking"]} / {float(results1[k]["score"]):.5f} and {results2[k]["ranking"]} / {float(results2[k]["score"]):.5f}')

    for k in results2:
        if k not in results1:
            print(f'Result not found (in {output1_filename}): {k}')
    
if __name__ == '__main__':
    main()
