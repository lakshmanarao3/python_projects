from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, IntegerField
from wtforms.validators import DataRequired
class Hostinfo(FlaskForm):
    network=StringField("IPV4/IPV6 address", validators=[DataRequired()])
    submit=SubmitField("GetInfo")
class Subnethost(FlaskForm):
    network=StringField("IPV4/IPV6 address", validators=[DataRequired()])
    hosts=IntegerField("No of hosts required", validators=[DataRequired()])
    submit=SubmitField("GetSubnets")
class Subnetsubnets(FlaskForm):
    network=StringField("IPV4/IPV6 address", validators=[DataRequired()])
    subnets=IntegerField("No of subnets required", validators=[DataRequired()])
    submit=SubmitField("GetSubnets")