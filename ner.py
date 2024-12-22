import re
import os
import json
from model.model_providers import make_model, model_openai, model_wizard
from loguru import logger
from util.util import read_cached_id, save_cached_id, read_file

logger.add('ner_wizard.log')

def pmc_data_iterator(
        pmc_path: str, 
        start_id: int, 
        max_samples: int=1000000, 
        use_cache_id: bool=False
    ):
    
    samples = []
    if use_cache_id:
        start_id = read_cached_id()
    logger.info(f'iterating from {start_id}')
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
                            # if idx % 10 == 0:
                            #     logger.info(f'saving cache id {idx}')
                            #     save_cached_id(idx)
                        
                        idx += 1
                        
                continue
            
            if ln.startswith("PMID"):
                continue
            
            samples.append(ln.strip())

def _parse_llm_response(response: str):
    json_text = re.search(r'{.*}', response, re.DOTALL).group(0)
    return json.loads(json_text)

def ner(context, prompt_template, llm):
    prompt = prompt_template.format_map(dict(context=context))
    # logger.debug(f'prompt: {prompt}')
    
    response = llm.predict(prompt)
    logger.debug(f"LLM: {response}")
    
    return _parse_llm_response(response)

def save(entity_list: list, output_path: str):
    entity_sty_dict = {}
    try:
        with open(output_path, 'r') as r:
            entity_sty_dict = json.load(r)
    except Exception as e:
        logger.error(e)
    
    if not entity_sty_dict:
        entity_sty_dict = {}

    for ets_dict in entity_list:
        for entity, sty in ets_dict.items():
            entity_sty_dict.setdefault(entity, []).append(sty)
    
    for k, v in entity_sty_dict.items():
        entity_sty_dict[k] = list(set(v))
    
    if isinstance(entity_sty_dict, dict):    
        with open(output_path, 'w') as w:
            json.dump(entity_sty_dict, w, ensure_ascii=False, indent=2)

def main():
    # model_provider = model_openai
    # max_samples = 50000
    
    # gpus, start_id, output_path ='', 20, "./result/biomed_kg_entities_openai.json"
    
    model_provider = model_wizard
    max_samples = 1000000
    
    # 注意 32, 34配置反了
    # gpus, start_id, output_path ='0,1', 1000500, "./result/biomed_kg_entities_32_wizard_p1.json"
    # gpus, start_id, output_path ='2,3', 2002500, "./result/biomed_kg_entities_32_wizard_p2.json"
    # gpus, start_id, output_path ='4,5', 3002500, "./result/biomed_kg_entities_32_wizard_p3.json"
    # gpus, start_id, output_path ='6,7', 4001000, "./result/biomed_kg_entities_32_wizard_p4.json"
    
    # gpus, start_id, output_path ='0,1', 5000000, "./result/biomed_kg_entities_34_wizard_p1.json"
    # gpus, start_id, output_path ='2,3', 6002000, "./result/biomed_kg_entities_34_wizard_p2.json"
    gpus, start_id, output_path ='4,5', 7010000, "./result/biomed_kg_entities_34_wizard_p3.json"
    # gpus, start_id, output_path ='6,7', 2000, "./result/biomed_kg_entities_34_wizard_p4.json"
    
    os.environ["CUDA_VISIBLE_DEVICES"] = gpus
    
    pmc_path = "./data/random_pmc_oa_2000w.txt"
    prompt_path = "./prompts/ner_en.txt"
    model_path = '/platform_tech/xiajun/PLMs/WizardLM-30B-recover'

    llm = make_model(model_provider, model_path)
    
    prompt_template = read_file(prompt_path)
    
    entities = []
    for context in pmc_data_iterator(pmc_path, start_id=start_id, max_samples=max_samples):
        context = context if model_provider==model_openai else context[:800]
        
        if len(entities) == 10:
            logger.info(f"updating ner results ...")
            try:
                save(entities, output_path)
            except:
                pass
            entities.clear()
        
        try:       
            ets_dict = ner(context, prompt_template, llm)
            if ets_dict:
                entities.append(ets_dict)      
        except Exception as e:
            logger.warning(e)
        
        

if __name__ == '__main__':
    main()
