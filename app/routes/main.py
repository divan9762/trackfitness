from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.workout import Workout, Exercise, Record, WorkoutExercise
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent workouts
    recent_workouts = Workout.query.filter_by(user_id=current_user.id)\
        .order_by(Workout.workout_date.desc())\
        .limit(5).all()

    # Get workout statistics
    total_workouts = Workout.query.filter_by(user_id=current_user.id).count()
    
    # Get recent records
    recent_records = Record.query.filter_by(user_id=current_user.id)\
        .order_by(Record.achieved_date.desc())\
        .limit(5).all()

    # Get workout frequency (last 30 days)
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    workouts_last_month = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= thirty_days_ago
    ).count()

    # Get most common exercises
    common_exercises = db.session.query(
        Exercise.exercise_name,
        func.count(WorkoutExercise.id).label('count')
    ).join(WorkoutExercise)\
     .join(Workout)\
     .filter(Workout.user_id == current_user.id)\
     .group_by(Exercise.exercise_name)\
     .order_by(func.count(WorkoutExercise.id).desc())\
     .limit(5).all()

    return render_template('main/dashboard.html',
                         recent_workouts=recent_workouts,
                         total_workouts=total_workouts,
                         recent_records=recent_records,
                         workouts_last_month=workouts_last_month,
                         common_exercises=common_exercises) 