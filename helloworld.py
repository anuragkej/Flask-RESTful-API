from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

# wrap app in a RESTful API
api = Api(app)

names = {
    "Anurag": {"age": 18, "gender": "male"},
    "Batman": {"age": 43, "gender": "male"},
}


# inherit Resource to handle GET, PUT, etc.
class HelloWorld(Resource):
    def get(self, name):
        return names[name]

    def post(self):
        return {"data": "Posted"}


# string name parameter to be passed in after helloworld
api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
