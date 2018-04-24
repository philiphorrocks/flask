from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pprint
import datetime

DateTime='date'

db = SQLAlchemy()


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


# Generate marshmallow Schemas from your model to handle serialisation
class groupSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ('group_name', 'group_host', 'group_date')

group_schema = groupSchema()
groups_schema = groupSchema(many=True)
