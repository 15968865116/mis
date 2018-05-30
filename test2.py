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
list_for_rec=[]


a=''
control2=0
cangku_page_search=0
cangku_count_search=0
cangku_page_jinhuo=0
cangku_count_jinhuo=0
cangku_page_chuhuo=0
cangku_count_chuhuo=0
recorddq=0
recordcount=0
yaodan=0
yaodancount=0
allcount=0
control=0
control1=0
control_for_cksearch=0
control_for_ckjinhuo=0
control_for_ckchuhuo=0
j=0
k=0
yaofangdq=0
wwc_count=0
ywc_count=0 
text=''
text2=''
list_for_yd=[]
list_for_chaxun=[]
pick_for_cangku_all=[]
list_for_cangku_select=[]
list_for_cangku_jinhuo=[]
list_for_cangku_chuhuo=[]
text_for_qy=''
text_for_upload=''
text_for_cangku_jin=''
text_for_cangku_chu=''
text_for_cangku_search=''
text_for_cangku_jinhuo=''
text_for_cangku_chuhuo=''
text_for_duizhao=''







@app.route('/index',methods=['GET'])
def index():
    global text_for_upload
    te={'text':text_for_upload}
    return render_template('upload.html',**te)
@app.route('/index', methods=['POST'])
def upload():
    global text_for_upload
    a=request.form['user1']
    b=request.form['pwd1']
    if(a=='' or b==''):
        text_for_upload='有输入为空，请重新输入'
        return redirect(url_for('index'))
    else:

        cursor.execute('select * from usermessage where id=%s ',a)
        re=cursor.fetchone()#取得查询出来的数据，列表形式
        if(re==None):
            text_for_upload='用户名或密码错误'
            return redirect(url_for('index'))
        else:
            text_for_upload=''
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
                return redirect(url_for('yaofangmanager'))
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
    elif(num=='3'):
        session['xingming']=''
        return redirect(url_for('index'))

@app.route('/create_medicine',methods=['GET'])
def create_medicine():
    global list_for_yd
    global a
    cursor.execute('select m_name from duizhao')
    allname=cursor.fetchall()
    list_for_allname=[]
    list_for_linshi1=list(allname)
    
    for i in range(len(list_for_linshi1)):
        al=list_for_linshi1[i][0].encode('UTF-8')
        b=al.strip()
        list_for_allname.append(b)

    
    medicine_for_list={'ypxx':list_for_yd,'xinxi':a,'selectvalue':list_for_allname}
    return render_template('createmedecine.html',**medicine_for_list)

@app.route('/create_medicine',methods=['POST'])
def create_medicine1():

    list_for_now=[]#临时存储
    global list_for_yd
    global a
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
        
            a=''
            
            return redirect(url_for('create_medicine'))

        else:

            a="有输入为空"
            
            return redirect(url_for('create_medicine'))
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
        if(len(list_for_yd)>=1):
            list_for_yd.pop();
            a=''
            return redirect(url_for('create_medicine'))

        else:
            a=''
            return redirect(url_for('create_medicine'))

    elif(num=='4'):
        a=''
        list_for_yd=[]
        return redirect(url_for('login_for_doc'))

@app.route('/search_medicine',methods=['GET'])
def search_medicine():
    list_yaodanwwcls=[]
    list_yaodanywcls=[]
    global yaodan
    global yaodancount
    cursor.execute('select * from yaodan where docname=%s',session['xingming'])
    all_news=cursor.fetchall()
    
    all_news_list=list(all_news)
    list_news_lists=[]
    list_for_show=[]
    list_ls=[]
    list_ls1=[]
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

    if(len(list_for_show)%15==0):
        yaodancount=len(list_for_show)/15
    else:
        yaodancount=len(list_for_show)/15+1

    for i in range(15*yaodan,(yaodan+1)*15):
        if(len(list_for_show)-1<i):
            break;
        list_ls1.append(list_for_show[i])
    list_ls=copy.deepcopy(list_ls1)
    list_ls1=[]
    pagecount=yaodancount
    pagedq=yaodan+1
    medicine_for_list={'ypxx':list_ls,'count':pagecount,'dq':pagedq}
    return render_template('search.html',**medicine_for_list)

@app.route('/search_medicine',methods=['POST'])
def search_medicine1():
    global yaodan
    global yaodancount
    caozuo=request.form['gongneng']
    if(caozuo=='1'):
        if(yaodan==0):
            return redirect(url_for('search_medicine'))
        else:
            yaodan=yaodan-1
            return redirect(url_for('search_medicine'))
    elif(caozuo=='2'):
        if(yaodan>=(yaodancount-1)):
            return redirect(url_for('search_medicine'))
        else:
            yaodan=yaodan+1
            return redirect(url_for('search_medicine'))
    elif(caozuo=='3'):
        yaodan=0
        return redirect(url_for('login_for_doc'))





@app.route('/login_for_cangku',methods=['GET'])#仓库管理
def login_for_cangku():

    return render_template('cangku.html')

@app.route('/login_for_cangku',methods=['POST'])#仓库管理
def login_for_cangku1():
    caozuo=request.form['gongneng']
    if(caozuo=='1'):
        return redirect(url_for('cangku_jinhuo'))
    elif(caozuo=='2'):
        return redirect(url_for('cangku_chuhuo'))
    elif(caozuo=='3'):
        return redirect(url_for('cangku_search'))
    elif(caozuo=='4'):
        return redirect(url_for('cangku_jinchu'))
    elif(caozuo=='5'):
        session['xingming']=''
        return redirect(url_for('index'))


