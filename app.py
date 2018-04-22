# Ptyhon Resfful API - Annsible compatible 
#  v .04 - Phil H

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relation, sessionmaker
from flask_marshmallow import Marshmallow
import datetime
import os

DateTime='date'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.sqlite')

# create an instances of our web application and set path of our SQLite uri
db = SQLAlchemy(app)
ma = Marshmallow(app)

# define a model called group
class group(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(80))
    group_date = db.Column(db.DateTime, default=datetime.datetime.now())
    group_host = db.Column(db.String(80))

    def __init__(self, group_name=None, group_host=None, group_date=None):
        self.group_name = group_name
        self.group_date = group_date
        self.group_host = group_host

# Generate marshmallow Schemas from your model
class groupSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('group_name', 'group_host', 'group_date')

group_schema = groupSchema()
groups_schema = groupSchema(many=True)

# ***Needs to be run from Python interactive shell***
# from app import db
# db.create_all()

# endpoint to create new group
@app.route("/add", methods=["POST"])

def add_group():

    name = request.json['group_name']
    host = request.json['group_host']

    new_group = group(name,host)

    db.session.add(new_group)
    db.session.commit()

    return jsonify(new_group)


# endpoint to show all groups
@app.route("/groups", methods=["GET"])
def get_groups():
    all_groups = group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result.data)

# endpoint to get detail by id
@app.route("/listID/<id>", methods=["GET"])
def group_detailID(id):

    group_id = group.query.get(id)
    return group_schema.jsonify(group_id)


# endpoint to get detail by group
@app.route("/group/<string:name>", methods=["GET"])
def group_detailName(name):

    groups = group.query.filter_by(group_name=name)
    return groups_schema.jsonify(groups)


# endpoint to update group by id
@app.route("/update/<id>", methods=["PUT"])
def group_update(id):
    gp = group.query.get(id)

    gp.group_name = request.json['group_name']
    gp.group_host = request.json['group_host']


    db.session.commit()
    return group_schema.jsonify(group)


# endpoint to delete id
@app.route("/delete/<id>", methods=["DELETE"])
def id_delete(id):
    del_id = group.query.get(id)
    db.session.delete(del_id)
    db.session.commit()

    return group_schema.jsonify(group)


if __name__ == '__main__':
    app.run(debug=True)
