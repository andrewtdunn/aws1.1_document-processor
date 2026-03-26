from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import boto3
from boto3.dynamodb.conditions import Key
import uuid
import datetime
import os
import secrets
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import StringField
from wtforms.validators import DataRequired

from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_login import LoginManager
load_dotenv() # This loads the variables from .env


app = Flask(__name__)


app.secret_key = secrets.token_hex()
login_manager = LoginManager()
login_manager.init_app(app)

BUCKET_NAME = "datajammers-blog-images"
TABLE_NAME = "BlogPosts"

# AWS DynamoDB Setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Signed Up successfully.')

        next = flask.request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return render_template('signup.html')


@app.route('/')
@login_required
def index():
  # Get all blog posts from DynamoDB
  response = table.scan()
  print(response)
  blog_posts = response['Items']
  # Sort blog posts by date (newest first)
  blog_posts.sort(key=lambda x: x['date'], reverse=True)
  
  return render_template('index.html', posts=blog_posts)

@app.route('/post/<id>')
@login_required
def post(id):
  response = table.query(
      KeyConditionExpression=Key('post_id').eq(id)
  )
  return render_template('post.html', post=response['Items'][0])

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
      post_id = str(uuid.uuid4())  
      title = request.form['title']
      content = request.form['content']
      author = request.form.get('author', 'Anonymous')
      tags = request.form['tags']
      date = datetime.datetime.now().isoformat()

      file = request.files['blog-image']
      filename = secure_filename(file.filename)

      if (filename):
        s3 = boto3.client('s3',aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
        try: 
          s3.upload_fileobj(file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
        except Exception as e:
              return str(e), 500

      post_image = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}" if filename else ""

      # Add post to DynamoDB
      table.put_item(
          Item={
              'post_id': post_id,
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
    return redirect(somewhere)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)