@app.route('/cangku_jinhuo',methods=['GET'])#仓库进货情况查询
def cangku_jinhuo():
    global control_for_ckjinhuo
    global cangku_count_jinhuo
    global cangku_page_jinhuo
    global list_for_cangku_jinhuo
    global text_for_cangku_jinhuo
    if(control_for_ckjinhuo==0):
        cursor.execute('select * from jinhuo')
        jinhuo=cursor.fetchall()
        list_jinhuo=list(jinhuo)
        ls=[]
        ls2=[]
        for_show=[]
        for i in range(len(list_jinhuo)):
            name=list_jinhuo[i][0].encode('UTF-8')
            m_name=name.strip()
            mid=list_jinhuo[i][1].encode('UTF-8')
            m_id=mid.strip()
            num=list_jinhuo[i][2]
            loc=list_jinhuo[i][3].encode('UTF-8')
            m_loc=loc.strip()
            scdate=list_jinhuo[i][4]
            bzq=list_jinhuo[i][5]
            jhdate=list_jinhuo[i][6]
            price=list_jinhuo[i][7]

            ls.append(m_name)
            ls.append(m_id)
            ls.append(num)
            ls.append(m_loc)
            ls.append(scdate)
            ls.append(bzq)
            ls.append(jhdate)
            ls.append(price)
            for_show.append(ls)
            ls=[]
        if(len(for_show)%15==0):
            cangku_count_jinhuo=len(for_show)/15
        else:
            cangku_count_jinhuo=len(for_show)/15+1

        for i in range(cangku_page_jinhuo*15,(cangku_page_jinhuo+1)*15):
            if(len(for_show)-1<i):
                break;
            ls.append(for_show[i])
        ls2=copy.deepcopy(ls)
        ls=[]
        dq=cangku_page_jinhuo+1

        
        me={'qyxx':ls2,'text':text_for_cangku_jinhuo,'dq':dq,'count':cangku_count_jinhuo}

        return render_template('cangku_jinhuo.html',**me)
    elif(control_for_ckjinhuo==1):
        if(text_for_cangku_jinhuo==''):
            ls=[]
            ls2=[]
            if(len(list_for_cangku_jinhuo)%15==0):
                cangku_count_jinhuo=len(list_for_cangku_jinhuo)/15
            else:
                cangku_count_jinhuo=len(list_for_cangku_jinhuo)/15+1

            for i in range(cangku_page_jinhuo*15,(cangku_page_jinhuo+1)*15):
                if(len(list_for_cangku_jinhuo)-1<i):
                    break;
                else:
                    ls.append(list_for_cangku_jinhuo[i])
            ls2=copy.deepcopy(ls)
            ls=[]
            dq=cangku_page_jinhuo+1

            text_for_cangku_jinhuo=''
            me={'qyxx':ls2,'text':text_for_cangku_jinhuo,'dq':dq,'count':cangku_count_jinhuo}
            return render_template('cangku_jinhuo.html',**me)
        else:
            dq=1
            count=1
            me={'qyxx':list_for_cangku_jinhuo,'text':text_for_cangku_jinhuo,'dq':dq,'count':count}
            return render_template('cangku_jinhuo.html',**me)

@app.route('/cangku_jinhuo',methods=['POST'])#仓库进货情况查询
def cangku_jinhuo1():
    global control_for_ckjinhuo
    global cangku_count_jinhuo
    global cangku_page_jinhuo
    global list_for_cangku_jinhuo
    global text_for_cangku_jinhuo

    caozuo=request.form['gongneng']
    if(caozuo=='1'):
        if(cangku_page_jinhuo==0):
            return redirect(url_for('cangku_jinhuo'))
        else:
            cangku_page_jinhuo=cangku_page_jinhuo-1
            return redirect(url_for('cangku_jinhuo'))   
    elif(caozuo=='2'):
        if(cangku_page_jinhuo>=(cangku_count_jinhuo-1)):
            return redirect(url_for('cangku_jinhuo'))
        else:
            cangku_page_jinhuo=cangku_page_jinhuo+1
            return redirect(url_for('cangku_jinhuo'))

    elif(caozuo=='3'):
        text_for_cangku_jinhuo=''
        list_for_cangku_jinhuo=[]
        cangku_page_jinhuo=0

        return redirect(url_for('login_for_cangku'))
    elif(caozuo=='4'):
        control_for_ckjinhuo=1
        nian=request.form['nian']
        yue=request.form['yue']
        ri=request.form['ri']
        if(nian!='' and yue!='' and ri!=''):
            date=nian+'-'+yue+'-'+ri
            cursor.execute('select * from jinhuo where jhdate=%s',date)
            n=cursor.fetchone()
            
            if(n!=None):
                cangku_page_jinhuo=0
                cursor.execute('select * from jinhuo where jhdate=%s',date)
                jinhuo=cursor.fetchall()
                list_jinhuo=list(jinhuo)
                ls=[]
                for_show=[]
                for i in range(len(list_jinhuo)):
                    name=list_jinhuo[i][0].encode('UTF-8')
                    m_name=name.strip()
                    mid=list_jinhuo[i][1].encode('UTF-8')
                    m_id=mid.strip()
                    num=list_jinhuo[i][2]
                    loc=list_jinhuo[i][3].encode('UTF-8')
                    m_loc=loc.strip()
                    scdate=list_jinhuo[i][4]
                    bzq=list_jinhuo[i][5]
                    jhdate=list_jinhuo[i][6]
                    price=list_jinhuo[i][7]

                    ls.append(m_name)
                    ls.append(m_id)
                    ls.append(num)
                    ls.append(m_loc)
                    ls.append(scdate)
                    ls.append(bzq)
                    ls.append(jhdate)
                    ls.append(price)
                    list_for_cangku_jinhuo.append(ls)
                text_for_cangku_jinhuo=''
                return redirect(url_for('cangku_jinhuo'))
            else:
                list_for_cangku_jinhuo=[]
                text_for_cangku_jinhuo='无当前日期数据'
                return redirect(url_for('cangku_jinhuo'))
        else:
            control_for_ckjinhuo=0
            text_for_cangku_jinhuo='有输入为空，请重新输入'
            return redirect(url_for('cangku_jinhuo'))


                
    elif(caozuo=='5'):
        control_for_ckjinhuo=0
        text_for_cangku_jinhuo=''
        cangku_page_jinhuo=0
        list_for_cangku_jinhuo=[]
        return redirect(url_for('cangku_jinhuo'))
    elif(caozuo=='6'):
        control_for_ckjinhuo=1
        ypname=request.form['ypname']
        if(ypname!=''):
            cursor.execute('select * from jinhuo where m_name=%s',ypname)
            n=cursor.fetchone()
            if(n!=None):
                cangku_page_jinhuo=0
                cursor.execute('select * from jinhuo where m_name=%s',ypname)
                jinhuo=cursor.fetchall()
                list_jinhuo=list(jinhuo)
                ls=[]
                for_show=[]
                for i in range(len(list_jinhuo)):
                    name=list_jinhuo[i][0].encode('UTF-8')
                    m_name=name.strip()
                    mid=list_jinhuo[i][1].encode('UTF-8')
                    m_id=mid.strip()
                    num=list_jinhuo[i][2]
                    loc=list_jinhuo[i][3].encode('UTF-8')
                    m_loc=loc.strip()
                    scdate=list_jinhuo[i][4]
                    bzq=list_jinhuo[i][5]
                    jhdate=list_jinhuo[i][6]
                    price=list_jinhuo[i][7]

                    ls.append(m_name)
                    ls.append(m_id)
                    ls.append(num)
                    ls.append(m_loc)
                    ls.append(scdate)
                    ls.append(bzq)
                    ls.append(jhdate)
                    ls.append(price)
                    list_for_cangku_jinhuo.append(ls)
                    ls=[]
                text_for_cangku_jinhuo=''
                return redirect(url_for('cangku_jinhuo'))

            else:
                text_for_cangku_jinhuo='没有此药品的数据'
                list_for_cangku_jinhuo=[]
                return redirect(url_for('cangku_jinhuo'))

        else:
            text_for_cangku_jinhuo='当前查找药品名字为空，请重新输入'
            list_for_cangku_jinhuo=[]
            return redirect(url_for('cangku_jinhuo'))



