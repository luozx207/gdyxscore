#-*-coding:utf-8-*-
from flask import Flask, g, flash, redirect, url_for,jsonify
from flask import render_template
from flask import request,session
from server import login_server,register_server,score_server,recommend_server
from server import score_detail,auth_server,all_user_s, pre_server,all_pre_s
from server import zero_server
from server import get_user_question,update_user_question
import background

app=Flask(__name__)
app.register_blueprint(background.bp, url_prefix='/background/')
app.config['SECRET_KEY'] = '0104*132*440_lu*ozx=8*52@394&27-ala^rk'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/pre_re/',methods=['POST','GET'])
def pre_re():
    if request.method=='POST':
        data=pre_server(**request.form)
        flash(data)
        if data=="预报名成功":
            return redirect(url_for('index'))
        else:
            return redirect(url_for('pre_re'))
    return render_template('pre_re.html')

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

@app.route('/question/<user_id>',methods=['GET','POST'])
def question(user_id):
    if request.method=='POST':
        try:
            update_user_question(**request.form)
        except Exception as e:
            return e
        return jsonify('seccess')

    question_id,data,undone = get_user_question(user_id)
    return jsonify({'questionId':question_id,
                    'title':data[0],
                    'options':[data[1],data[2],data[3],data[4]],
                    'attributes':{
                        'questionID':question_id,
                        'answer':data[6],
                        'answerExplain':data[5],
                        },
                    'totalQuestionNumber':undone,
                    })


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
    session.pop('auth',None)
    session.pop('user_id',None)
    flash('登出成功')
    return render_template('layout.html')


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
