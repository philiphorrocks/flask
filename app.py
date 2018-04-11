from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relation, sessionmaker
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
DateTime='date'

class group(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(80))
    group_date = db.Column(db.Integer)
    group_host = db.Column(db.String(80))

    def __init__(self, group_name=None, group_date=None, group_host=None):
        self.group_name = group_name
        self.group_date = group_date
        self.group_host = group_host


class groupSchema(ma.Schema):
    class Meta:
        fields = ('group_name', 'group_date', 'group_host')

group_schema = groupSchema()
groups_schema = groupSchema(many=True)


# endpoint to create new user
@app.route("/add", methods=["POST"])

def add_group():

    g = request.json['group_name']
    d = request.json['group_date']
    h = request.json['group_host']

    new_group = group(g, d, h)

    db.session.add(new_group)
    db.session.commit()

    return jsonify(new_group)


# endpoint to show all groups
@app.route("/groups", methods=["GET"])
def get_groups():
    all_groups = group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/groups/<string:name>", methods=["GET"])
def group_detail(name):
    print(name)
    groups = group.query.filter_by(group_name=name)
    return groups_schema.jsonify(groups)


# endpoint to update user
@app.route("/groups/<id>", methods=["PUT"])
def group_update(id):
    group = group.query.get(id)
    host = request.json['host']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/groups/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(group_name)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
