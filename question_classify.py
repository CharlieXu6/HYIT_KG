# coding:utf-8

import excel2neo4j
import ahocorasick

#coding:utf-8
import ahocorasick

def make_AC(AC, word_set):
    for word in word_set:
        AC.add_word(word,word)
    return AC

def entity_att_extract(question):
    '''
    ahocosick：自动机的意思
    可实现自动批量匹配字符串的作用，即可一次返回该条字符串中命中的所有关键词
    '''
    entity_list, property_names = excel2neo4j.get_dict()
    print(property_names)
    AC_KEY = ahocorasick.Automaton()
    AC_KEY = make_AC(AC_KEY, set(entity_list))
    AC_KEY.make_automaton()
    name_list = set()
    for item in AC_KEY.iter(question):
        name_list.add(item[1])
    name_list = list(name_list)
    print(name_list)
    ATT_KEY = ahocorasick.Automaton()
    ATT_KEY = make_AC(ATT_KEY, set(property_names))
    ATT_KEY.make_automaton()
    att_list = set()
    for item in ATT_KEY.iter(question):
        att_list.add(item[1])
    att_list = list(att_list)
    print(att_list)
    return name_list, att_list

def classify(question):
    name_list, att_list = entity_att_extract(question)
    if name_list.__len__() > 0 and att_list.__len__() > 0:
        return "ok"
    else:
        return "error"

# if __name__ == "__main__":
#     question = '唐三藏的别称是什么'
#     classify(question)



