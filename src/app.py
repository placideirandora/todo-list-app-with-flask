from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    completed = db.Column(db.Boolean, default=False)

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
        # db.session.query(Todo).delete()
        # db.session.commit()
        todos = Todo.query.all()
        return render_template('index.html', todos=todos)


@app.route('/complete/<int:id>')
def complete_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = True

    try:
        db.session.commit()
        return redirect('/')

    except:
        return 'Error: the todo completion failed.'


if __name__ == '__main__':
    app.run(debug=True)



