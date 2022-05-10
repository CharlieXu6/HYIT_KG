#coding=utf8
import sys
import re
from py2neo import Graph
import json

graph = Graph("bolt://localhost:7687/browser/", username="neo4j", password="12345678")


def query(name):
    # data = graph.run( "match(n:People{name:'%s'})-[r]->(m) return n.name, r, m limit 50\
    #     Union all\
    #     match(n)-[r]->(m:People{name:'%s'}) return n,r,m.name limit 50" % (name, name))
    # data=match(n:People{name:'银角大王'})-[r]->(n1) return n
    data = graph.run("match(n:实体{name:'%s'})-[r]->(n1) return n1.value,n1.name,r" % (name))
    # data = graph.run("match(p:People {name:'%s'})-[r:`%s`]->(n) return n.value" % (entity, attr))

    data = list(data)
    # print(data)
    data_list = []
    triple_list = []
    for temp in data:

        # print('temp')
        print(temp)
        '''
        需正则的是28行 temp=
        需改成的格式为  xxxx：xxxx：xxxx
        '''
        temp = str(temp).replace("、", "")
        reg1 = re.compile(r'value=(.*?)n1.name=')
        reg11 = re.compile(r'n1.name=(.*?)r')
        reg2 = re.compile(r'r=\((.+?)\)')
        reg3 = re.compile(r':([\u4e00-\u9fa5]*?)[\s]{')

        name1 = re.findall(reg1, str(temp))
        name3 = re.findall(reg11, str(temp))
        print(name3)
        # print('reg1')
        # print(reg1)
        # print('name1')
        # print(name1)
        # name2 = re.findall(reg11, str(temp))
        # r1 = re.findall(reg2, str(temp))
        # r2 = re.findall(reg3, str(temp))
        # print(r1)
        # print(r2)
        if name1 == ['None ']:
            # print('{}:{}:{}'.format(name1[0], r1[0], r2[0]))
            print(name3)
            r1 = re.findall(reg2, str(temp))
            r2 = re.findall(reg3, str(temp))
            temp = r1[0] + ':' + r2[0] + ':' + name3[0]
            # temp.replace("'", "")
            # print(temp)

        else:

            # print('name2')
            # print(name2)
            # print('{}:{}:{}'.format(name2[0],r1[0],r2[0]))
            # name2 = re.findall(reg1, str(temp))
            # print(name2)
            r1 = re.findall(reg2, str(temp))
            r2 = re.findall(reg3, str(temp))
            temp = r1[0] + ':' + r2[0] + ':' + name1[0]

        print(temp)
        # temp = str(temp).replace("Record r=(", "").replace(")-[", "").replace(" {}]->(", ":").replace(")>", "").replace("<", "")
        # print(temp)
        triple_list.append(temp)
        temp = temp.split(":")
        temp_result = dict()
        temp_result['name'] = temp[0]
        # print(temp_result)
        # data_list.append({'name': temp[0]})
        # data_list.append({'name': temp[2]})
        if not data_list.__contains__({'name': temp[0]}):
            data_list.append({'name': temp[0]})

        # temp_result['name'] = temp[2]
        if not data_list.__contains__({'name': temp[2]}):
            data_list.append({'name': temp[2]})
    print(data_list)
    links = []
    for triple in triple_list:
        temp_triple = triple.split(":")
        source = temp_triple[0]
        target = temp_triple[2]
        source_id = data_list.index({'name':source})
        target_id = data_list.index({'name':target})
        value = temp_triple[1]
        result = {'source': source_id, 'target': target_id, 'value': value}
        links.append(result)
    json_data = {'data': data_list, 'links': links}
    # print(json.loads(json_data))
    return json_data
    # return json_data(ensure_ascii=False)

    # print(data)
    # return get_json_data(data)


def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.label_zh']+"_")
        d.append(i['n.label_zh']+"_")
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        #data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        #string=str(i['r'])
        #p = re.compile(".*?:`(.*?)`]->.*?", re.S)
        #result = re.findall(p, string)
        link_item = {}

        link_item['source'] = name_dict[i['p.label_zh']]

        link_item['target'] = name_dict[i['n.label_zh']]
        link_item['value'] = i['r.label_zh']
        json_data['links'].append(link_item)
    return json_data
    # return json_data( ensure_ascii=False)
