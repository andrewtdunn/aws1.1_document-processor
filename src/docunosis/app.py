from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import boto3
from boto3.dynamodb.conditions import Key
import uuid
import datetime
import os
import secrets
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,validators
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_login import LoginManager

from user import DocunosisUser
load_dotenv() # This loads the variables from .env


app = Flask(__name__)
bcrypt = Bcrypt(app)



app.secret_key = secrets.token_hex()
login_manager = LoginManager()
login_manager.init_app(app)

BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['DOCUMENTS_TABLE_NAME']
USERS_TABLE_NAME = os.environ['USERS_TABLE_NAME']


# AWS DynamoDB Setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)
users_table = dynamodb.Table(USERS_TABLE_NAME)
bucket = boto3.resource('s3')

class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])


@login_manager.user_loader
def load_user(user_id):
    response = users_table.query(KeyConditionExpression=Key('username').eq(user_id))
    if response['Count'] == 0:
        return None
    user_data = response['Items'][0]
    return DocunosisUser(user_data['username'], user_data['email'], user_data['password'])

@app.route("/healthy", methods=["GET"])
def healthy():
    return jsonify({"status": "OK"}), 200

@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = DocunosisUser.get(form.username.data)
        if user is None:
            return render_template('login.html', form=form, login_error="user not found")
        is_valid = bcrypt.check_password_hash(user.password, form.password.data)
        if user and is_valid: 
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else: 
           render_template('login.html', form=form, login_error="wrong password")     
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("signup")
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = UserForm()
    if form.validate_on_submit():
        print("validated")

        # Login and validate the user.
        # user should be an instance of your `User` class
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = DocunosisUser.create(form.username.data,form.email.data, hashed_password)
        login_user(user, form.username.data)
        
        flash('Signed Up successfully.')

        return redirect(url_for('index'))
    else: 
      print("not validated")
      print(form.errors)
    return render_template('signup.html', form=form)


@app.route('/')
@login_required
def index():
  # Get all blog posts from DynamoDB
  response = table.scan()
  blog_posts = response['Items']
  # Sort blog posts by date (newest first)
  blog_posts.sort(key=lambda x: x['date'], reverse=True)
  
  return render_template('index.html', posts=blog_posts, username=current_user.username)

@app.route('/post/<id>')
@login_required
def post(id):
  response = table.query(
      KeyConditionExpression=Key('doc_id').eq(id)
  )
  return render_template('post.html', post=response['Items'][0])

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
      doc_id = str(uuid.uuid4())  
      title = request.form['title']
      content = request.form['content']
      author = request.form.get('author', 'Anonymous')
      tags = request.form['tags']
      date = datetime.datetime.now().isoformat()

      file = request.files['blog-image']
      filename = secure_filename(file.filename)

      if (filename):
        s3 = boto3.client('s3')
        try: 
          s3.upload_fileobj(file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
        except Exception as e:
              return str(e), 500

      post_image = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}" if filename else ""

      # Add post to DynamoDB
      table.put_item(
          Item={
              'doc_id': doc_id,
              'title': title,
              'content': content,
              'author': author,
              'date': date,
              'status': "published",
              'tags': tags,
              "post_image": post_image
          }
      )

      # Redirect to the new post
      return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)