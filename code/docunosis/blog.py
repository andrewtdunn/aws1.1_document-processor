from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)

import boto3
import os

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from docunosis.auth import login_required
from docunosis.db import get_db

bp = Blueprint('blog', __name__)

@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, imgfile, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

def get_post(id, check_author=True):
  post = get_db().execute(
    'SELECT p.id, title, body created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()

  if post is None:
    abort(404, "Post id {0} doesn't exist.".format(id))

  if check_author and post['author_id'] != g.user['id']:
    abort(403)

  return post

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        print(request.form)
        print(request.files)
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)

        load_dotenv()

        s3 = boto3.client(
          "s3",
          aws_access_key_id=os.getenv("AWS_KEY"),
          aws_secret_access_key=os.getenv("AWS_SECRET")
        )

        BUCKET_NAME = "datajammers-upload-forms"

        file = request.files['user_file']
        filename = secure_filename(file.filename)

        if filename:

          print("file detected")
          print(filename)
          
          try:
              s3.upload_fileobj(
                  file,
                  BUCKET_NAME,
                  filename,
                  ExtraArgs={
                      "ContentType": file.content_type  # Essential for viewing images in browser
                  }
              )
              print("saving - file")
              print(filename)
              db = get_db()
              db.execute(
                  "INSERT INTO post (title, body, imgfile, author_id) VALUES (?, ?, ?, ?)",
                  (title, body, filename, g.user["id"]),
              )
              print(db.commit())
              return redirect(url_for('blog.index'))
              
          except Exception as e:
              return str(e), 500
        
        else:
            print("saving - no file")
            db = get_db()
            
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template("blog/create.html")

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, id)
      )
      db.commit()
      return redirect(url_for('blog.index'))

  return render_template('blog/update.html', post=post)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))