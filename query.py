# #coding:utf-8
# from py2neo import Graph, Node, Relationship, NodeMatcher
#
#
# class Query:
#     def __init__(self):
#         self.graph = Graph("bolt://localhost:7687/browser/", username="neo4j", password="12345678")
#
#     def run(self, cql):
#         result = []
#         find_rela = self.graph.run(cql)
#         print(find_rela)
#         for i in find_rela:
#             result.append(i.items()[0][1])
#         print(len(result))
#         return result
#
