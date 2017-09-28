#!/usr/bin/env python3

import csv
import os

from collections import defaultdict


base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, 'assets')

pool_file = os.path.join(assets_dir, 'general_class_question_pool.txt')
pool_index_file = os.path.join(assets_dir, 'general_class_question_pool_index.txt')
pool_csv = os.path.join(assets_dir, 'pool.csv')

pool_index = defaultdict(lambda: {
    'title': None,
    'id': None,
    'exam_questions': 0,
    'exam_groups': 0,
    'total_questions': 0,
    'index': defaultdict(str),
})

find = lambda lst, word: min(i for i, sentence in enumerate(lst) if word in sentence)

with open(pool_index_file, 'r') as f:
    for line in f:
        l_stripped = line.rstrip()
        l_split = l_stripped.split(' ')

        if l_split[0] == 'SUBELEMENT':
            l_split.pop(0)
            id = l_split[0]
            l_split.pop(0)

            lb_pos = find(l_split, '[')
            rb_pos = find(l_split, ']')

            l_split[lb_pos] = l_split[lb_pos].replace('[', '')
            l_split[rb_pos] = l_split[rb_pos].replace(']', '')
            qs_and_grps = (' '.join(l_split[lb_pos:rb_pos+1])).split('-')

            title = ' '.join(l_split[0:lb_pos])
            exam_questions = int((qs_and_grps[0].split(' '))[0])
            grp_questions = int((qs_and_grps[1].split(' '))[0])
            total_questions = int(l_split[rb_pos+1])

            pool_index[id]['id'] = id
            pool_index[id]['title'] = title
            pool_index[id]['exam_questions'] = exam_questions
            pool_index[id]['exam_groups'] = grp_questions
            pool_index[id]['total_questions'] = total_questions

        else:
            section_id = line[0:2]
            id = line[2:3]
            title = (line.split('-'))[1].strip()
            pool_index[section_id]['index'][id] = title

with open(pool_file, 'r') as f:
    for line in f:
        pass

with open(pool_csv, 'w') as f:
    output = csv.writer(f)
    for sid, sec in pool_index.items():
        output.writerow(['group', sid, sec['title'], sec['exam_questions'], sec['exam_groups'], sec['total_questions']])
        for qid, title in sec['index'].items():
            output.writerow(['subgroup', sid, qid, title])
