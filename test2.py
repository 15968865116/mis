# -*- coding:utf-8 -*-
from flask import Flask,render_template
from flask import request
from flask import make_response
from flask import abort, redirect, url_for
from flask import session
from flask_session import Session
from flask import g
import pymssql
import sys
import copy
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)




conn = pymssql.connect(host=r"localhost",user=r"sa",password=r"123456",database=r"medecine",charset=r'utf8')
cursor=conn.cursor()




app=Flask(__name__)
app.config['SECRET_KEY'] = 'you never guess' # 使用 session 必须要配置这个，不然会报500错误的！

list_for_yd=[]
j=0
k=0
wwc_count=0
ywc_count=0 

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
    global list_for_yd
    cursor.execute('select m_name from duizhao')
    allname=cursor.fetchall()
    list_for_allname=[]
    list_for_linshi1=list(allname)
    
    for i in range(len(list_for_linshi1)):
        a=list_for_linshi1[i][0].encode('UTF-8')
        b=a.strip()
        list_for_allname.append(b)


    
    print(list_for_allname)
    a=''
    medicine_for_list={'ypxx':list_for_yd,'xinxi':a,'selectvalue':list_for_allname}
    return render_template('createmedecine.html',**medicine_for_list)

@app.route('/create_medicine',methods=['POST'])
def create_medicine1():

    list_for_now=[]#临时存储
    global list_for_yd
    num=request.form['gongneng']#操作
    if (num=='1'):#判断是什么操作
        
        mn=request.form['medicinename']#药品名称
        sl=request.form['medicinenum']#数量
        br=request.form['illnum']#病人编号
        
        if(mn!=''and sl!='' and br!=''):#判断是否有空，没有空参数进行下列操作
            
            slzs=int(sl)
            list_for_now.append(mn)#药品名字进列表
            list_for_now.append(slzs)#药品数量进列表
            list_for_now.append(br)#病人编号进列表

            cursor.execute('select m_id from duizhao where m_name=%s',mn)
            ypid=cursor.fetchone()
            ypid1=ypid[0]
            ypidjm=ypid1.encode('UTF-8')        
            list_for_now.append(ypidjm)#药品编号解码进列表

            list_for_now.append(session['xingming'])#医生姓名进列表

            cursor.execute('select m_price from duizhao where m_name=%s',mn)
            prprice=cursor.fetchone()#找单价
            prprice1=prprice[0]           
            allprice=10.0
            allprice=slzs*prprice1
            list_for_now.append(allprice)

            list_for_now.append('false')


            list_for_yd.append(list_for_now)
            list_for_now=[]
        
            cursor.execute('select m_name from duizhao')
            allname=cursor.fetchall()
            list_for_allname=[]
            list_for_linshi1=list(allname)
    
            for i in range(len(list_for_linshi1)):

                a=list_for_linshi1[i][0].encode('UTF-8')
                b=a.strip()
                list_for_allname.append(b)
            a=''
            medicine_for_list={'ypxx':list_for_yd,'xinxi':a,'selectvalue':list_for_allname}
            return render_template('createmedecine.html',**medicine_for_list)

        elif(num=='' or sl=='' or br==''):
            cursor.execute('select m_name from duizhao')
            allname=cursor.fetchall()
            list_for_allname=[]
            list_for_linshi1=list(allname)
    
            for i in range(len(list_for_linshi1)):

                a=list_for_linshi1[i][0].encode('UTF-8')
                b=a.strip()
                list_for_allname.append(b)
            a="有输入为空"
            medicine_for_list={'ypxx':list_for_yd,'xinxi':a,'selectvalue':list_for_allname}
            
            return render_template('createmedecine.html',**medicine_for_list)
    elif(num=='2'):#判断是什么操作
        list_for_yd1=[]
        list_for_yd1=copy.deepcopy(list_for_yd)
        list_for_yd=[]
        list_num=len(list_for_yd1)
        for i in range(0,list_num):
            cursor.execute('insert into yaodan(m_id,m_name,num,docname,ill_id,allpri,isok) values(%s,%s,%s,%s,%s,%s,%s)',(list_for_yd1[i][3],list_for_yd1[i][0],list_for_yd1[i][1],list_for_yd1[i][4],list_for_yd1[i][2],list_for_yd1[i][5],list_for_yd1[i][6]))
            conn.commit()
        return redirect(url_for('login_for_doc'))
        
        
        
        
    elif(num=='3'):
        list_for_yd.pop();
        cursor.execute('select m_name from duizhao')
        allname=cursor.fetchall()
        list_for_allname=[]
        list_for_linshi1=list(allname)
    
        for i in range(len(list_for_linshi1)):#获取所有药品名字

            a=list_for_linshi1[i][0].encode('UTF-8')
            b=a.strip()
            list_for_allname.append(b)

        a=''
        medicine_for_list={'ypxx':list_for_yd,'xinxi':a,'selectvalue':list_for_allname}
        return render_template('createmedecine.html',**medicine_for_list)