@app.route('/cangku_chuhuo',methods=['GET'])#仓库出货情况查询
def cangku_chuhuo():
    global control_for_ckchuhuo
    global cangku_count_chuhuo
    global cangku_page_chuhuo
    global list_for_cangku_chuhuo
    global text_for_cangku_chuhuo
    if(control_for_ckchuhuo==0):
        cursor.execute('select * from chuhuo')
        chuhuo=cursor.fetchall()
        list_chuhuo=list(chuhuo)
        ls=[]
        ls2=[]
        for_show=[]
        for i in range(len(list_chuhuo)):
            name=list_chuhuo[i][0].encode('UTF-8')
            m_name=name.strip()
            num=list_chuhuo[i][1]
            chdate=list_chuhuo[i][2]
            chloc=list_chuhuo[i][3].encode('UTF-8')
            ch_loc=chloc.strip()
            scdate=list_chuhuo[i][4]



            ls.append(m_name)
            ls.append(num)
            ls.append(chdate)
            ls.append(ch_loc)
            ls.append(scdate)
            for_show.append(ls)
            ls=[]
        if(len(for_show)%15==0):
            cangku_count_chuhuo=len(for_show)/15
        else:
            cangku_count_chuhuo=len(for_show)/15+1

        for i in range(cangku_page_chuhuo*15,(cangku_page_chuhuo+1)*15):
            if(len(for_show)-1<i):
                break;
            ls.append(for_show[i])
        ls2=copy.deepcopy(ls)
        ls=[]
        dq=cangku_page_chuhuo+1

        
        me={'qyxx':ls2,'text':text_for_cangku_jinhuo,'dq':dq,'count':cangku_count_chuhuo}

        return render_template('cangku_chuhuo.html',**me)

    elif(control_for_ckchuhuo==1):
        if(text_for_cangku_chuhuo==''):
            ls=[]
            ls2=[]
            if(len(list_for_cangku_chuhuo)%15==0):
                cangku_count_chuhuo=len(list_for_cangku_chuhuo)/15
            else:
                cangku_count_chuhuo=len(list_for_cangku_chuhuo)/15+1

            for i in range(cangku_page_chuhuo*15,(cangku_page_chuhuo+1)*15):
                if(len(list_for_cangku_chuhuo)-1<i):
                    break;
                else:
                    ls.append(list_for_cangku_chuhuo[i])
            ls2=copy.deepcopy(ls)
            ls=[]
            dq=cangku_page_jinhuo+1

            text_for_cangku_chuhuo=''
            me={'qyxx':ls2,'text':text_for_cangku_chuhuo,'dq':dq,'count':cangku_count_chuhuo}
            return render_template('cangku_chuhuo.html',**me)
        else:
            dq=1
            count=1
            me={'qyxx':list_for_cangku_chuhuo,'text':text_for_cangku_chuhuo,'dq':dq,'count':count}
            return render_template('cangku_chuhuo.html',**me)

