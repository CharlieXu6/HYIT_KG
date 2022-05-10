#coding:utf-8
from flask import Blueprint

import ast
from flask import Flask, render_template, request, jsonify, session
from inquire_kg import query
from edit_kg import addnode, searchentity, addrelation, delrelation, delnode, addpro, delpro, modpro

managekg = Blueprint('managekg', __name__)


@managekg.before_request
def before():
    if session.get('is_login') == 'true':
        pass
    else:
        return render_template('login.html')


@managekg.route('/admsearch', methods=['GET', 'POST'])
def admsearch():
    return render_template('admsearch.html')


@managekg.route('/entitysearch', methods=['GET', 'POST'])
def entitysearch():
    return render_template('entitysearch.html')


@managekg.route('/entityadd', methods=['GET', 'POST'])
def entityadd():
    return render_template('entityadd.html')


@managekg.route('/entityinfo', methods=['GET', 'POST'])
def entityinfo():
    name = request.form['entity_zh']
    data = searchentity(name)
    if len(data) == 0:
        return render_template('entity404.html')
    # print(data)
    data1 = data['data']
    data2 = data['result']
    datas = dict(zip(data1, data2))
    # print(datas)
    # for i in data1:
    #     print(i)
    return render_template('entityinfo.html', datas=datas)


@managekg.route('/entityalter', methods=['GET', 'POST'])
def entityalter():
    name = request.form['entity_zh']
    data = searchentity(name)
    if len(data) == 0:
        return render_template('entity404.html')
    # print(data)
    data1 = data['data']
    data2 = data['result']
    datas = dict(zip(data1, data2))
    # for i in datas:
    #     print(datas[i])
    # print(datas['label_zh'])
    return render_template('entityalter.html', datas=datas)


@managekg.route('/relasearch', methods=['GET', 'POST'])
def relasearch():
    return render_template('relasearch.html')


@managekg.route('/relasearch2', methods=['GET', 'POST'])
def relasearch2():
    return render_template('relasearch2.html')


@managekg.route('/relationadd', methods=['GET', 'POST'])
def relationadd():
    name = request.form['entity_zh']
    # print(name)
    data = searchentity(name)
    if len(data) == 0:
        return render_template('entity404.html')
    return render_template('relationadd.html', entity_zh=name)


@managekg.route('/relationdel', methods=['GET', 'POST'])
def relationdel():
    name = request.form['entity_zh']
    data = searchentity(name)
    if len(data) == 0:
        return render_template('entity404.html')
    return render_template('relationdel.html', entity_zh=name)


@managekg.route('/add_entity', methods=['GET', 'POST'])
def add_entity():
    name = request.args.get('name')
    addnode(str(name))


@managekg.route('/del_entity', methods=['GET', 'POST'])
def del_entity():
    namejson = request.args.get('name')
    print(namejson, type(namejson))
    namejson = ast.literal_eval(namejson)
    name = namejson['label_zh']
    print(name)
    delnode(str(name))


@managekg.route('/add_pro', methods=['GET', 'POST'])
def add_pro():
    datas = request.args.get('datas')
    dataJson = request.args.get('dataJson')
    datas = ast.literal_eval(datas)
    dataJson = ast.literal_eval(dataJson)
    # print(datas)
    # print(dataJson)
    addpro(datas['label_zh'], dataJson)


@managekg.route('/del_pro', methods=['GET', 'POST'])
def del_pro():
    name = request.args.get('name')
    datas = request.args.get('datas')
    datas = ast.literal_eval(datas)
    delpro(datas['label_zh'], name)


@managekg.route('/mod_pro', methods=['GET', 'POST'])
def mod_pro():
    datas = request.args.get('datas')
    pros = request.args.get('pros')
    datas = ast.literal_eval(datas)
    pros = ast.literal_eval(pros)
    label_zh = datas['label_zh']
    names = []
    for i in datas:
        names.append(i)
    datasnew = dict(zip(names, pros))
    # print(datasnew)
    modpro(label_zh, datasnew)


@managekg.route('/add_relation', methods=['GET', 'POST'])
def add_relation():
    head_name = request.args.get('head_name')
    end_name = request.args.get('end_name')
    relation_name = request.args.get('relation_name')
    addrelation(head_name, end_name, relation_name)
    json_data = query(str(head_name))
    return jsonify(json_data)


@managekg.route('/del_relation', methods=['GET', 'POST'])
def del_relation():
    head_name = request.args.get('head_name')
    end_name = request.args.get('end_name')
    delrelation(head_name, end_name)
    json_data = query(str(head_name))
    return jsonify(json_data)
#TEST
