# -*- coding:utf-8 -*-
from flask import Flask,render_template
from flask import request
from flask import make_response
from flask import abort, redirect, url_for
from flask import session
from flask_session import Session
from flask import g
import pymssql


conn = pymssql.connect(host=r"localhost",user=r"sa",password=r"123456",database=r"medecine",charset=r'utf8')
cursor=conn.cursor()




app=Flask(__name__)
app.config['SECRET_KEY'] = 'you never guess' # 使用 session 必须要配置这个，不然会报500错误的！

list_for_yd=[]

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
    name=re[2].strip()
    
    poc=re[3].encode('UTF-8')#解码,职位
    poc1=poc.strip()
    bpwd=b.encode('UTF-8')#解码
    session['xingming']=name
    session['zhiwei'] =poc1 

    if (pwdfn==bpwd and poc1=="医生"):#判断用户名密码是否正确
        return redirect(url_for('login_for_doc'))
    elif (pwdfn==bpwd and poc1=="仓库管理员"):#判断用户名密码是否正确
        return redirect(url_for('login_for_cangku'))
    elif (pwdfn==bpwd and poc1=="药房管理员"):#判断用户名密码是否正确
        return redirect(url_for('login_for_yaofang'))
    else:
    	return redirect(url_for('wrong'))


@app.route('/login_for_doc',methods=['GET'])#医生
def login_for_doc():
    context={'username':session['xingming']}

    return render_template('yisheng.html' ,**context)

@app.route('/login_for_doc',methods=['POST'])#医生
def readytocreate():
    num=request.form['gongneng']
    if (num=='1'):#判断去哪个页面
		return redirect(url_for('create_medicine'))#新建药方
    elif(num=='2'):
    	return redirect(url_for('search_medicine'))#查询旧药方



@app.route('/create_medicine',methods=['GET'])
def create_medicine():
	return render_template('createmedecine.html')

@app.route('/create_medicine',methods=['POST'])
def create_medicine1():
    
    list_for_now=[]#临时存储
    global list_for_yd
    num=request.form['gongneng']#操作
    if (num=='1'):#判断是什么操作
        mn=request.form['medicinename']#药品名称
        sl=request.form['medicinenum']#数量
        br=request.form['illnum']#病人编号
        
        list_for_now.append(mn)
        list_for_now.append(sl)
        list_for_now.append(br)
        list_for_yd.append(list_for_now)
        list_for_now=[]
        
        
        medicine_for_list={'ypxx':list_for_yd}
        
        return render_template('createmedecine.html',**medicine_for_list)
    elif(num=='2'):#判断是什么操作
        list_num=len(list_for_yd)
        for i in range(0,list_num):
            cursor.execute('select m_id from duizhao where m_name=%s',list_for_yd[i][0])
            m_id1=cursor.fetchone()
            cursor.execute('select m_price from duizhao where m_name=%s',list_for_yd[i][0])
            m_price1=cursor.fetchone()
            nub=int(list_for_yd[i][1])
            alprice=nub*m_price1
            cursor.execute('insert into yaodao values(%s,%s,%d,%s,%s,%f,%s)',m_id1,list_for_yd[i][0],nub,session['xingming'],list_for_yd[i][2],alprice,'no')
            conn.commit()
        session['cunzhi']=[]
        
        
        return redirect(url_for('create_medicine'))


@app.route('/search_medicine',methods=['GET'])
def search_medicine():
	return render_template('search.html')

@app.route('/login_for_cangku')#仓库管理
def login_for_cangku():
    return render_template('cangku.html')


@app.route('/login_for_yaofang')#药房管理
def login_for_yaofang():
    return render_template('yaofang.html')


@app.route('/wrong')#登录失败
def wrong():
    return "<a>hhhh</a>"
        

if __name__=='__main__':
    
    app.run()