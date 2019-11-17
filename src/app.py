from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        todo = request.form['content']
        new_todo = Todo(content=todo)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'Error: the todo could not be added.'

    else:
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todos = todos)


if __name__ == '__main__':
    app.run(debug=True)



