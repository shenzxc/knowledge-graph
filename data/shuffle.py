import random
random.seed(1)

samples = []

with open('pubmed_abstract_title.txt', 'r') as r:
    one_samples = []
    for ln in r:
        
        # 总计34268951篇
        if ln.startswith("/raid/tanwei/data/pubmed"):
            if len(one_samples):
                context = ''.join(one_samples)
                samples.append(context)
                one_samples.clear()
        
        one_samples.append(ln)

random.shuffle(samples)

with open('random_pmc_oa_2000w.txt', 'w') as w:
    for ln in random.sample(samples, 20000000):
        w.write(ln)
              
with open('random_pmc_oa_10w.txt', 'w') as w:
    for ln in random.sample(samples, 100000):
        w.write(ln)