from flask import Flask, request, redirect, render_template, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fNLjA7Y7V4EzM1'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    

@app.route('/blog', methods=['POST', 'GET'])
def index():
    blog_id=request.args.get('id')
    if blog_id == None:
        new_post = Blog.query.all()
        return render_template('blog.html',title="Add a Blog Entry", new_post=new_post)
    else: 
        blog_entry=Blog.query.get(blog_id)
        return render_template('single-post.html', blog_entry=blog_entry)
  

@app.route('/newpost', methods=['POST','GET'])
def new_post(): 
    


    if request.method == "GET":
        return render_template('new-post.html')
        
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['body']
        new_blog = Blog(blog_title, blog_content)

       

        if len(blog_title) is 0 or len(blog_content) is 0:
            flash("Blog title and content must be filled!", 'error')    
            return render_template("new-post.html", blog_title=blog_title, blog_content=blog_content)

        else: 
            db.session.add(new_blog)
            db.session.commit()
            url = "/blog?id=" + str(new_blog.id)
            return redirect(url)
            
            

@app.route('/single', methods=['POST'])
def show_post():
    blog_id=request.args.get('id')
    if request.method == "POST":
        redirect('./blog?id={{Blog.id}}')


if __name__ == "__main__":
    app.run()