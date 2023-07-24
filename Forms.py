from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class PrefernceForm(FlaskForm):
    myChoices = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Barnyard']
    species = SelectField(u'Select animal Species', choices = myChoices, validators = [DataRequired()])
    myChoices2 = ['Baby', 'Young', 'Adult', 'Senior']
    age = SelectField(u'Select animal age', choices = myChoices2, validators = [DataRequired()])
    myChoices3 = ['Male', 'Female']
    gender = SelectField(u'Select Gender', choices = myChoices3, validators = [DataRequired()])
    myChoices4 = ['Small', 'Medium', 'Large', 'Xlarge']
    size= SelectField(u'Select size of the animal', choices = myChoices4, validators = [DataRequired()])
    location = StringField('Zipcode',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit =SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField()

    submit = SubmitField('Login')

class ContactForm(FlaskForm):

    submit = SubmitField('Reject')
    submit2 = SubmitField('Like')

class NavigationForm(FlaskForm):

    submit = SubmitField('Back One')
    submit2 = SubmitField('Next One')