@app.route('/cangku_chuhuo',methods=['POST'])#仓库出货情况查询
def cangku_chuhuo1():
    global control_for_ckchuhuo
    global cangku_count_chuhuo
    global cangku_page_chuhuo
    global list_for_cangku_chuhuo
    global text_for_cangku_chuhuo


    caozuo=request.form['gongneng']
    if(caozuo=='1'):
        if(cangku_page_chuhuo==0):
            return redirect(url_for('cangku_chuhuo'))
        else:
            cangku_page_chuhuo=cangku_page_chuhuo-1
            return redirect(url_for('cangku_chuhuo'))
    elif(caozuo=='2'):
        if(cangku_page_chuhuo>=(cangku_count_chuhuo-1)):
            return redirect(url_for('cangku_chuhuo'))
        else:
            cangku_page_chuhuo=cangku_page_chuhuo+1
            return redirect(url_for('cangku_chuhuo'))
    elif(caozuo=='3'):
        text_for_cangku_chuhuo=''
        list_for_cangku_chuhuo=[]
        control_for_ckchuhuo=0
        cangku_page_chuhuo=0
        return redirect(url_for('login_for_cangku'))

    elif(caozuo=='4'):
        control_for_ckchuhuo=1
        nian=request.form['nian']
        yue=request.form['yue']
        ri=request.form['ri']
        if(nian!='' and yue!='' and ri!=''):
            date=nian+'-'+yue+'-'+ri
            cursor.execute('select * from chuhuo where chdate=%s',date)
            n=cursor.fetchone()
            
            if(n!=None):
                cangku_page_chuhuo=0
                cursor.execute('select * from chuhuo where chdate=%s',date)
                chuhuo=cursor.fetchall()
                list_chuhuo=list(chuhuo)
                ls=[]
                for_show=[]
                for i in range(len(list_chuhuo)):
                    name=list_chuhuo[i][0].encode('UTF-8')
                    m_name=name.strip()
                    num=list_chuhuo[i][1]
                    chdate=list_chuhuo[i][2]
                    chloc=list_chuhuo[i][3].encode('UTF-8')
                    ch_loc=chloc.strip()
                    scdate=list_chuhuo[i][4]

                    ls.append(m_name)
                    ls.append(num)
                    ls.append(chdate)
                    ls.append(ch_loc)
                    ls.append(scdate)
                    list_for_cangku_chuhuo.append(ls)
                    ls=[]
                text_for_cangku_chuhuo=''
                return redirect(url_for('cangku_chuhuo'))
            else:
                list_for_cangku_chuhuo=[]
                text_for_cangku_chuhuo='无当前日期数据'
                return redirect(url_for('cangku_chuhuo'))
        else:
            control_for_ckchuhuo=0
            text_for_cangku_chuhuo='有输入为空，请重新输入'
            return redirect(url_for('cangku_chuhuo'))
    elif(caozuo=='5'):
        control_for_ckchuhuo=0
        text_for_cangku_chuhuo=''
        cangku_page_chuhuo=0
        list_for_cangku_chuhuo=[]
        return redirect(url_for('cangku_chuhuo'))

    elif(caozuo=='6'):
        control_for_ckchuhuo=1
        ypname=request.form['ypname']
        if(ypname!=''):
            cursor.execute('select * from chuhuo where m_name=%s',ypname)
            n=cursor.fetchone()
            if(n!=None):
                cangku_page_chuhuo=0
                cursor.execute('select * from chuhuo where m_name=%s',ypname)
                chuhuo=cursor.fetchall()
                list_chuhuo=list(chuhuo)
                ls=[]
                for_show=[]
                for i in range(len(list_chuhuo)):
                    name=list_chuhuo[i][0].encode('UTF-8')
                    m_name=name.strip()
                    num=list_chuhuo[i][1]
                    chdate=list_chuhuo[i][2]
                    chloc=list_chuhuo[i][3].encode('UTF-8')
                    ch_loc=chloc.strip()
                    scdate=list_chuhuo[i][4]


                    ls.append(m_name)
                    ls.append(num)
                    ls.append(chdate)
                    ls.append(ch_loc)
                    ls.append(scdate)

                    list_for_cangku_chuhuo.append(ls)
                    ls=[]
                text_for_cangku_chuhuo=''
                return redirect(url_for('cangku_chuhuo'))

            else:
                text_for_cangku_chuhuo='没有此药品的数据'
                list_for_cangku_chuhuo=[]
                return redirect(url_for('cangku_chuhuo'))

        else:
            text_for_cangku_chuhuo='当前查找药品名字为空，请重新输入'
            list_for_cangku_chuhuo=[]
            return redirect(url_for('cangku_chuhuo'))
    
    

