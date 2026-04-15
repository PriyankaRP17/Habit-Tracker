from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField("Register")

class HabitForm(FlaskForm):
    habit_name = StringField("Habit Name")
    habit_choice = SelectField(
        "Choose a habit",
        choices=[("", "Select from below"), ("Exercise", "Exercise"), ("Yoga", "Yoga"), ("Drink Water", "Drink Water")]
    )
    weight = IntegerField("Weight (kg)", validators=[Optional(), NumberRange(min=1)])
    height = IntegerField("Height (cm)", validators=[Optional(), NumberRange(min=30)])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=1)])
    gender = RadioField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[Optional()]
    )
    frequency = IntegerField("Frequency (days)", validators=[DataRequired(), NumberRange(min=1)])
    duration = IntegerField("Duration (Hours)", validators=[DataRequired(), NumberRange(min=1)])
    preferred_time = SelectField(
        "Preferred Time",
        choices=[("", "Choose from below"), ("Morning", "Morning"), ("Afternoon", "Afternoon"), ("Night", "Night")]
    )
    submit = SubmitField("Add")

