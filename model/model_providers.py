import sys
sys.path.append('..')
import openai, tenacity
from api_key import openai_api_base, openai_api_key, openai_api_type, openai_api_version

import torch
import transformers
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
from transformers import LlamaTokenizer, AutoModelForCausalLM, LlamaForCausalLM, GenerationConfig, AutoConfig
from loguru import logger

assert (
    "LlamaTokenizer" in transformers._import_structure["models.llama"]
), "LLaMA is now in HuggingFace's main branch.\nPlease reinstall it: pip uninstall transformers && pip install git+https://github.com/huggingface/transformers.git"



class ModelProvider:
    def predict(self, query):
        raise NotImplementedError


class OpenAIModelProvider(ModelProvider):
    
    def __init__(self, model_name_or_path) -> None:
        super().__init__()
    
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=3, max=6),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def chat(self, messages, temperature=0.7, max_tokens=4096):
        openai.api_type = openai_api_type
        openai.api_base = openai_api_base
        openai.api_version = openai_api_version
        openai.api_key = openai_api_key

        response = openai.ChatCompletion.create(
            engine="turbo-idea",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result = ''
        for choice in response.choices:
            result += choice.message.content

        return result
    
    def predict(self, query: str):
        messages = [
            {"role": "system", "content": "你是一个生物医学专家。"},
            {"role": "user", "content": query},
        ]
        
        return self.chat(messages)

class WizardLMModelProvider(ModelProvider):
    def __init__(self, model_name_or_path) -> None:
        self.tokenizer = self._load_tokenizer(model_name_or_path)
        self.model = self._load_model(model_name_or_path)
        
    def _load_model(self, model_name_or_path: str):
        logger.info(f"loading model {model_name_or_path} ...")
        config = AutoConfig.from_pretrained(model_name_or_path,
                                            trust_remote_code=True,
                                            use_auth_token=False)

        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config, trust_remote_code=True)

        model = load_checkpoint_and_dispatch(
            model, model_name_or_path, device_map="auto", no_split_module_classes=["LlamaDecoderLayer"],
            dtype=torch.float16  # torch.float32
        )
        
        # unwind broken decapoda-research config
        model.config.pad_token_id = self.tokenizer.pad_token_id = 0  # unk
        model.config.bos_token_id = 1
        model.config.eos_token_id = 2

        model.eval()
        if torch.__version__ >= "2" and sys.platform != "win32":
            model = torch.compile(model)
            
        return model
    
    def _load_tokenizer(self, model_name_or_path):
        logger.info(f"loading tokenizer {model_name_or_path} ...")
        return LlamaTokenizer.from_pretrained(model_name_or_path, use_fast=False)

        
    def predict(self, query):
        prompts = f"""A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {query} ASSISTANT:"""
        
        inputs = self.tokenizer(
                prompts, 
                return_tensors="pt",
                add_special_tokens=False,
                max_length=2048,
                truncation=True
            )
        input_ids = inputs["input_ids"].to(0)
        
        with torch.no_grad():
            kwargs = {
                'max_new_tokens': 2048,
                'min_new_tokens': 1,
                'temperature': 0.7,
                'top_p': 1.0,
                'use_cache': True,
                'num_beams': 1
            }
            generation_output = self.model.generate(
                input_ids=input_ids,
                **kwargs
            )
  
        s = generation_output[0].tolist() if type(generation_output) == torch.Tensor else generation_output.sequences[0]
        output =  self.tokenizer.decode(s, skip_special_tokens=True)

        return output.split("ASSISTANT:")[1].strip()
    
model_openai = "openai"
model_wizard = "wizard"

_PROVIDER_MAP = {
    model_openai: OpenAIModelProvider,
    model_wizard: WizardLMModelProvider
}


def make_model(provider, model_name_or_path: str=None):
    assert provider in _PROVIDER_MAP, f"No model provider '{provider}' implemented"
    return _PROVIDER_MAP[provider](model_name_or_path)

if __name__ == '__main__':
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = '0,1'
    
    model = make_model('wizard', '/platform_tech/xiajun/PLMs/WizardLM-13B-recover')
    
    query = '世界第一高峰是什么？'
    print(model.predict(query))