@app.route('/search_medicine',methods=['GET'])
def search_medicine():
    list_yaodanwwcls=[]
    list_yaodanywcls=[]
    cursor.execute('select * from yaodan where docname=%s',session['xingming'])
    all_news=cursor.fetchall()
    print(all_news)
    all_news_list=list(all_news)
    list_news_lists=[]
    list_for_show=[]
    for i in range(len(all_news_list)):
        m_id=all_news_list[i][0].encode('UTF-8')
        mid1=m_id.strip()
        m_name=all_news_list[i][1].encode('UTF-8')
        name1=m_name.strip()
        num=all_news_list[i][2]
        docname=all_news_list[i][3].encode('UTF-8')
        docname1=docname.strip()
        ill_id=all_news_list[i][4].encode('UTF-8')
        iid=ill_id.strip()
        allpri=all_news_list[i][5]
        isok=all_news_list[i][6].encode('UTF-8')
        isok1=isok.strip()
        list_news_lists.append(mid1)
        list_news_lists.append(name1)
        list_news_lists.append(num)
        list_news_lists.append(docname1)
        list_news_lists.append(iid)
        list_news_lists.append(allpri)
        list_news_lists.append(isok)
        list_for_show.append(list_news_lists)
        list_news_lists=[]

    medicine_for_list={'ypxx':list_for_show}
    return render_template('search.html',**medicine_for_list)

@app.route('/login_for_cangku')#仓库管理
def login_for_cangku():
    return render_template('cangku.html')


