from flask import Flask, request, redirect, render_template, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False


@app.route('/', methods=['GET'])
def index():
    blogs = Blog.query.all()
    return render_template("blog.html",blogs=blogs, title='title')

app.route('/new-post', methods=['POST','GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['body']
        new_blog = Blog(blog_title, blog_content)

        if new_blog.is_valid():
            db.session.add(new_blog)
            db.session.commit()
            url = "/single_template?id=" + str(new_blog.id)
            return redirect(url)

        else:
            flash("Entries needed in both fields!")

            return render_template('new-post.html',category="error",
                                    blog_title = blog_title, blog_content  = blog_content)


    else:
        return render_template('new-post.html')


@app.route('/single-post', methods=['GET'])
def show_post():
    blog_id = request.args.get('id')
    blogs = Blog.query.filter_by(id=blog_id).first()

    return render_template('single-post.html', blogs=blogs)


@app.route('/blog', methods=['GET'])
def get_posts():
    return redirect('/')




if __name__ == "__main__":
    app.run()