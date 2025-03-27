from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, URL


# -------------------------------
# Student Registration Form
# -------------------------------
class StudentRegistrationForm(FlaskForm):
    confirm_pass_msg = "Please confirm the same entered password!"
    
    # Email field with email validation
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Full name is required
    full_name = StringField('Full Name', validators=[DataRequired()])
    
    # Password and confirmation with equality check
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message=confirm_pass_msg)]
    )
    
    # Optional contact info
    phone_number = StringField('Phone Number (optional)', validators=[])
    nationality = StringField('Nationality (optional)', validators=[])
    country_of_residence = StringField('Country of Residence (optional)', validators=[])
    
    submit = SubmitField('Register')


# -------------------------------
# Student Login Form
# -------------------------------
class StudentLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# -------------------------------
# Agency Registration Form
# -------------------------------
class AgencyRegistrationForm(FlaskForm):
    url_msg = "Please, insert a website's valid URL with a protocol and a TLD!"
    confirm_pass_msg = "Please confirm the same entered password!"
    
    # Basic required fields
    name = StringField('Agency Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message=confirm_pass_msg)]
    )

    # Optional fields for agency details
    description = TextAreaField('Description (optional)')
    website = StringField('Website', validators=[URL(message=url_msg)])
    
    submit = SubmitField('Register')


# -------------------------------
# Agency Login Form
# -------------------------------
class AgencyLoginForm(FlaskForm):
    name = StringField('Agency Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# -------------------------------
# Advisor Registration Form
# -------------------------------
class AdvisorRegistrationForm(FlaskForm):
    confirm_pass_msg = "Please confirm the same entered password!"
    
    # Required fields for identification and login
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message=confirm_pass_msg)]
    )
    
    # Required location + optional phone
    country_of_residence = StringField('Country of Residence', validators=[DataRequired()])
    phone_number = StringField('Phone Number (optional)', validators=[])
    
    submit = SubmitField('Register')


# -------------------------------
# Advisor Login Form
# -------------------------------
class AdvisorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
