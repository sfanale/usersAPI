from flask import Flask, render_template,jsonify, request
import flask
import connexion
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
import users_api
import jwt as JWT


def decode_token(token):
    ret = JWT.decode(token, '69', algorithms=['HS256'])
    print(ret)
    return ret


# create application instance
myapp = connexion.App(__name__, specification_dir="./")
myapp.app.config['JWT_SECRET_KEY'] = '69'
  # Change this!
jwt = JWTManager(myapp.app)
# read swagger.yml to configure endpoints
myapp.add_api('swagger.yml')

# add CORS support
CORS(myapp.app)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'user_id': user.id}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username




@myapp.route('/')
def home():
    """
            This function just responds to the browser ULR
            localhost:5000/

            :return:        the rendered template 'home.html'
            """
    return render_template("home.html")



# if we are running in stand alone mode, run the application
if __name__ == '__main__':
    myapp.run(host='0.0.0.0', port=5000, debug=True)
