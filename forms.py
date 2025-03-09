from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, URL


class StudentRegistrationForm(FlaskForm):
    confirm_pass_msg = "Please confirm the same entered password!"
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password', message=confirm_pass_msg)])
    phone_number = StringField('Phone Number (optional)', validators=[])
    nationality = StringField('Nationality (optional)', validators=[])
    country_of_residence = StringField(
        'Country of Residence (optional)', validators=[])
    submit = SubmitField('Register')


class StudentLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AgencyRegistrationForm(FlaskForm):
    url_msg = "Please, insert a website's valid URL with a protocol and a TLD!"
    confirm_pass_msg = "Please confirm the same entered password!"
    name = StringField('Agency Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password', message=confirm_pass_msg)])
    description = TextAreaField('Description (optional)')
    website = StringField('Website', validators=[URL(message=url_msg)])
    submit = SubmitField('Register')


class AgencyLoginForm(FlaskForm):
    name = StringField('Agency Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AdvisorRegistrationForm(FlaskForm):
    confirm_pass_msg = "Please confirm the same entered password!"
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password', message=confirm_pass_msg)])
    country_of_residence = StringField(
        'Country of Residence', validators=[DataRequired()])
    phone_number = StringField('Phone Number (optional)', validators=[])
    submit = SubmitField('Register')


class AdvisorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
