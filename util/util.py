import os
import json

cache_file = '.cache'

def read_cached_id():
    if os.path.exists(cache_file) is False:
        return 0
    
    with open(cache_file, 'r') as r:
        return int(r.read())

def save_cached_id(id):
    id = str(id)
    if id.isdigit() is False:
        raise f'invalid id {id}'
    
    with open(cache_file, 'w') as w:
        w.write(id)
           
def read_file(path):
    with open(path, 'r') as r:
        return r.read()
    
def get_terms_from_json(path):
    with open(path) as r:
        return json.load(r)

def read_freq_data(path):
    d = {}
    with open(path) as r:
        for ln in r:
            t, ratio = ln.split('##')
            d[t] = float(ratio)
            
    return d

def matched_data_iterator(matched_path, start_id=0, max_samples=10000000):
    with open(matched_path)  as r:
        idx = 0
        for ln in r:
            if (idx - start_id) >= max_samples: break
            if not ln: continue
            if idx >= start_id:
                data = json.loads(ln)
                context = data['text']
                entities = data['entities']
                yield context, entities
                
            idx += 1
            

def pmc_data_iterator(pmc_path, start_id=0, max_samples=100000000):
    samples = []
    with open(pmc_path, 'r') as r:
        idx = 0
        for ln in r:
            if (idx - start_id) >= max_samples: break
            if not ln: continue
            if ln.startswith("/raid/tanwei/data/pubmed"):
                if len(samples):
                    context = '\n'.join(samples)
                    if len(context.split()) > 100:
                        samples.clear()
                        
                        if idx >= start_id:
                            yield context

                        idx += 1
                        
                continue
            
            if ln.startswith("PMID"):
                continue
            
            samples.append(ln.strip())