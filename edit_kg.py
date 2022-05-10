#coding:utf-8
from py2neo import Graph, Node

graph = Graph("http://localhost:7474/browser/", username="neo4j", password="12345678")


def addnode(name):
    data1 = graph.run("MATCH (e:entity {label_zh:'%s'}) RETURN e" % name).data()
    if len(data1) == 0:
        # 数据库中不存在该实体，添加实体
        n = Node('entity', label_zh=name)
        graph.create(n)


def delnode(name):
    graph.run("MATCH (r{label_zh:'%s'}) DETACH DELETE r" % name)


def addpro(name, data):
    graph.run("match (n{label_zh:'%s'}) set n.%s = '%s' return n" % (name, data['name'], data['pro']))


def delpro(label_zh, name):
    graph.run("match (n{label_zh:'%s'}) remove n.%s return n" % (label_zh, name))


def modpro(name, datas):
    for i in datas:
        graph.run("match (n{label_zh:'%s'}) set n.%s = '%s' return n" % (name, i, datas[i]))


def searchentity(name):
    json_data = {'data': [], "result": []}
    data1 = graph.run("MATCH (e:People {name:'%s'}) RETURN e" % name).data()
    if len(data1) == 0:
        return data1
    data = graph.run("MATCH (e:People {name:'%s'}) RETURN e" % name).data()[0]['e']
    # print(data,type(data))
    data = list(data)
    for i in data:
        json_data['data'].append(i)
    # result = []
    for i in data:
        i_result = graph.run("match (n:People{name:'%s'}) RETURN n.%s as pro" % (name, i)).data()[0]['pro']
        json_data['result'].append(i_result)
    return json_data


def addrelation(head_name, end_name, relation_name):
    graph.run(
        "MATCH (m:entity),(n:entity) where m.label_zh='%s'and n.label_zh='%s' CREATE (m)-[r:relation{label_zh:'%s'}]->(n)" % (
        head_name, end_name, relation_name))


def delrelation(head_name, end_name):
    graph.run(
        "MATCH (m:entity{label_zh:'%s'})-[r:relation]->(n:entity{label_zh:'%s'}) DELETE r" % (head_name, end_name))
