from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# wrap app in a RESTful API
api = Api(app)

# config a database and where to access it at a relative path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    # unique id
    id = db.Column(db.Integer, primary_key=True)
    # video always has a name
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views = {views}, likes={likes})"


# db.create_all()


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

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes of the video is required")

# def abort_id_DNE(video_id):
#     if video_id not in videos:
#         abort(404, message="Video ID is not valid...")


# def abort_video_exists(video_id):
#     if video_id in videos:
#         abort(409, message="This video already exists with that ID...")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    # decorator to serialize
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_id_DNE(video_id)

        result = VideoModel.query.filter_by(id=video_id).first()
        # error handling for video ID
        if not result:
            abort(404, message="Can not find video with that ID.")
        return result

    # create new video
    @marshal_with(resource_fields)
    def put(self, video_id):
        # abort_video_exists(video_id)
        # args = video_put_args.parse_args()
        # videos[video_id] = args
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        # send a query to see if the video_id is taken
        if result:
            abort(409, message="Video ID taken...")
        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        # adds to current database session
        db.session.add(video)
        # permanently put to database
        db.session.commit()
        return video, 201  # 'created' status code

    # update
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        # update process
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()
        return result

    def delete(self, video_id):
        abort_id_DNE(video_id)
        del videos[video_id]
        return "", 204


# string video_id parameter to be passed in after /video/
api.add_resource(Video, "/video/<int:video_id>")
if __name__ == "__main__":
    app.run(debug=True)
