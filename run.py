#-*-coding:utf-8-*-
from flask import Flask, g, flash, redirect, url_for
from flask import render_template
from flask import request,session
from server import login_server,register_server,score_server,recommend_server
from server import score_detail,auth_server,back_view
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = '0104*132*440_lu*ozx=8*52@394&27-ala^rk'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/background/')
def background():
    if 'user_id' in session:
        auth=auth_server(session['user_id'])
        if auth[0]:
            users=back_view()
            return render_template('background.html',users=users)
        else:
            flash('您没有权限访问此页')
            return redirect(url_for('index'))
    else:
        flash('请先登陆')
        return redirect(url_for('login'))

@app.route('/score/')
def score():
    if 'user_id' in session:
        data=score_server(session['user_id'])
        if data[1] and data[1]!=0:
            res=score_detail(session['user_id'])
            return render_template('score.html',real_score=data[0],
                                   virtual_score=data[1],res=res)
        return render_template('score.html',real_score=data[0],\
                               virtual_score=data[1])
    else:
        flash('请先登陆')
        return redirect(url_for('login'))

@app.route('/recommend/',methods=['POST','GET'])
def recommend():
    if 'user_id' in session:
        if request.method=='POST':
            data=recommend_server(session['user_id'],**request.form)
            flash(data)
            return redirect(url_for('score'))
        return render_template('recommend.html')
    else:
        flash('请先登陆')
        return redirect(url_for('login'))

@app.route('/register/',methods=['POST','GET'])
def register():
    if request.method=='POST':
        data=register_server(**request.form)
        flash(data)
        if data=="注册成功":
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login/',methods=['POST','GET'])
def login():
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
            flash('登陆成功')
            return redirect(url_for('score'))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('user_id',None)
    flash('登出成功')
    return render_template('layout.html')


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
