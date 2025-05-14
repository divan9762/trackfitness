-- Create database if not exists
CREATE DATABASE IF NOT EXISTS trackfit;
USE trackfit;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Workouts table
CREATE TABLE IF NOT EXISTS workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    workout_name VARCHAR(100) NOT NULL,
    workout_date DATE NOT NULL,
    duration_minutes INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Exercises table
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exercise_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workout_Exercises table (junction table for workouts and exercises)
CREATE TABLE IF NOT EXISTS workout_exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT NOT NULL,
    exercise_id INT NOT NULL,
    sets INT NOT NULL,
    reps INT,
    weight DECIMAL(5,2),
    duration_minutes INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

-- Records table (for tracking personal records)
CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL,
    record_value DECIMAL(5,2) NOT NULL,
    record_type ENUM('weight', 'reps', 'duration') NOT NULL,
    achieved_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

-- Insert some default exercises
INSERT INTO exercises (exercise_name, category, description) VALUES
('Bench Press', 'Chest', 'A compound exercise that primarily targets the chest muscles'),
('Squat', 'Legs', 'A compound exercise that targets the lower body'),
('Deadlift', 'Back', 'A compound exercise that targets the posterior chain'),
('Pull-up', 'Back', 'A bodyweight exercise that targets the back and biceps'),
('Push-up', 'Chest', 'A bodyweight exercise that targets the chest and triceps'),
('Plank', 'Core', 'An isometric exercise that targets the core muscles'),
('Running', 'Cardio', 'A cardiovascular exercise that improves endurance'),
('Cycling', 'Cardio', 'A low-impact cardiovascular exercise'),
('Dumbbell Curl', 'Arms', 'An isolation exercise that targets the biceps'),
('Shoulder Press', 'Shoulders', 'A compound exercise that targets the deltoids'); 