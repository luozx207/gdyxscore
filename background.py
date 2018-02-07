#-*-coding:utf-8-*-
from flask import Blueprint
from flask import Flask, g, flash, redirect, url_for
from flask import render_template
from flask import request,session
from server import login_server
from server import score_detail,auth_server,all_user_s, pre_server,all_pre_s
from server import zero_server,get_user_by_id, change_status_server
from server import get_userid_by_re
from functools import wraps

def auth_func(func):
    @wraps(func)
#This ensures that metadata such as the function name is copied over from
#func to the wrapper
    def wrapper(*args,**kwargs):
        if 'auth' in session and session['auth']:
            return func(*args,**kwargs)
        else:
            flash('您没有权限访问后台')
            return redirect(url_for('index'))
    return wrapper
#You need to ensure your decorator wrapper has the same name as the
#wrapped view function, otherwise all your views look like the same endpoint

bp = Blueprint('background', __name__)

@bp.route('',methods=['POST','GET'])
def background():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        data=login_server(username,password)
        if 'user_id' in session:
            flash('请勿重复登录')
        elif type(data)==str:
            flash(data)
        else:
            session['user_id']=data[0]
            auth=auth_server(session['user_id'])
            session['auth']=auth[0]
            if not auth[0]:
                flash('您没有权限访问后台')
                return redirect(url_for('index'))
            flash('登陆成功')
    return render_template('background.html')

@bp.route('all_user/')
@auth_func
def all_user():
    users=all_user_s()
    return render_template('all_user.html',users=users)

@bp.route('all_pre/')
@auth_func
def all_pre():
    pres=all_pre_s()
    return render_template('all_pre.html',pres=pres)

@bp.route('zero/<id>')
@auth_func
def zero(id):
    zero_server(id)
    flash('成功清零')
    return redirect(url_for('background.all_user'))

@bp.route('detail/<id>')
@auth_func
def detail(id):
    user=get_user_by_id(id)
    data=score_detail(id)
    return render_template('detail.html',data=data,user=user)

@bp.route('change_status1/<id>')
@auth_func
def change_status1(id):
    user=get_userid_by_re(id)
    change_status_server(id,user[0],1,"参加入学考试")
    return redirect(f'background/detail/{user[0]}')

@bp.route('change_status2/<id>')
@auth_func
def change_status2(id):
    user=get_userid_by_re(id)
    change_status_server(id,user[0],2,"已缴纳学费")
    return redirect(f'background/detail/{user[0]}')
