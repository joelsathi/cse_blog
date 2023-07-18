from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Pass the file name, __name__ indicates the this current file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Blog post {self.id}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form["author"]
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
        return redirect("/posts")
    else:
        with app.app_context():
            all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html", posts=all_posts)


@app.route("/posts/delete/<int:id>")
def delete(id):
    with app.app_context():
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect("/posts")

@app.route("/posts/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        print("Posting to the database")
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form["author"]
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# Set it up in the debug mode as a good practice, so that you can run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
