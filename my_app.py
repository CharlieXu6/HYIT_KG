#coding:utf-8
import os

from flask import Flask, render_template, request, jsonify, session
from inquire_kg import query
# from preprocess_data import Question
import pymysql
import time
from managekg import *
import excel2neo4j
import question_classify
import question_parser
import inquire_kg
db = pymysql.connect(host="127.0.0.1", user="root", passwd='12345678', db='prog')
cur = db.cursor()
# que = Question()
app = Flask(__name__)
app.register_blueprint(managekg)
app.config['SECRET_KEY'] = os.urandom(24)  # 生成24位的随机数种子，用于产生SESSION ID
# 上传文件
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['xls','xlsx'])  # 允许上传的文件后缀


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template('index.html')


@app.route('/login',methods=['GET'])
def login1():
    session.clear()
    print('test')
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    sql = """ select username,password from sign where username='%s' and password='%s' """ % (username, password)
    cur.execute(sql)
    results = cur.fetchone()
    if results:
        session['is_login'] = 'true'
        return render_template('admsearch.html')
        db.close()
    else:
        return render_template('login.html',method=['GET'])
        db.close()


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    return render_template('index_bak.html')

@app.route('/message', methods=['POST'])
def reply():
    question = request.form['msg']
    question_type = question_classify.classify(question)
    if question_type == "ok":
        answer = question_parser.get_answer(question)
    else:
        answer = "我暂时回答不了这个问题！"
    print(answer)
    return jsonify({'text': answer})


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))

    return jsonify(json_data)


@app.route('/show_relation', methods=['GET', 'POST'])
def show_relation():
    name = request.args.get('name')
    json_data = query(str(name))
    # print(name)
    return jsonify(json_data)


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 具有上传功能的页面
@app.route('/upload_index')
def upload_test():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    del_file(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = f.filename
        f.save(os.path.join(file_dir, fname))  # 保存文件到upload目录
        return jsonify({"errno": 0, "errmsg": "uplaod successful"})
    else:
        return jsonify({"errno": 1001, "errmsg": "upload failed"})

# 删除文件夹下的所有文件
def del_file(path_data):
    for i in os.listdir(path_data): # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "/" + i #当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True: #os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)

@app.route('/build_kg', methods=['GET', 'POST'])
def build_kg():
    excel2neo4j.build_nodes('Vertexes')
    excel2neo4j.build_entity_relationship('Edges')
    return render_template('search.html')

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"  # 指定浏览器渲染的文件类型，和解码格式；
