from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit_username = SubmitField("Update Username")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None and user.username != current_user.username:
            raise ValidationError("Username is already taken!")

class UpdateProfilePicForm(FlaskForm):
    picture = FileField(
        "Profile Picture",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Only jpegs and pngs are accepted"),
        ],
    )
    submit_picture = SubmitField("Update Profile Picture")

class MomentForm(FlaskForm):
    description = TextAreaField("Description", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    public = BooleanField("Post publicly", default=True)
    addressed_to = StringField("Addressed To")
    submit = SubmitField("Create Post")

class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[InputRequired()])
    public = BooleanField("Post publicly", default=True)
    submit = SubmitField("Post Comment")
