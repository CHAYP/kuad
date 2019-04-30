#!/usr/bin/env python3

import sys
import os
import glob

FLOAT_DELTA = 0.000001

# change this to whare you keep the data files
RAW_SCORE_GLOB = '/home/neizod/git/kuad-d60/ano-dist/[gu]*.csv'

def read_raw_scores():
    raw_scores = {}
    for filename in glob.glob(RAW_SCORE_GLOB):
        lines = open(filename).readlines()
        for l in lines:
            items = l.strip().split(',')
            if len(items)<=1:
                continue

            if items[0] not in raw_scores:
                raw_scores[items[0]] = []

            raw_scores[items[0]].append((os.path.basename(filename) + ':' + l).strip())

    return raw_scores
    
def read_scores(filename):
    scores = {}
    lines = open(filename).readlines()
    for l in lines:
        items = l.strip().split(',')
        if len(items) < 2:
            continue

        nat_id = items[0]
        sub_type = int(items[1])
        major_count = int(items[2])

        app_scores = []
        for l in range(major_count):
            app_scores.append((int(items[3+l*2]), float(items[4+l*2])))

        if major_count > 1 and sub_type != 1:
            print('Subtype error', nat_id)
        scores[nat_id] = app_scores

    return scores


def check_app_scores(national_id, app_scores1, app_scores2, raw_scores):
    if len(app_scores1) != len(app_scores2):
        print(national_id,'major pref size mismatch:',len(app_scores1),' and ',len(app_scores2))
        return

    has_error = False
    for i in range(len(app_scores1)):
        if app_scores1[i][0] != app_scores2[i][0]:
            has_error = True
            print(national_id,'major pref mismatch')
            continue
        if (((app_scores1[i][1] < 0) and (app_scores2[i][1] >= 0)) or
            ((app_scores2[i][1] < 0) and (app_scores1[i][1] >= 0)) or
            ((app_scores1[i][1] >= 0) and (app_scores2[i][1] >=0) and (abs(app_scores1[i][1] - app_scores2[i][1]) > FLOAT_DELTA))):
            has_error = True
            print(national_id,'score error for',app_scores1[i][0],':',
                  app_scores1[i][1],'and',app_scores2[i][1])
    if has_error:
        print('\n'.join(raw_scores[national_id]))
        print('---------------------------------')
        
def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    scores1 = read_scores(filename1)
    scores2 = read_scores(filename2)

    raw_scores = read_raw_scores()

    for nat_id in scores1.keys():
        if nat_id not in scores2:
            print(nat_id,'not found in',filename2)
            continue

        check_app_scores(nat_id, scores1[nat_id], scores2[nat_id], raw_scores)

    for nat_id in scores2.keys():
        if nat_id not in scores1:
            print(nat_id,'not found in',filename2)
            continue

        
if __name__=='__main__':
    main()

