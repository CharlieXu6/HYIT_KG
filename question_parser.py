# coding:utf-8
import question_classify as qc
from py2neo import Graph

graph = Graph("bolt://localhost:7687/browser/", username="neo4j", password="12345678")

def get_answer(question):
    name_list, att_list = qc.entity_att_extract(question)
    if name_list.__len__() > 0 and att_list.__len__() > 0:
        entity = name_list[0]
        attr = att_list[0]
        data = graph.run("match(p:实体 {name:'%s'})-[r:`%s`]->(n) return n.value " % (entity, attr))
        data = list(data)





        if data.__len__() == 0:
            return "我暂时回答不了这个问题！"
        for temp in data:
            result = str(temp).replace("<Record n.value=", "").replace(">", "")
            print(result)
            return result

    else:
        return "我暂时回答不了这个问题！"
        # print(data)

# if __name__ == '__main__':
#     get_answer("唐三藏的别称是什么")

