from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, render_template
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os
import urllib.request
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/upload')
@login_required
def upload_form():
	return render_template('upload.html', user=current_user)

@views.route('/upload', methods=['POST'])
@login_required
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading','error')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join('C:/Users/Chamudi/DeceptionDetectionFlask/Flask-Web-App-Tutorial-main/website/static/uploads/', filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename, user=current_user)

@views.route('/upload/display/<filename>')
@login_required
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@views.route('/past-videos', methods=['GET'])
@login_required
def past_videos():
    return render_template("past_videos.html", user=current_user)