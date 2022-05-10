# coding:utf-8
import xlwt
import xlrd
from py2neo import Graph, Node, Relationship
import os

##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('bolt://localhost:7687', username='neo4j', password='12345678')
full_path = ''
for lists in os.listdir('./upload'):
    full_path = os.path.join('./upload', lists)
book = xlrd.open_workbook(full_path)
workSheetName = book.sheet_names()
print("Excel文件包含的表单有："+str(workSheetName))

# 根据指定的表单名,一行一行获取指定表单中的所有数据，表单名为worksheetname
def build_nodes(worksheetname):
    graph.delete_all()
    bridgeStructure = book.sheet_by_name(worksheetname)
    AllsheetValue = []

    all_properties_pairs = []
    for i in range(bridgeStructure.nrows):
        each_entity_property = []
        each_row = []
        if i == 0:
            continue
        property_pair = []
        for j in range(bridgeStructure.ncols):
            each_row.append(bridgeStructure.cell_value(i,j))
            if j > 3:
                if j % 2 == 0:
                    property_pair.append(bridgeStructure.cell_value(i, j))
                else:
                    property_pair.append(bridgeStructure.cell_value(i, j))
                    each_entity_property.append(property_pair)
                    property_pair = []
        all_properties_pairs.append(each_entity_property)
        id_node = Node("实体", name=each_row[1], entity_id=each_row[0], label=each_row[2])
        graph.create(id_node)
        # print(AllsheetValue)
        for pro in each_entity_property:
            property_name = pro[0]
            property_value = pro[1]
            if str(property_name).strip().__len__() > 0 and str(property_value).strip().__len__() > 0:
                temp_node = Node("property", value=property_value)
                graph.create(temp_node)
                node_relation = Relationship(id_node, property_name, temp_node)
                graph.create(node_relation)
                print(property_name)
        AllsheetValue.append(each_row)
    return AllsheetValue

# 再建立实体节点之间的关系
def build_entity_relationship(worksheetname):
    bridgeStructure = book.sheet_by_name(worksheetname)
    for i in range(bridgeStructure.nrows):
        each_row = []
        if i == 0:
            continue
        for j in range(bridgeStructure.ncols):
            each_row.append(bridgeStructure.cell_value(i, j))
        source_id = each_row[1]
        target_id = each_row[2]
        graph.run("match(a:%s),(b:%s) where a.entity_id='%s' and b.entity_id='%s' CREATE (a)-[r:%s]->(b)" % ("实体", "实体", str(source_id), str(target_id), str(each_row[0])))
        print(each_row)

def get_dict():
    entity = []
    attribute_names = []
    bridgeStructure = book.sheet_by_name('Vertexes')
    AllsheetValue = []
    all_properties_pairs = []
    for i in range(bridgeStructure.nrows):
        each_entity_property = []
        each_row = []
        if i == 0:
            continue
        property_pair = []
        for j in range(bridgeStructure.ncols):
            each_row.append(bridgeStructure.cell_value(i,j))
            if j > 3:
                if j % 2 == 0:
                    property_pair.append(bridgeStructure.cell_value(i, j))
                else:
                    property_pair.append(bridgeStructure.cell_value(i, j))
                    each_entity_property.append(property_pair)
                    property_pair = []
        all_properties_pairs.append(each_entity_property)
        if entity.__contains__(each_row[1]):
            continue
        else:
            entity.append(each_row[1])
        for pro in each_entity_property:
            property_name = pro[0]
            property_value = pro[1]
            if str(property_name).strip().__len__() > 0 and str(property_value).strip().__len__() > 0:
                if attribute_names.__contains__(property_name):
                    continue
                else:
                    attribute_names.append(property_name)
    return entity, attribute_names

# if __name__ == '__main__':
#     entity, attribute_names = get_dict()
#     print(entity)
#     print(attribute_names)


