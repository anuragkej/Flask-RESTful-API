from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)

# wrap app in a RESTful API
api = Api(app)

# Parses through request and ensures it fits the request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the video is required", required=True
)

videos = {}


def abort_id_DNE(video_id):
    if video_id not in videos:
        abort(404, message="Video ID is not valid...")


def abort_video_exists(video_id):
    if video_id in videos:
        abort(409, message="This video already exists with that ID...")


class Video(Resource):
    def get(self, video_id):
        abort_id_DNE(video_id)
        return videos[video_id]

    # create new video
    def put(self, video_id):
        abort_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201  # 'created' status code

    def delete(self, video_id):
        abort_id_DNE(video_id)
        del videos[video_id]
        return "", 204


# string video_id parameter to be passed in after /video/
api.add_resource(Video, "/video/<int:video_id>")
if __name__ == "__main__":
    app.run(debug=True)