@app.route('/cangku_search',methods=['GET'])#仓库全部查询
def cangku_search():
    global cangku_page_search
    global cangku_count_search
    global text_for_cangku_search
    global control_for_cksearch
    global pick_for_cangku_all
    global list_for_cangku_select
    if(control_for_cksearch==0):
        cursor.execute('select * from cangkukucun')
        cangkuyp=cursor.fetchall()
        list_cangkukucun=list(cangkuyp)
        ls=[]
        ls1=[]
        for_show=[]
        ls2=[]
        for i in range(len(list_cangkukucun)):
            n=list_cangkukucun[i][0].encode('UTF-8')
            name=n.strip()
            mid=list_cangkukucun[i][1].encode('UTF-8')
            m_id=mid.strip()
            num=list_cangkukucun[i][2]
            loc=list_cangkukucun[i][3].encode('UTF-8')
            loc1=loc.strip()
            scdate=list_cangkukucun[i][4]
            bzq=list_cangkukucun[i][5]
            price=list_cangkukucun[i][6]
            ls.append(name)
            ls.append(m_id)
            ls.append(num)
            ls.append(loc1)
            ls.append(scdate)
            ls.append(bzq)
            ls.append(price)
            for_show.append(ls)
            ls=[]

        if(len(for_show)%15==0):
            cangku_count_search=len(for_show)/15
        else:
            cangku_count_search=len(for_show)/15+1
        for i in range(15*cangku_page_search,15*(cangku_page_search+1)):
            if(len(for_show)-1<i):
                break;
            else:
                ls1.append(for_show[i])
        ls2=copy.deepcopy(ls1)
        ls1=[]

        page_dq=cangku_page_search+1
        
        mes={'ypxx':ls2,'dq':page_dq,'count':cangku_count_search,'text':text_for_cangku_search}
        
        return render_template('cangku_search.html',**mes)
    elif(control_for_cksearch==1):


        if(text_for_cangku_search==''):
            ls1=[]
            ls2=[]

            if(len(list_for_cangku_select)%15==0):
                cangku_count_search=len(list_for_cangku_select)/15
            else:
                cangku_count_search=len(list_for_cangku_select)/15+1
            for i in range(15*cangku_page_search,15*(cangku_page_search+1)):
                if(len(list_for_cangku_select)-1<i):
                    break;
                else:
                    ls1.append(list_for_cangku_select[i])
            ls2=copy.deepcopy(ls1)
            ls1=[]

            page_dq=cangku_page_search+1


            mes={'ypxx':ls2,'dq':page_dq,'count':cangku_count_search,'text':text_for_cangku_search}
            return render_template('cangku_search.html',**mes)
        else:

            
            page_dq1=1
            cangkuc=1
            mes={'ypxx':list_for_cangku_select,'dq':page_dq1,'count':cangkuc,'text':text_for_cangku_search}
            return render_template('cangku_search.html',**mes)

@app.route('/cangku_search',methods=['POST'])#仓库全部查询
def cangku_search1():
    caozuo=request.form['gongneng']
    global cangku_page_search
    global cangku_count_search
    global text_for_cangku_search
    global control_for_cksearch
    global pick_for_cangku_all
    global list_for_cangku_select

    if(caozuo=='1'):
        control_for_cksearch=1

        name=request.form['ypmc']
        if(name!=''):
            cursor.execute('select * from cangkukucun where m_name=%s',name)
            cangkuyp=cursor.fetchone()

            if(cangkuyp!=None):
                cangku_page_search=0
                cursor.execute('select * from cangkukucun where m_name=%s',name)
                cangkuyp1=cursor.fetchall()

                list_cangkukucun=list(cangkuyp1)
                ls=[]
                ls1=[]
                for_show=[]
                ls2=[]
                for i in range(len(list_cangkukucun)):
                    n=list_cangkukucun[i][0]
                    name1=n.encode('UTF-8')
                    name=name1.strip()
                    mid=list_cangkukucun[i][1]
                    mid1=mid.encode('UTF-8')
                    m_id=mid1.strip()
                    num=list_cangkukucun[i][2]
                    loc=list_cangkukucun[i][3]
                    loc2=loc.encode('UTF-8')
                    loc1=loc2.strip()
                    scdate=list_cangkukucun[i][4]
                    bzq=list_cangkukucun[i][5]
                    price=list_cangkukucun[i][6]
                    

                    ls.append(name)
                    ls.append(m_id)
                    ls.append(num)
                    ls.append(loc1)
                    ls.append(scdate)
                    ls.append(bzq)
                    ls.append(price)
                    list_for_cangku_select.append(ls)
                
                text_for_cangku_search=''
                return redirect(url_for('cangku_search'))

            else:
                list_for_cangku_select=[]
                text_for_cangku_search='没有此药品的数据'
                return redirect(url_for('cangku_search'))
        else:
            control_for_cksearch=0
            text_for_cangku_search='有输入为空，请重新输入'
            return redirect(url_for('cangku_search'))



    elif(caozuo=='2'):#取消查询
        control_for_cksearch=0
        list_for_cangku_select=[]
        text_for_cangku_search=''

        return redirect(url_for('cangku_search'))
    elif(caozuo=='3'):
        #上一页
        if(cangku_page_search==0):
            return redirect(url_for('cangku_search'))
        else:
            cangku_page_search=cangku_page_search-1
            return redirect(url_for('cangku_search'))
    elif(caozuo=='4'):
        if(cangku_page_search>=(cangku_count_search-1)):
            return redirect(url_for('cangku_search'))
        else:
            cangku_page_search=cangku_page_search+1
            return redirect(url_for('cangku_search'))

        #下一页

    elif(caozuo=='5'):
        control_for_cksearch=0
        list_for_cangku_select=[]
        text_for_cangku_search=''
        cangku_page_search=0
        #返回
        return redirect(url_for('login_for_cangku'))

@app.route('/cangku_jinchu',methods=['GET'])#仓库进出登记
def cangku_jinchu():
    global text_for_cangku_jin
    global text_for_cangku_chu
    global text_for_duizhao
    me={'textj':text_for_cangku_jin,'textc':text_for_cangku_chu,'textdz':text_for_duizhao}
    return render_template('cangku_jinchu.html',**me)

