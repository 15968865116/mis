# -*- coding:utf-8 -*-
from flask import Flask,render_template
from flask import request
from flask import make_response
from flask import abort, redirect, url_for
import pymssql
conn = pymssql.connect(host=r"localhost",user=r"sa",password=r"123456",database=r"medecine",charset=r'utf8')
cursor=conn.cursor()

app=Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    
    return render_template('upload.html')
@app.route('/', methods=['POST'])
def upload():
    a=request.form['user1']
    b=request.form['pwd1']
    cursor.execute('select * from usermessage where id=%s ',a)
    re=cursor.fetchone()#取得查询出来的数据，列表形式
    pwd=re[1].encode('UTF-8')#查询返回的是uicode形式，并且包含空格，此处解码
    pwdfn=pwd.strip()#此处去除空格
    name=re[2].encode('UTF-8')#解码
    bpwd=b.encode('UTF-8')#解码  

    if (pwdfn==bpwd):#判断用户名密码是否正确
        return redirect(url_for('login'))
    else:
    	return redirect(url_for('wrong'))
@app.route('/login')
def login():
    return render_template('test1.html')
@app.route('/wrong')
def wrong():
    return "<a>hhhh</a>"
        

if __name__=='__main__':
    app.run()