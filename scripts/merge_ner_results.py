import os
import json
import re

# 设置目录路径
directory = '../result'

# 存储合并结果的字典
merged_entities = {}

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath) as file:
            data = json.load(file)
            # 遍历每个文件中的实体和类型列表
            for entity, types in data.items():
                if entity in merged_entities:
                    # 合并实体的语义类型为列表
                    merged_entities[entity] = list(set(merged_entities[entity]) & set(types))
                else:
                    # 如果实体不存在于合并结果中，则将实体和类型添加到合并结果中
                    merged_entities[entity] = types

# 读取语义类型的txt文件
semantic_types_file = '../schema/semantic_types.txt'
with open(semantic_types_file) as file:
    allowed_types = {line.strip() for line in file}

# 清洗规则：去除空白实体
def remove_blank_entities(entities):
    return {entity: types for entity, types in entities.items() if entity.strip()}

# 清洗规则：去除特殊字符
def remove_special_characters(entities):
    cleaned_entities = {}
    for entity, types in entities.items():
        cleaned_entity = re.sub(r'[^a-zA-Z0-9 ]', '', entity)
        if cleaned_entity.strip():
            cleaned_entities[cleaned_entity] = types
    return cleaned_entities

# 清洗规则：大小写统一
def unify_case(entities):
    return {entity.lower(): types for entity, types in entities.items()}

# 清洗规则：去除超长实体
def remove_long_entities(entities, max_length):
    return {entity: types for entity, types in entities.items() if len(entity) <= max_length}

# 应用清洗规则
merged_entities = remove_blank_entities(merged_entities)
merged_entities = remove_special_characters(merged_entities)
merged_entities = unify_case(merged_entities)
merged_entities = remove_long_entities(merged_entities, 80) 

# 读取术语文件
terms_file = '../cleanterms6.txt'
terms = {}
with open(terms_file) as file:
    lines = file.readlines()
    header = lines[0].split('\t')
    for line in lines[1:]:
        values = line.split('\t')
        term = values[header.index('str.lower')]
        types = [values[header.index('sty')]]
        if term in merged_entities:
            merged_entities[term] += types
        else:
            merged_entities[term] = types

# 过滤合并结果中的语义类型不在允许范围内的实体。 cleanterms的语义类型和UMLS原始类型不一致
#filtered_entities = {}
#for entity, types in merged_entities.items():
#    filtered_types = list(set([t for t in types if t in allowed_types]))
#    if filtered_types:
#        filtered_entities[entity] = filtered_types

filtered_entities = {}
for entity, types in merged_entities.items():
    filtered_types = list(set(types))
    if filtered_types:
        filtered_entities[entity] = filtered_types


# 将过滤后的结果写入文件
output_file = '../result/merged_filtered_entities.json'
with open(output_file, 'w') as file:
    json.dump(filtered_entities, file, indent=2)

print("过滤后的结果已保存到", output_file)
print(len(filtered_entities))