@app.route('/cangku_jinchu',methods=['POST'])#仓库进出登记
def cangku_jinchu1():
    global text_for_cangku_jin
    global text_for_cangku_chu
    global text_for_duizhao
    caozuo=request.form['gongneng']
    if(caozuo=='1'):
        ypnamej=request.form['ypmzj']
        ypnumj=request.form['ypslj']
        
        nianj=request.form['nianj']
        yuej=request.form['yuej']
        rij=request.form['rij']
        loc=request.form['cfwz']
        nians=request.form['niansc']
        yues=request.form['yuesc']
        ris=request.form['risc']
        bzq=request.form['bzq']
        if(ypnamej!='' and ypnumj!='' and nianj!='' and yuej!='' and rij!='' and nians!='' and yues!='' and ris!='' and loc!='' and bzq!='' ):
            datej=nianj+'-'+yuej+'-'+rij
            datesc=nians+'-'+yues+'-'+ris
            ynumj=int(ypnumj)
            cursor.execute('select * from duizhao where m_name=%s',ypnamej)
            ypdz=cursor.fetchone()
            if(ypdz==None):
                text_for_cangku_jin='对照表中无此药品对照请先添加对照'
                return redirect(url_for('cangku_jinchu'))
            else:
                bzq1=int(bzq)
                list_ypdz=list(ypdz)
                m_id=list_ypdz[0].encode('UTF-8')
                m_id1=m_id.strip()
                price=list_ypdz[2]
                cursor.execute('insert into jinhuo(m_name,m_id,num,loc,shengchanriqi,baozhiqi,jhdate,price) values(%s,%s,%s,%s,%s,%s,%s,%s)',(ypnamej,m_id1,ynumj,loc,datesc,bzq1,datej,price))
                conn.commit()

                cursor.execute('select * from cangkukucun where m_name=%s and loc=%s and shengchanriqi=%s',(ypnamej,loc,datesc))
                n=cursor.fetchone()
                if(n==None):
                    cursor.execute('insert into cangkukucun values(%s,%s,%s,%s,%s,%s,%s)',(ypnamej,m_id1,ynumj,loc,datesc,bzq1,price))
                    conn.commit()
                    return redirect(url_for('cangku_jinchu'))
                else:
                    list_n=list(n)
                    ynum=list_n[2]
                    print(ynum)
                    nnum=ynum+ynumj

                    cursor.execute('update cangkukucun set num=%s where m_name=%s and loc=%s and shengchanriqi=%s',(nnum,ypnamej,loc,datesc))
                    conn.commit()
                    return redirect(url_for('cangku_jinchu'))
        else:
            text_for_cangku_jin='有输入为空，请重新输入'
            return redirect(url_for('cangku_jinchu'))
    elif(caozuo=='2'):
        text_for_cangku_jin=''
        text_for_cangku_chu=''
        text_for_duizhao=''
        return redirect(url_for('login_for_cangku'))
    elif(caozuo=='3'):
        ypmcc=request.form['ypmzc']
        ynumc=request.form['ypslc']
        nianc=request.form['nianc']
        yuec=request.form['yuec']
        ric=request.form['ric']
        cywz=request.form['cfwzc']
        niansc=request.form['nianscc']
        yuesc=request.form['yuescc']
        riscc=request.form['riscc']
        if(ypmcc!='' and ynumc!='' and nianc!='' and yuec!='' and ric!='' and cywz!='' and niansc!='' and yuesc!='' and riscc!=''):
            cdate=nianc+'-'+yuec+'-'+ric
            scdate=niansc+'-'+yuesc+'-'+riscc
            ypnumc=int(ynumc)

            cursor.execute('select * from cangkukucun where m_name=%s and shengchanriqi=%s and loc=%s',(ypmcc,scdate,cywz))
            cyp=cursor.fetchone()
            if(cyp!=None):
                list_cyp=list(cyp)
                ylnum=list_cyp[2]
                hlnum=ylnum-ypnumc
                if(hlnum>=0):
                    cursor.execute('insert into chuhuo values(%s,%s,%s,%s,%s)',(ypmcc,ypnumc,cdate,cywz,scdate))
                    conn.commit()
                    cursor.execute('update cangkukucun set num=%s where m_name=%s and shengchanriqi=%s and loc=%s',(hlnum,ypmcc,scdate,cywz))
                    conn.commit()
                    return redirect(url_for('cangku_jinchu'))
                else:
                    text_for_cangku_chu='仓库内此药品数量不足，无法出库'
                    return redirect(url_for('cangku_jinhuo'))
            else:
                text_for_cangku_chu='仓库内无当前药品，无法进行出库操作'
                return redirect(url_for('cangku_jinchu'))

        else:
            text_for_cangku_chu='有输入为空，请重新输入'
            return redirect(url_for('cangku_jinchu'))


    elif(caozuo=='4'):
        text_for_cangku_jin=''
        text_for_cangku_chu=''
        text_for_duizhao=''
        return redirect(url_for('login_for_cangku'))
    elif(caozuo=='5'):
        ypmc=request.form['xymc']
        ypid=request.form['xyid']
        ypprice=request.form['xyjg']
        if(ypmc!='' and ypid!='' and ypprice!=''):
            ypprice1=int(ypprice)
            cursor.execute('insert into duizhao values(%s,%s,%S)',(ypmc,ypid,ypprice1))
            conn.commit()
            return redirect(url_for('cangku_jinchu'))
        else:
            text_for_duizhao='有输入为空，请重新输入'
            return redirect(url_for('cangku_jinchu'))
    elif(caozuo=='6'):
        text_for_duizhao=''
        text_for_cangku_jin=''
        text_for_cangku_chu=''
        return redirect(url_for('login_for_cangku'))

    return render_template('cangku_jinchu.html')










@app.route('/yaofangmanager',methods=['GET'])
def yaofangmanager():

    return render_template('yaofangcaozuo.html')

@app.route('/yaofangmanager',methods=['POST'])
def yaofangmanager2():
    manage_name=request.form['gongneng']
    if(manage_name=='1'):
        return redirect(url_for('login_for_yaofang'))
    elif(manage_name=='2'):
        return redirect(url_for('chakankucunyf'))
    elif(manage_name=='3'):
        return redirect(url_for('yaofangin'))
    elif(manage_name=='4'):
        return redirect(url_for('quyaojilu'))
    elif(manage_name=='5'):
        session['xingming']=""
        return redirect(url_for('index'))

    

