from py2neo import Graph
import re
import json
graph = Graph("bolt://localhost:7687/browser/", username="neo4j", password="12345678")
data = graph.run("match(n:实体{name:'银角大王'})-[r]->(n1) return n1.value,n1.name,r" )

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
    if name1==['None ']:
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


