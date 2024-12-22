import re
import os
import sys
import json
from model.model_providers import make_model, model_openai, model_wizard
from loguru import logger
from util.util import matched_data_iterator, read_file, read_freq_data

# logger.add('ner_wizard.log')

def _parse_llm_response(response: str):
    pattern = r'^(.*?)#(.*?)#(.*)$'
    return re.findall(pattern, response, re.MULTILINE)

def extract_re(context, entities, prompt_template, llm):
    # terms = set()
    # for ent in entities:
    #     ent = ent['phrase']
    #     terms.add(ent)
    # ents_str = ','.join(list(terms))
    
    # prompt = prompt_template.format_map(dict(context=context, entities=ents_str))
    prompt = prompt_template.format_map(dict(context=context))
    # logger.debug(f'prompt: {prompt}')
    
    response = llm.predict(prompt)
    logger.debug(f"LLM: {response}")
    
    return _parse_llm_response(response)

def main():
    shard_id = int(sys.argv[1])
    assert 0 <= shard_id <= 7, 'invalid args shard_id, must be in [0,7]'
    
    model_provider = model_wizard
    max_samples = 10000
    matched_path = "./data/matched_entities_result.json" # 928w
    prompt_path = "./prompts/re_en.txt"
    model_path = '/platform_tech/xiajun/PLMs/WizardLM-13B-recover' # 30B

    # shards = [
    #     ('0,1', 100000, "./result/re_results/triples_32_p1.csv"),
    #     ('2,3', 200000, "./result/re_results/triples_32_p2.csv"),
    #     ('4,5', 300000, "./result/re_results/triples_32_p3.csv"),
    #     ('6,7', 400000, "./result/re_results/triples_32_p4.csv"),
        
    #     ('0,1', 500000, "./result/re_results/triples_34_p1.csv"),
    #     ('2,3', 600000, "./result/re_results/triples_34_p2.csv"),
    #     ('4,5', 700000, "./result/re_results/triples_34_p3.csv"),
    #     ('6,7', 800000, "./result/re_results/triples_34_p4.csv")
    # ]
    shards = [
        ('0', 310000, "./result/re_results/triples_32_p1.csv"),
        ('1', 320000, "./result/re_results/triples_32_p2.csv"),
        ('2', 330000, "./result/re_results/triples_32_p3.csv"),
        ('3', 340000, "./result/re_results/triples_32_p4.csv"),
        ('4', 350000, "./result/re_results/triples_32_p5.csv"),
        ('5', 360000, "./result/re_results/triples_32_p6.csv"),
        ('6', 370000, "./result/re_results/triples_32_p7.csv"),
        ('7', 380000, "./result/re_results/triples_32_p8.csv"),
        
        # ('0', 210000, "./result/re_results/triples_34_p1.csv"),
        # ('1', 220000, "./result/re_results/triples_34_p2.csv"),
        # ('2', 230000, "./result/re_results/triples_34_p3.csv"),
        # ('3', 240000, "./result/re_results/triples_34_p4.csv"),
        # ('4', 250000, "./result/re_results/triples_34_p5.csv"),
        # ('5', 260000, "./result/re_results/triples_34_p6.csv"),
        # ('6', 270000, "./result/re_results/triples_34_p7.csv"),
        # ('7', 280000, "./result/re_results/triples_34_p8.csv"),
    ]
    
    gpus, start_id, output_path = shards[int(shard_id)]
    
    os.environ["CUDA_VISIBLE_DEVICES"] = gpus
    

    llm = make_model(model_provider, model_path)
    prompt_template = read_file(prompt_path)
    writer = open(output_path, 'a+')
    for context, entities in matched_data_iterator(matched_path, start_id=start_id, max_samples=max_samples):
        context = context if model_provider==model_openai else context[:1200]
        
        try:       
            triples = extract_re(context, entities, prompt_template, llm)
            for head, rel, tail in triples:
                if head == 'head_entity':
                    continue
                writer.write(f'{head}\t{rel}\t{tail}\n')
                writer.flush()
            
        except Exception as e:
            logger.warning(e)
    
    writer.close()
        

if __name__ == '__main__':
    main()
