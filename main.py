from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

# wrap app in a RESTful API
api = Api(app)

videos = {}


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create new video
    def put(self, video_id):
        print(request.form)
        return {}


# string name parameter to be passed in after helloworld
api.add_resource(Video, "/video/<int:video_id>")
if __name__ == "__main__":
    app.run(debug=True)
