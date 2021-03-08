from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))


# db.create_all()  # once the database file i.e sqlite.db is created just comment this line


task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='This is required', required=True)
task_post_args.add_argument('summary', type=str, help='This is required', required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument('task', type=str)
task_put_args.add_argument('summary', type=str)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String,
}


class TodoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task, "summary": task.summary}
        return todos


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(404, description='Could not find task with that id.')
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        # import ipdb; ipdb.set_trace()
        args = task_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()

        if task:
            abort(409, description='ToDo id already exists.')
        todo = ToDoModel(id=todo_id, task=args['task'], summary=args['summary'])

        db.session.add(todo)
        db.session.commit()

        return todo, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()

        if not task:
            abort(404, message='task does not exist, can not update')
        if args['task']:
            task.task = args['task']
        if args['summary']:
            task.summary= args['summary']

        db.session.commit()
        return task

    def delete(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()

        if not task:
            abort(404, message='task does not exist, can not be deleted')
        db.session.delete(task)
        db.session.commit()
        return f'task with id {task.id} is deleted', task.id


api.add_resource(TodoList, "/todos")
api.add_resource(Todo, "/todos/<int:todo_id>")

if __name__ == '__main__':
    app.run(debug=True)
