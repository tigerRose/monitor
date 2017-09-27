#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class NewProjectForm(FlaskForm):
    project_name = StringField('工程名称', validators=[Required()])
    devices_name = StringField('设备列表', validators=[Required()])
    submit = SubmitField('新建工程')
