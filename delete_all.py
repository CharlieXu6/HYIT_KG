from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
graph.delete_all()