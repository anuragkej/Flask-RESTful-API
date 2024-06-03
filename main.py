from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

#wrap app in a RESTful API
api = Api(app)

#inherit Resource to handle GET, PUT, etc.
class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World"}
    
api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True)
    
