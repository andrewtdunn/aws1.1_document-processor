from flask import Flask, render_template, request, redirect, url_for
import boto3
from boto3.dynamodb.conditions import Key
import uuid
import datetime
import os

from dotenv import load_dotenv
from werkzeug.utils import secure_filename
load_dotenv() # This loads the variables from .env

app = Flask(__name__)

BUCKET_NAME = "datajammers-blog-images"
TABLE_NAME = "BlogPosts"

# AWS DynamoDB Setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

@app.route("/healthy", methods=["GET"])
def healthy():
    return jsonify({"status": "OK"}), 200

@app.route('/')
def index():
  # Get all blog posts from DynamoDB
  response = table.scan()
  print(response)
  blog_posts = response['Items']
  # Sort blog posts by date (newest first)
  blog_posts.sort(key=lambda x: x['date'], reverse=True)
  
  return render_template('index.html', posts=blog_posts)

@app.route('/post/<id>')
def post(id):
  response = table.query(
      KeyConditionExpression=Key('post_id').eq(id)
  )
  return render_template('post.html', post=response['Items'][0])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
      # Generate a unique ID for the post
      post_id = str(uuid.uuid4())  
      # Get form data
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

if __name__ == '__main__':
    app.run(debug=False)