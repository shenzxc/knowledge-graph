import json

matched_path = "../data/matched_entities_result.json"

filtered_terms = {}

with open(matched_path) as r:
    cnt = 0
    for ln in r:
        cnt += 1
        if cnt >= 1000000: break
        d = json.loads(ln)
        for e in d['entities']:
            t = e['phrase']
            filtered_terms[t] = filtered_terms.get(t, 0) + 1
            

print('all lns ', cnt)

with open('filtered_terms_by_freq.txt', 'w') as w:
    sorted_ts = sorted(filtered_terms.items(), key=lambda x:x[1], reverse=True)
    for term, freq in sorted_ts:
        if freq/cnt >= 0.1:
            print(term)
            continue

        w.write(f'{term}##{freq/cnt}\n')
