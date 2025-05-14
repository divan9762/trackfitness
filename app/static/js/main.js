// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add exercise to workout
    const addExerciseForm = document.getElementById('addExerciseForm');
    if (addExerciseForm) {
        addExerciseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showAlert('danger', data.error);
                } else {
                    showAlert('success', data.message);
                    // Optionally refresh the exercise list or add the new exercise to the DOM
                    setTimeout(() => window.location.reload(), 1000);
                }
            })
            .catch(error => {
                showAlert('danger', 'An error occurred while adding the exercise.');
            });
        });
    }

    // Delete exercise from workout
    const deleteExerciseButtons = document.querySelectorAll('.delete-exercise');
    deleteExerciseButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to remove this exercise?')) {
                const exerciseId = this.dataset.exerciseId;
                
                fetch(`/workouts/exercises/${exerciseId}/delete`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        showAlert('danger', data.error);
                    } else {
                        showAlert('success', data.message);
                        // Remove the exercise element from the DOM
                        this.closest('.exercise-item').remove();
                    }
                })
                .catch(error => {
                    showAlert('danger', 'An error occurred while deleting the exercise.');
                });
            }
        });
    });

    // Add record
    const addRecordForm = document.getElementById('addRecordForm');
    if (addRecordForm) {
        addRecordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    showAlert('success', 'Record added successfully!');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                showAlert('danger', 'An error occurred while adding the record.');
            });
        });
    }

    // Helper function to show alerts
    function showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Dynamic exercise form fields
    const exerciseTypeSelect = document.getElementById('exerciseType');
    if (exerciseTypeSelect) {
        exerciseTypeSelect.addEventListener('change', function() {
            const weightFields = document.getElementById('weightFields');
            const durationFields = document.getElementById('durationFields');
            
            if (this.value === 'strength') {
                weightFields.style.display = 'block';
                durationFields.style.display = 'none';
            } else if (this.value === 'cardio') {
                weightFields.style.display = 'none';
                durationFields.style.display = 'block';
            } else {
                weightFields.style.display = 'none';
                durationFields.style.display = 'none';
            }
        });
    }
}); 