@app.route('/chakankucunyf',methods=['GET'])
def chakankucunyf():
    
    global control
    global text
    if(control==0):
        list_kucun=[]
        list_news_kucun=[]
        list_final=[]
        cursor.execute('select * from yaofangkucun')
        kucun=cursor.fetchall()
        list_kucun=list(kucun)
        for i in range(len(list_kucun)):
            m_id=list_kucun[i][1].encode('UTF-8')
            mid1=m_id.strip()
            m_name=list_kucun[i][0].encode('UTF-8')
            name1=m_name.strip()
            num=list_kucun[i][2]
            loc=list_kucun[i][3].encode('UTF-8')
            loc1=loc.strip()
            scdate=list_kucun[i][4]
            bzq=list_kucun[i][5]
            price=list_kucun[i][6]

            
            list_news_kucun.append(mid1)
            list_news_kucun.append(name1)
            list_news_kucun.append(num)
            list_news_kucun.append(loc1)
            list_news_kucun.append(scdate)
            list_news_kucun.append(bzq)
            list_news_kucun.append(price)
            list_final.append(list_news_kucun)
            list_news_kucun=[]
            
        if(len(list_final)%15==0):
            pcount1=len(list_final)/15
        else:
            pcount1=len(list_final)/15+1
        global allcount
        allcount=pcount1 
        global yaofangdq
        dq_wwc=yaofangdq+1

        list_ls=[]
        list_ls1=[]
        for i in range(15*yaofangdq,(yaofangdq+1)*15):
            if(len(list_final)-1<i):
                break;
            list_ls1.append(list_final[i])
        list_ls=copy.deepcopy(list_ls1)
        list_ls1=[]
        text=''



        medicine_for_list={'ypzxx':list_ls,'count':allcount,'dq_count':dq_wwc,'text':text}
        return render_template('yfkucun.html',**medicine_for_list)
    elif(control==1):
        dq_wwc=yaofangdq+1
        medicine_for_list={'ypzxx':list_for_chaxun,'count':allcount,'dq_count':dq_wwc,'text':text}
        return render_template('yfkucun.html',**medicine_for_list)

@app.route('/chakankucunyf',methods=['POST'])
def chakankuyf1():
    global list_for_chaxun
    global text
    global control
    global yaofangdq
    global allcount
    list_ysls=[]
    caozuo=request.form['gongneng']
    m_name=request.form['ypmc']
    
    if(caozuo=='1'):
        if(m_name==''):
            return redirect(url_for('chakankucunyf'))
        else:
            control=1
            lu=cursor.execute('select * from yaofangkucun where m_name=%s',m_name)
            xz=cursor.fetchone()
            
                
            if(xz==None):
                text='无当前药品记录'
                allcount=0
                yaofangdq=0

                return redirect(url_for('chakankucunyf'))
                    
            else:
                list_xz=list(xz)

                m_id=list_xz[1].encode('UTF-8')
                mid1=m_id.strip()
                m_name=list_xz[0].encode('UTF-8')
                name1=m_name.strip()
                num=list_xz[2]
                loc=list_xz[3].encode('UTF-8')
                loc1=loc.strip()
                scdate=list_xz[4]
                bzq=list_xz[5]
                price=list_xz[6]

                list_ysls.append(mid1)
                list_ysls.append(name1)
                list_ysls.append(num)
                list_ysls.append(loc1)
                list_ysls.append(scdate)
                list_ysls.append(bzq)
                list_ysls.append(price)

                list_for_chaxun.append(list_ysls)
                list_ysls=[]
                    
                    
                text=''
                allcount=1
                yaofangdq=0
                return redirect(url_for('chakankucunyf'))
                
    elif(caozuo=='2'):
        control=0
        list_for_chaxun=[]
        return redirect(url_for('chakankucunyf'))
    elif(caozuo=='3'):
        if(yaofangdq==0):
            return redirect(url_for('chakankucunyf'))
        else:
            yaofangdq=yaofangdq-1
            return redirect(url_for('chakankucunyf'))
    elif(caozuo=='4'):
        if(yaofangdq>=(allcount-1)):
                
            return redirect(url_for('chakankucunyf'))
        else:
            yaofangdq=yaofangdq+1
            return redirect(url_for('chakankucunyf'))
    elif(caozuo=='5'):
        return redirect(url_for('yaofangmanager'))


@app.route('/yaofangin',methods=['GET'])
def yaofangin():
    global text2
    
    text3={'text':text2}
    
    return render_template('yaofangxinzeng.html',**text3)

@app.route('/yaofangin',methods=['POST'])
def yaofangin1():
    caozuo=request.form['gongneng']
    global text2

    if(caozuo=='1'):
        m_name=request.form['ypmz']
        m_id=request.form['ypid']
        num=request.form['ypsl']
        year=request.form['nian']
        month=request.form['yue']
        day=request.form['ri']
        scdate=year+'-'+month+'-'+day
        loc=request.form['cfwz']
        price1=request.form['xsdj']
        bzq1=request.form['bzq']
        
        if(m_name!='' and m_id!='' and num!='' and year!='' and month!='' and day!='' and price1!='' and bzq!='' and loc!='' ):
            price=float(price1)
            bzq=int(bzq1)
            cursor.execute('select * from yaofangkucun where m_name=%s',m_name)
            dd=cursor.fetchone()
            if(dd==None):
                cursor.execute('insert into yaofangkucun values(%s,%s,%s,%s,%s,%s,%s)',(m_name,m_id,num,loc,scdate,bzq,price))
                conn.commit()
                text2="录入成功"
                return redirect(url_for('yaofangin'))
            else:
                listdd=list(dd)
                numfromlist=listdd[2]
                newnum=numfromlist+int(num)
                cursor.execute('update yaofangkucun set num=%s',newnum)
                conn.commit()
                text2="录入成功"
                return redirect(url_for('yaofangin'))
        else:
            text2='有输入为空，请重新输入'
            return redirect(url_for('yaofangin'))
    elif(caozuo=='2'):
        text2=""
        return redirect(url_for('yaofangmanager'))

    

