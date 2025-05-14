from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.workout import Workout, Exercise, WorkoutExercise, Record
from app import db
from datetime import datetime

bp = Blueprint('workouts', __name__, url_prefix='/workouts')

@bp.route('/')
@login_required
def index():
    workouts = Workout.query.filter_by(user_id=current_user.id)\
        .order_by(Workout.workout_date.desc()).all()
    return render_template('workouts/index.html', workouts=workouts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        workout_name = request.form.get('workout_name')
        workout_date = datetime.strptime(request.form.get('workout_date'), '%Y-%m-%d').date()
        duration_minutes = request.form.get('duration_minutes')
        notes = request.form.get('notes')

        workout = Workout(
            user_id=current_user.id,
            workout_name=workout_name,
            workout_date=workout_date,
            duration_minutes=duration_minutes,
            notes=notes
        )

        try:
            db.session.add(workout)
            db.session.commit()
            flash('Workout created successfully!', 'success')
            return redirect(url_for('workouts.view', workout_id=workout.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the workout.', 'danger')

    exercises = Exercise.query.all()
    return render_template('workouts/create.html', exercises=exercises)

@bp.route('/<int:workout_id>')
@login_required
def view(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('You do not have permission to view this workout.', 'danger')
        return redirect(url_for('workouts.index'))
    
    # Get all exercises for the Add Exercise modal
    exercises = Exercise.query.all()
    return render_template('workouts/view.html', workout=workout, exercises=exercises, today=datetime.now().date())

@bp.route('/<int:workout_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('You do not have permission to edit this workout.', 'danger')
        return redirect(url_for('workouts.index'))

    if request.method == 'POST':
        workout.workout_name = request.form.get('workout_name')
        workout.workout_date = datetime.strptime(request.form.get('workout_date'), '%Y-%m-%d').date()
        workout.duration_minutes = request.form.get('duration_minutes')
        workout.notes = request.form.get('notes')

        try:
            db.session.commit()
            flash('Workout updated successfully!', 'success')
            return redirect(url_for('workouts.view', workout_id=workout.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the workout.', 'danger')

    exercises = Exercise.query.all()
    return render_template('workouts/edit.html', workout=workout, exercises=exercises)

@bp.route('/<int:workout_id>/delete', methods=['POST'])
@login_required
def delete(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('You do not have permission to delete this workout.', 'danger')
        return redirect(url_for('workouts.index'))

    try:
        db.session.delete(workout)
        db.session.commit()
        flash('Workout deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the workout.', 'danger')

    return redirect(url_for('workouts.index'))

@bp.route('/<int:workout_id>/exercises/add', methods=['POST'])
@login_required
def add_exercise(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    exercise_id = request.form.get('exercise_id')
    sets = request.form.get('sets')
    reps = request.form.get('reps')
    weight = request.form.get('weight')
    duration_minutes = request.form.get('duration_minutes')
    notes = request.form.get('notes')

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise_id,
        sets=sets,
        reps=reps,
        weight=weight,
        duration_minutes=duration_minutes,
        notes=notes
    )

    try:
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify({'message': 'Exercise added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred'}), 500

@bp.route('/exercises/<int:exercise_id>/delete', methods=['POST'])
@login_required
def delete_exercise(exercise_id):
    workout_exercise = WorkoutExercise.query.get_or_404(exercise_id)
    if workout_exercise.workout.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        db.session.delete(workout_exercise)
        db.session.commit()
        return jsonify({'message': 'Exercise removed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred'}), 500

@bp.route('/records/add', methods=['POST'])
@login_required
def add_record():
    exercise_id = request.form.get('exercise_id')
    record_value = request.form.get('record_value')
    record_type = request.form.get('record_type')
    achieved_date = datetime.strptime(request.form.get('achieved_date'), '%Y-%m-%d').date()

    record = Record(
        user_id=current_user.id,
        exercise_id=exercise_id,
        record_value=record_value,
        record_type=record_type,
        achieved_date=achieved_date
    )

    try:
        db.session.add(record)
        db.session.commit()
        flash('Record added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the record.', 'danger')

    return redirect(url_for('workouts.index'))

@bp.route('/init-exercises')
@login_required
def init_exercises():
    # Check if exercises already exist
    if Exercise.query.first() is not None:
        flash('Exercises already exist in the database.', 'info')
        return redirect(url_for('workouts.index'))
    
    # List of default exercises
    default_exercises = [
        # Strength exercises
        {'name': 'Bench Press', 'type': 'strength'},
        {'name': 'Squats', 'type': 'strength'},
        {'name': 'Deadlift', 'type': 'strength'},
        {'name': 'Pull-ups', 'type': 'strength'},
        {'name': 'Push-ups', 'type': 'strength'},
        {'name': 'Shoulder Press', 'type': 'strength'},
        {'name': 'Bicep Curls', 'type': 'strength'},
        {'name': 'Tricep Extensions', 'type': 'strength'},
        {'name': 'Lunges', 'type': 'strength'},
        {'name': 'Plank', 'type': 'strength'},
        
        # Cardio exercises
        {'name': 'Running', 'type': 'cardio'},
        {'name': 'Cycling', 'type': 'cardio'},
        {'name': 'Swimming', 'type': 'cardio'},
        {'name': 'Jump Rope', 'type': 'cardio'},
        {'name': 'Rowing', 'type': 'cardio'}
    ]
    
    try:
        # Add exercises to database
        for exercise_data in default_exercises:
            exercise = Exercise(
                exercise_name=exercise_data['name'],
                exercise_type=exercise_data['type']
            )
            db.session.add(exercise)
        
        db.session.commit()
        flash('Default exercises added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding exercises.', 'danger')
    
    return redirect(url_for('workouts.index')) 