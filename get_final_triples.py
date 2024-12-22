import os
import json
import re

re_result_dir = './result/re_results/'
ner_merged_result = './result/clean/cleaned_gpt_terms.json'

# 获取术语
terms = {}
with open(ner_merged_result) as r:
    terms = json.load(r)

print(list(terms.items())[:3])

# 遍历目录中的所有文件
triples = {}
cnt = 0
for filename in os.listdir(re_result_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(re_result_dir, filename)
        with open(filepath) as file:
            for line in file:
                cnt += 1
 
                ss = line.replace('\_','_').strip().split('\t')
                if len(ss) >= 3:
                    head, relation, tail = ss[-3:]
                    # print(head, relation, tail)
                    if head.lower() == tail.lower():
                        continue 
                    if head.lower() in terms and tail.lower() in terms:
                        # print('$$$$$$', line)
                        # triples.append("###".join([head, relation, tail]))
                        tstr = "###".join([head, relation, tail])
                        triples[tstr] = triples.get(tstr, 0) + 1 
                        

# print(triples)
with open('gpt_kg.csv', 'w') as w:
    w.write('head_entity\trelation\ttail_entity\n')
    for triple in triples.keys():
        head, rel, tail = triple.split('###')
        w.write(f'{head}\t{rel}\t{tail}\n')

with open('gpt_kg_core.csv', 'w') as w:
    w.write('head_entity\trelation\ttail_entity\n')
    for triple, cnt in triples.items():
        if cnt >= 5:
            head, rel, tail = triple.split('###')
            w.write(f'{head}\t{rel}\t{tail}\n')
