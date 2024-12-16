from flask import Flask, render_template, request, redirect
# render_template is used to render our html page which is in template and shows on browser

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)




# SQLALCHEMY_DATABASE_URI. The database connection URI used for the default engine. It can be either a string or a SQLAlchemy URL instance
# SQLite, relative to Flask instance path -> sqlite:///project.db
# PostgreSQL -> postgresql://scott:tiger@localhost/project
# MySQL / MariaDB -> mysql://scott:tiger@localhost/project
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str: # when we print object of this class it will only return the following
        return f"{self.sno} - {self.title}"




# it runs on port 127.0.0.1:8000 
# @app.route("/")
# def hello_world():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return "<p>Hello, World!</p>"







@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        
        scheduled_time_str = request.form['scheduled_time']
        
        if scheduled_time_str:
            # Parsing the datetime string properly
            try:
                scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
                todo.scheduled_time = scheduled_time
            except ValueError:
                # If the datetime format is invalid, keep the original value
                todo.scheduled_time = todo.scheduled_time
        else:
            # If no scheduled time is provided, set it to None
            todo.scheduled_time = None
        
        db.session.commit()
        return redirect("/")
    
    return render_template("update.html", todo=todo)








# it is for delete
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")






@app.route("/", methods=["GET", "POST"])
def tem():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        scheduled_time_str = request.form['scheduled_time']  # User input

        # If the user provides a scheduled time, parse it
        if scheduled_time_str:
            scheduled_time_str = scheduled_time_str.replace('T', ' ')  # Replace 'T' with space
            scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%d %H:%M')
        else:
            scheduled_time = None  # No scheduled time, so set to None

        # Create the Todo item with the current UTC time and optional scheduled time
        todo = Todo(title=title, desc=desc, scheduled_time=scheduled_time)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    # it is through jinja2 that we are able to see allodo and in render_template also







# after we add /Friends to our port it will run 127.0.0.1:8000/Friends
@app.route("/Friends")
def friends():
    return "Rajnish Loves Chandini"







# without the below lines if we run code will not output anything
# with these lines included it will do as i coded
if __name__ == "__main__":
    #app.run(debug=True) # if any error show in debug terminal
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000) # if we want to run on port 8000






# if i want to see files which are in static and download then we just need to add that name to our port
# 127.0.0.0.1:8000/static/chandu.txt