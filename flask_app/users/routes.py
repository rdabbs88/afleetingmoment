import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import LoginForm, RegistrationForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    # redirect the user to the index route if they are already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('moments.index'))
    
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    # redirect the user to the index route if they are already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('moments.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            # check if username and password match, if successfully authenticated, redirect to their account page
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            # otherwise not successfully authenticated, ask the user to authenticate again
            else:
                flash("Login failed. Check your username and/or password")

    return render_template('login.html', form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('moments.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.modify(username=update_username_form.username.data)
            current_user.save()
            logout_user()
            return redirect(url_for("users.login"))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            # comments to help me understand what these do

            # retrieves the uploaded file from the submitted form
            image = update_profile_pic_form.picture.data
            # makes sure that filename is safe for storage by removing any special characters
            filename = secure_filename(image.filename)
            # extracts the last 3 characters of the filename and constructs a MIME type string, is ok because we are assuming only .jpg and .png?
            content_type = f'images/{filename[-3:]}'

            # check for case 1, adding a profile pic if user doesn't have one
            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(image.stream, content_type=content_type)
            # case 2, otherwise user has a profile pic so replace it
            else:
                current_user.profile_pic.replace(image.stream, content_type=content_type)

            current_user.save()
            return redirect(url_for("users.account"))

    # TODO: handle get requests
    profile_pic_base64 = None
    if current_user.profile_pic:
        profile_pic_bytes = io.BytesIO(current_user.profile_pic.read())
        profile_pic_base64 = base64.b64encode(profile_pic_bytes.getvalue()).decode()
    
    return render_template('account.html', update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form, image=profile_pic_base64)
