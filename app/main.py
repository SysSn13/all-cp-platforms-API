from flask import Flask,render_template
from flask_restful import Resource,Api
from app.helper import User, UsernameError,PlatformError
app = Flask(__name__)
api = Api(app)


# @app.route("/")
# def index():
#     return "this in the index page"

class UserDetails(Resource):
    def get(self,username,platform):
        user = User(username,platform)
        try:
            return user.get_info()
        except UsernameError:
            return {'status':'failed','details':'Invalid username'}
        except PlatformError:
            return {'status':'failed','details':'Invalid platform'}


api.add_resource(UserDetails,'/api/<string:platform>/<string:username>')

if __name__== "__main__":
    app.run(debug=True)
