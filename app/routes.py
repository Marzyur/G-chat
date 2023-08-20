import datetime
from io import BytesIO
from flask import render_template,flash,redirect,request, send_file,url_for,session,jsonify
from flask_login import login_required,current_user
from app import app,db
from app.models import UserInput,ChatResponse,User,ImageRequest
from app.chatbot import generate_response,generate_image
from app.forms import UserInputForm
import json

@app.route('/')
def index():
    return render_template('base.html',current_user=current_user)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user=User.create_user(username,email,password)
        if user:
            flash("creating User")
            return redirect(url_for('home'))
        else:
            flash("Error creating User")
    return render_template('signup.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id']=user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/home',methods=['GET','POST'])
def home():
    form=UserInputForm()
    if form.validate_on_submit():
        user_input=UserInput(text=form.text.data)
        db.session.add(user_input)
        db.session.commit()
        chat_response=ChatResponse(text=generate_response(user_input.text))
        db.session.add(chat_response)
        db.session.commit()
        return redirect(url_for('home'))
    user_inputs=UserInput.query.order_by(UserInput.created_at.desc()).limit(10)
    chat_responses=ChatResponse.query.order_by(ChatResponse.created_at.desc()).limit(10)
    return render_template('home.html',form=form,user_inputs=user_inputs,chat_responses=chat_responses)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = UserInput(text=request.form['user_input'])
    db.session.add(user_input)
    db.session.commit()
    chat_response = ChatResponse(text=generate_response(user_input.text))
    db.session.add(chat_response)
    db.session.commit()
    return redirect(url_for('home'))


    

@app.route('/chat-response',methods=['GET','POST'])
# @login_required
def chat_response():
    chat_responses=ChatResponse.query.order_by(ChatResponse.created_at.desc()).limit(10)
    return render_template('chat_response.html',chat_responses=chat_responses)

@app.route('/image')
def Dalle():
    return render_template("index.html")

@app.route('/generate_image',methods=['GET','POST'])
def generate_image_route():
    prompt=request.form["prompt"]
    image_url=generate_image(prompt)
    image_request=ImageRequest(prompt=prompt,image_url=json.dumps(image_url),created_at=datetime.datetime.utcnow())
    # print(image_url)
    db.session.add(image_request)
    db.session.commit()
    return jsonify({"image url:":image_url})
    

