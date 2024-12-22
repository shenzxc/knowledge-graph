import sys
sys.path.append('..')
from util.util import get_terms_from_json
import json

bios_term_path = '../data/bios_v2.2_release/CoreData/ConceptTerms.txt'
gpt_term_path = '../result/merged_filtered_entities.json'
cleanterms_path = '../cleanterms6.txt'

gpt_terms = get_terms_from_json(gpt_term_path)
ct6_terms = set()
bios_terms = set()

# ct6
with open(cleanterms_path) as file:
    lines = file.readlines()
    header = lines[0].split('\t')
    for line in lines[1:]:
        values = line.split('\t')
        term = values[header.index('str.lower')]
        ct6_terms.add(term)

# bios
with open(bios_term_path) as r:
    for ln in r:
        term = ln.split('|')[2]
        bios_terms.add(term)

cleaned_gpt_terms = {}
for term, stys in gpt_terms.items():
    if term in ct6_terms or term in bios_terms:
        cleaned_gpt_terms.setdefault(term, stys)

print('raw gpt terms cnt ', len(gpt_terms))
print('ct6 terms cnt ', len(ct6_terms))
print('bios terms cnt ', len(bios_terms))
print('cleaned terms cnt ', len(cleaned_gpt_terms))
with open('../result/clean/cleaned_gpt_terms.json', 'w') as w:
    w.write(json.dumps(cleaned_gpt_terms, ensure_ascii=False, indent=2))