@app.route('/login_for_yaofang',methods=['GET'])#药房管理
def login_for_yaofang():
    cursor.execute('select m_name from duizhao')
    allname=cursor.fetchall()
    list_for_allname=[]
    list_for_linshi1=list(allname)
    
    for i in range(len(list_for_linshi1)):#获取所有药品名字
        a=list_for_linshi1[i][0].encode('UTF-8')
        b=a.strip()
        list_for_allname.append(b)


    false='false'#未完成药单查询五个一组
    global j
    list_yaodanwwc=[]
    list_news_lists=[]
    cursor.execute('select * from yaodan where isok=%s',false)
    yaodan_wwc=cursor.fetchall()
    list_yaodan_wwc=list(yaodan_wwc)
    for i in range(len(list_yaodanwwc)):
        list_yaodanwwc[i]=[]
    for i in range(len(list_yaodan_wwc)):
        m_id=list_yaodan_wwc[i][0].encode('UTF-8')
        mid1=m_id.strip()
        m_name=list_yaodan_wwc[i][1].encode('UTF-8')
        name1=m_name.strip()
        num=list_yaodan_wwc[i][2]
        docname=list_yaodan_wwc[i][3].encode('UTF-8')
        docname1=docname.strip()
        ill_id=list_yaodan_wwc[i][4].encode('UTF-8')
        iid=ill_id.strip()
        allpri=list_yaodan_wwc[i][5]
        isok=list_yaodan_wwc[i][6].encode('UTF-8')
        isok1=isok.strip()
        list_news_lists.append(mid1)
        list_news_lists.append(name1)
        list_news_lists.append(num)
        list_news_lists.append(docname1)
        list_news_lists.append(iid)
        list_news_lists.append(allpri)
        list_news_lists.append(isok)
        list_yaodanwwc.append(list_news_lists)
        list_news_lists=[]
        
    global k
    true='true'#已完成药单信息查询 五个一组
    list_yaodanywc=[]

    cursor.execute('select * from yaodan where isok=%s',true)
    yaodan_ywc=cursor.fetchall()
    list_yaodan_ywc=list(yaodan_ywc)
    for i in range(len(list_yaodan_ywc)):
        m_id=list_yaodan_ywc[i][0].encode('UTF-8')
        mid1=m_id.strip()
        m_name=list_yaodan_ywc[i][1].encode('UTF-8')
        name1=m_name.strip()
        num=list_yaodan_ywc[i][2]
        docname=list_yaodan_ywc[i][3].encode('UTF-8')
        docname1=docname.strip()
        ill_id=list_yaodan_ywc[i][4].encode('UTF-8')
        iid=ill_id.strip()
        allpri=list_yaodan_ywc[i][5]
        isok=list_yaodan_ywc[i][6].encode('UTF-8')
        isok1=isok.strip()
        list_news_lists.append(mid1)
        list_news_lists.append(name1)
        list_news_lists.append(num)
        list_news_lists.append(docname1)
        list_news_lists.append(iid)
        list_news_lists.append(allpri)
        list_news_lists.append(isok)
        list_yaodanywc.append(list_news_lists)
        list_news_lists=[]
    if(len(list_yaodanwwc)%5==0):
        pcount1=len(list_yaodanwwc)/5
    else:
        pcount1=len(list_yaodanwwc)/5+1

    if(len(list_yaodanywc)%5==0):
        pcount2=len(list_yaodanywc)/5
    else:
        pcount2=len(list_yaodanywc)/5+1
    
    global wwc_count
    global ywc_count  
    wwc_count=pcount1
    ywc_count=pcount2

    

    
    dq_wwc=j+1
    dq_ywc=k+1
    list_yaodanywcls1=[]
    list_yaodanwwcls1=[]
    list_yaodanywcls=[]
    list_yaodanwwcls=[]
    for i in range(5*j,(j+1)*5+1):
        if(len(list_yaodanwwc)-1<i):
            break;
        list_yaodanwwcls1.append(list_yaodanwwc[i])
    list_yaodanwwcls=copy.deepcopy(list_yaodanwwcls1)
    list_yaodanwwcls1=[]
    for i in range(5*k,(k+1)*5+1):
        if(len(list_yaodanywc)-1<i):
            break;
        list_yaodanywcls1.append(list_yaodanywc[i])
    list_yaodanywcls=copy.deepcopy(list_yaodanywcls1)
    list_yaodanywcls1=[]



    medicine_for_list={'ypxxwwc':list_yaodanwwcls,'ypxxywc':list_yaodanywcls,'selectvalue':list_for_allname,'ywccount':ywc_count,'wwccount':wwc_count,'dqwwc':dq_wwc,'dqywc':dq_ywc}
    

    return render_template('yaofang.html',**medicine_for_list)

@app.route('/login_for_yaofang',methods=['POST'])#药房管理
def login_for_yaofang1():
    caozuo=request.form['gongneng']
    global wwc_count
    global ywc_count
    global j
    global k
    if(caozuo=='1'):
        if(j==0):
            return redirect(url_for('login_for_yaofang'))
        else:
            j=j-1
            return redirect(url_for('login_for_yaofang'))
    elif(caozuo=='2'):
        if(j>=(wwc_count-1)):
            return redirect(url_for('login_for_yaofang'))
        else:
            j=j+1
            return redirect(url_for('login_for_yaofang'))
    elif(caozuo=='3'):
        if(k==0):
            return redirect(url_for('login_for_yaofang'))
        else:
            k=k-1
            return redirect(url_for('login_for_yaofang'))
    elif(caozuo=='4'):
        if(k>=(ywc_count-1)):
            return redirect(url_for('login_for_yaofang'))
        else:
            k=k+1
            return redirect(url_for('login_for_yaofang'))
    elif(caozuo=='5'):
        ill=request.form['patient']
        true='true'
        cursor.execute('update yaodan set isok=%s where ill_id=%s',(true,ill))
        conn.commit()
        return redirect(url_for('login_for_yaofang'))



@app.route('/wrong')#登录失败
def wrong():
    return "<a>hhhh</a>"
        

if __name__=='__main__':
    
    app.run()