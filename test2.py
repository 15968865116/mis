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
text_for_qy=''
control2=0
recorddq=0
recordcount=0
yaodan=0
yaodancount=0
text2=''
allcount=0
control=0
control1=0
list_for_yd=[]
list_for_chaxun=[]
j=0
k=0
yaofangdq=0
wwc_count=0
ywc_count=0 
text=''
text_for_upload=''
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
    elif(num=='4'):
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
    return render_template('cangku_jinhuo.html')

@app.route('/cangku_chuhuo',methods=['GET'])#仓库出货情况查询
def cangku_chuhuo():
    return render_template('cangku_chuhuo.html')

@app.route('/cangku_search',methods=['GET'])#仓库全部查询
def cangku_search():
    return render_template('cangku_search.html')

@app.route('/cangku_jinchu',methods=['GET'])#仓库进出登记
def cangku_jinchu():
    return render_template('cangku_jinchu.html')

@app.route('/yaofangmanager',methods=['GET'])
def yaofangmanager():

    name={'a':session['xingming']}
    return render_template('yaofangcaozuo.html',**name)

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