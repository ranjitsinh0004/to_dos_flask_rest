from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

todos = {
    1: {'task': 'Learn Flask Rest', 'summary': 'Flask Restful, HTTP Methods'},
    2: {'task': 'Learn Frontend', 'summary': 'HTML, CSS, Javascript'}
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='This is required', required=True)
task_post_args.add_argument('summary', type=str, help='This is required', required=True)


class TodoList(Resource):
    def get(self):
        return todos


class Todo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        args = task_post_args.parse_args()
        if todo_id in todos:
            abort(409, description='ToDo id already exists.')
        todos[todo_id] = {
            'task': args['task'],
            'summary': args['summary']
        }
        return todos


api.add_resource(TodoList, "/todos")
api.add_resource(Todo, "/todos/<int:todo_id>")

if __name__ == '__main__':
    app.run(debug=True)
