# KG-By-GPT

## Usage

### Requirements

运行环境： pip install requrements.txt

PubMed文本:  链接: https://pan.baidu.com/s/1MKXlxmRvevkRmCTJuXD-0Q 提取码: 34a2

WizardLM: [Wizard模型下载](https://huggingface.co/WizardL) & 合并权重

### NER

`CUDA_VISIBLE_DEVICES=0,1 python ner.py`

### RE

TODO

## How to build BioMed KnowledgeGraph?

### Step1: Define Schema

* entity semantic type: use [UMLS](https://www.nlm.nih.gov/research/umls/index.html) semantic type
* relationship type: *TODO*

### Step2: Entity Extraction (NER)

We use Large Language Model as engine to extract biomed entities.

### Step3: Relation Extraction (RE)

TODO 


## What is WizardLM?

see [Wizard](https://github.com/nlpxucan/WizardLM)