@app.route('/quyaojilu',methods=['GET'])
def quyaojilu():
    global recorddq
    global recordcount
    global control2
    if(control2==0):
        cursor.execute('select * from getmedicinerecord')
        record=cursor.fetchall()
        list_record=list(record)
        list_lsls=[]
        list_record_final=[]
        for i in range(len(list_record)):
            m_name=list_record[i][0].encode('UTF-8')
            num=list_record[i][1]
            getdate=list_record[i][2]
            list_lsls.append(m_name)
            list_lsls.append(num)
            list_lsls.append(getdate)
            list_record_final.append(list_lsls)
            list_lsls=[]

        if(len(list_record_final)%15==0):
            pcount1=len(list_record_final)/15
        else:
            pcount1=len(list_record_final)/15+1

        recordcount=pcount1
        list_ls1=[]
        list_ls=[]

        for i in range(15*recorddq,(recorddq+1)*15):
            if(len(list_record_final)-1<i):
                break;
            list_ls1.append(list_record_final[i])
        list_ls=copy.deepcopy(list_ls1)
        list_ls1=[]
        dqpg=recorddq+1

        
        neirong={'qyxx':list_ls,'count':recordcount,'dq':dqpg,'text':text_for_qy}
        return render_template('quyaojilu.html',**neirong)
    elif(control2==1):
        if(len(list_for_rec)%15==0):
            pcount1=len(list_for_rec)/15
        else:
            pcount1=len(list_for_rec)/15+1

        recordcount=pcount1
        list_ls1=[]
        list_ls=[]

        for i in range(15*recorddq,(recorddq+1)*15):
            if(len(list_for_rec)-1<i):
                break;
            list_ls1.append(list_for_rec[i])
        list_ls=copy.deepcopy(list_ls1)
        list_ls1=[]
        dqpg=recorddq+1

             
        neirong={'qyxx':list_ls,'count':recordcount,'dq':dqpg,'text':text_for_qy}
        return render_template('quyaojilu.html',**neirong)

@app.route('/quyaojilu',methods=['POST'])
def quyaojilu1():
    caozuo=request.form['gongneng']
    global recorddq
    global recordcount
    global text_for_qy
    global control2
    global list_for_rec
    if(caozuo=='1'):
        if(recorddq==0):
            return redirect(url_for('quyaojilu'))
        else:
            recorddq=recorddq-1
            return redirect(url_for('quyaojilu'))
    elif(caozuo=='2'):
        if(recorddq>=(recordcount-1)):
            return redirect(url_for('quyaojilu'))
        else:
            recorddq=recorddq+1
            return redirect(url_for('quyaojilu'))
    elif(caozuo=='3'):
        text_for_qy=''
        return redirect(url_for('yaofangmanager'))
    elif(caozuo=='4'):
        recorddq=0
        control2=1
        year=request.form['nian']
        month=request.form['yue']
        day=request.form['ri']
        if(year!='' and month!='' and day!=''):
            sdate=year+'-'+month+'-'+day
            cursor.execute('select * from getmedicinerecord where gettime=%s',sdate)
            re=cursor.fetchall()
            print(re)
            if(re!=[]):
                list_re=list(re)
                list_ls2=[]
                for i in range(len(list_re)):
                    m_name=list_re[i][0].encode('UTF-8')
                    name=m_name.strip()
                    num=list_re[i][1]
                    time=list_re[i][2]
                    list_ls2.append(name)
                    list_ls2.append(num)
                    list_ls2.append(time)
                    list_for_rec.append(list_ls2)
                    list_ls2=[]
                text_for_qy='查询成功'
                return redirect(url_for('quyaojilu'))
            else:
                control2=0
                text_for_qy='没有此日期的数据'
                return redirect(url_for('quyaojilu'))

        else:
            control2=0
            text_for_qy='有输入为空，请重新输入'
            return redirect(url_for('quyaojilu'))
    elif(caozuo=='5'):
        control2=0
        text_for_qy=''
        return redirect(url_for('quyaojilu'))




@app.route('/login_for_yaofang',methods=['GET'])#药房取药和出库操作
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
    elif(caozuo=='6'):
        m_name=request.form['yaopinname']
        num=request.form['yaopinnum']
        year=request.form['year']
        month=request.form['month']
        day=request.form['day']
        date=year+'-'+month+'-'+day
        cursor.execute('insert into getmedicinerecord values(%s,%s,%s)',(m_name,num,date))
        conn.commit()
        cursor.execute('select * from yaofangkucun where m_name=%s',m_name)
        xxz=cursor.fetchone()
        list_xxz=[]
        list_xxz=list(xxz)
        num_yl=list_xxz[2]
        num_hl=num_yl-int(num)
        cursor.execute('update yaofangkucun set num=%s where m_name=%s',(num_hl,m_name))
        conn.commit()
        return redirect(url_for('login_for_yaofang'))
    elif(caozuo=='7'):
        return redirect(url_for('yaofangmanager'))


@app.route('/wrong')#登录失败
def wrong():
    return "<a>hhhh</a>"
        

if __name__=='__main__':
    
    app.run()