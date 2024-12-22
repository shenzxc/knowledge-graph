from py2neo import Graph

# 连接到数据库
graph = Graph(uri="bolt://localhost:7687", auth=('neo4j', 'Idea@2022'))
res = graph.run("MATCH (n) RETURN count(n);")
print(res)
graph.run("MATCH (n) DETACH DELETE n;")
print('delete old data')
res = graph.run("MATCH (n) RETURN count(n);")
print(res)

# 导入三元组数据
with open('gpt_kg_core.csv', 'r') as r:
    for line in r:
        try:
            
            line = line.replace("\'", "\\'").replace(" ", "_").replace("-", "_")

            head_entity, relation, tail_entity = line.strip().split('\t')
            
            # 创建或获取头实体节点
            query_head = "MERGE (h:Entity {name: '" + head_entity + "'}) RETURN h;"
            print(query_head)
            head_node = graph.run(query_head).evaluate()

            # 创建或获取尾实体节点
            query_tail = "MERGE (t:Entity {name: '" + tail_entity + "'}) RETURN t;"
            print(query_tail)
            tail_node = graph.run(query_tail).evaluate()

            # 创建关系
            query_relation = "MATCH (h:Entity {name: '" + head_entity +"'}), (t:Entity {name: '" + tail_entity + "'}) \
                            MERGE (h)-[r:_"+ relation +"_]->(t) RETURN r;"
            print(query_relation)
            graph.run(query_relation)
        
        except Exception as e:
            print(e)

