import base64, io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from .. import google_client, db
from datetime import datetime
from ..models import Moment, Comment
from ..forms import MomentForm, CommentForm, SearchForm

moments = Blueprint("moments", __name__)

@moments.route("/")
def index():
    db_moments = Moment.objects.order_by('-created_at')
    
    # Format moments for template
    formatted_moments = []
    for moment in db_moments:
        formatted_moments.append({
            'id': str(moment.id),
            'content': moment.content,
            'username': moment.username,
            'addressed': moment.addressed_to,
            'lat': moment.location[0],
            'lng': moment.location[1],
            'time': moment.created_at.strftime("%Y-%m-%d %H:%M UTC")
        })
    
    return render_template("index.html", key=google_client.getKey(), moments=formatted_moments)

@moments.route("/createmoment", methods=["POST", "GET"])
def create_moment():
    form = MomentForm()
    
    if request.method == "GET":
        return render_template("createmoment.html", form=form)
    
    if form.validate_on_submit():
        content = form.description.data
        location_text = form.location.data
        
        # Get coordinates using Google Geocode API
        try:
            geocode_result = google_client.geocode(location_text)
            lat = geocode_result['lat']
            lng = geocode_result['lng']
        except Exception as e:
            print(f"Geocoding error: {e}")
            lat = float(request.form.get('latitude', 0.0))
            lng = float(request.form.get('longitude', 0.0))
        
        is_public = form.public.data
        
        if is_public:
            temp_username = 'Anonymous'  
        else:
            temp_username = '' 
            
        addressed_to = form.addressed_to.data
        
        # Create new moment
        new_moment = Moment(
            content=content,
            addressed_to=addressed_to,
            location=[lat, lng],
            username=temp_username,
            created_at=datetime.now()
        )
        new_moment.save()
        
        flash('Moment created successfully!', 'success')
        return redirect(url_for('moments.index'))
    
    # If form validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", 'danger')
    return render_template("createmoment.html", form=form)
    
@moments.route("/moment/<id>", methods=["GET"])
def create_comment(id):
    form = CommentForm()
    try:
        moment = Moment.objects.get(id=id)
        comments = Comment.objects(moment_id=id).order_by('-created_at')
        return render_template("createcomment.html", moment=moment, comments=comments, form=form)
    except:
        flash('Moment not found', 'danger')
        return redirect(url_for('moments.index'))

@moments.route("/comment/<id>", methods=["POST"])
def post_comment(id):
    form = CommentForm()
    try:
        moment = Moment.objects.get(id=id)
        
        if form.validate_on_submit():
            content = form.content.data
            is_public = form.public.data
            
            # Set username based on privacy preference
            if is_public:
                temp_username = 'Anonymous'
            else:
                temp_username = ''
            
            # Create new comment
            new_comment = Comment(
                content=content,
                username=temp_username,
                moment_id=id,
                created_at=datetime.now()
            )
            new_comment.save()
            
            flash('Comment added successfully!', 'success')
            return redirect(url_for('moments.create_comment', id=id))
        
        # If form validation fails
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
        
        comments = Comment.objects(moment_id=id).order_by('-created_at')
        return render_template("createcomment.html", moment=moment, comments=comments, form=form)
    except:
        flash('Moment not found', 'danger')
        return redirect(url_for('moments.index'))
    
@moments.route("/search", methods=["GET"])
def search():
    query = request.args.get('search')
    if not query:
        return redirect(url_for('moments.index'))
    
    # Search for moments containing the query
    # Search for moments containing the query in username or content
    from mongoengine.queryset.visitor import Q
    db_moments = Moment.objects(Q(content__icontains=query) | 
                                Q(username__icontains=query) | 
                                Q(addressed_to__icontains=query))
    db_moments = db_moments.order_by('-created_at')
    
    # Format moments for template
    formatted_moments = []
    for moment in db_moments:
        formatted_moments.append({
            'id': str(moment.id),
            'content': moment.content,
            'username': moment.username,
            'addressed': moment.addressed_to,
            'lat': moment.location[0],
            'lng': moment.location[1],
            'time': moment.created_at.strftime("%Y-%m-%d %H:%M UTC")
        })
    
    return render_template("index.html", key=google_client.getKey(), moments=formatted_moments)