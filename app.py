from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
DateTime='date'

class group(db.Model):

    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, unique=True)
    group = db.Column(db.String(80), unique=True)

# Generate marshmallow Schemas from models using ModelSchema
    def __init__(self, group):
            self.group = group



class groupSchema(ma.Schema):
    class Meta:
        fields = ('group', 'date')

group_schema = groupSchema()
groups_schema = groupSchema(many=True)


class variables(db.Model):

    __tablename__ = 'variables'

    id = db.Column(db.Integer, primary_key=True)
    vars = db.Column(db.String(80), unique=True)
    host = db.Column(db.String(80), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('group', backref='groups')


# Generate marshmallow Schemas from models using ModelSchema

class variablesSchema(ma.Schema):
    class Meta:
        fields = ('group', 'host', 'vars')

variable_schema = variablesSchema()
variables_schema = variablesSchema(many=True)




# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


# endpoint to show all groups
@app.route("/groups", methods=["GET"])
def get_groups():
    all_groups = group.query.all()
    result = group_schema.dump(all_groups)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/groups/<id>", methods=["GET"])
def group_detail(id):
    groups = group.query.get(id)
    return group_schema.jsonify(groups)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
