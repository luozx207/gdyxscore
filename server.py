import sqlite3
import re
import datetime
def login_server(username=None,password=None):
   conn = sqlite3.connect('test.sqlite')
   cursor = conn.cursor()
   cursor.execute('select * from user where username=? and password=?',(username,password))
   data=cursor.fetchall()
   conn.close()
   if data:
       return data[0]
   else:
       return '账号或密码错误'

def register_server(**data):
   conn = sqlite3.connect('test.sqlite')
   cursor = conn.cursor()
   reg= re.compile(r'^1[34578][0-9]{9}$')
   if not reg.match(data['telephone'][0]):
       return "请填写正确的手机号码"
   try:
       cursor.execute('insert into user (username,password,createtime,name,\
                      telephone,QQ,email)values(?,?,?,?,?,?,?)',\
                      (data['username'][0],data['password'][0],\
                       datetime.date.today(),data['name'][0],\
                       data['telephone'][0],data['QQ'][0],data['email'][0]))
   except sqlite3.IntegrityError:
       conn.close()
       return "用户名重复"
   conn.commit()
   conn.close()
   return "注册成功"

def pre_server(**data):
   conn = sqlite3.connect('test.sqlite')
   cursor = conn.cursor()
   reg= re.compile(r'^1[34578][0-9]{9}$')
   if not reg.match(data['telephone'][0]):
       return "请填写正确的手机号码"
   try:
       cursor.execute('insert into pre (name,telephone,createtime,\
                      QQ,email)values(?,?,?,?,?)',\
                      (data['name'][0],data['telephone'][0],\
                       datetime.date.today(),data['QQ'][0],\
                       data['email'][0]))
   except sqlite3.IntegrityError:
       conn.close()
       return "手机号码重复"
   conn.commit()
   conn.close()
   return "预报名成功"

def score_server(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select real_score,virtual_score from user where id=?',(user_id,))
    data=cursor.fetchall()
    conn.close()
    return data[0]

def score_detail(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select createtime,name,telephone,status,id\
                   from re where user_id=?',(user_id,))
    data=cursor.fetchall()
    conn.close()
    return data

def recommend_server(user_id,**data):
   conn = sqlite3.connect('test.sqlite')
   cursor = conn.cursor()
   reg= re.compile(r'^1[34578][0-9]{9}$')
   if not reg.match(data['re_telephone'][0]):
       return "请填写正确的手机号码"
   try:
       cursor.execute('insert into re (createtime,name,telephone,email,\
                      user_id)values(?,?,?,?,?)',\
                      (datetime.date.today(),data['re_name'][0],data['re_telephone'][0],\
                       data['re_email'][0],user_id))
   except sqlite3.IntegrityError:
       conn.close()
       return "此人已被推荐"
   conn.commit()
   cursor.execute('update user set virtual_score=virtual_score+150 where id=?',\
                  (user_id,))
   conn.commit()
   conn.close()
   return "恭喜获得150个推荐积分！"

def auth_server(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select role from user where id=?',(user_id,))
    data=cursor.fetchall()
    conn.close()
    return data[0]

def all_user_s():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select createtime,name,telephone,real_score,\
                   virtual_score,id from user where role=0')
    data=cursor.fetchall()
    conn.close()
    return data

def all_pre_s():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select createtime,name,telephone,QQ,\
                   email from pre')
    data=cursor.fetchall()
    conn.close()
    return data

def zero_server(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('update user set virtual_score=0 ,real_score=0 where id=?',\
                   (user_id,))
    cursor.execute('delete from re where user_id=?',(user_id,))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select name,telephone,QQ,email from user where id=?',\
                   (user_id,))
    data=cursor.fetchall()
    conn.close()
    return data[0]

def get_userid_by_re(re_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select user_id from re where id=?',(re_id,))
    data=cursor.fetchall()
    conn.close()
    return data[0]

def change_status_server(re_id,user_id,status,s):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('update re set status=? where id=?',(s,re_id))
    if status==1:
        cursor.execute('update user set virtual_score=virtual_score-50,\
                         real_score=real_score+50 where id=?',(user_id,))
    if status==2:
        cursor.execute('update user set virtual_score=virtual_score-100,\
                         real_score=real_score+100 where id=?',(user_id,))
    conn.commit()
    conn.close()
