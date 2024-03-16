document.addEventListener('DOMContentLoaded', function() {
    
    fetchHabitChecks();

    habitCheckModals = document.querySelectorAll('.habit-check-modal');
    habitCheckModals.forEach(modal => {
        confirmButton = modal.querySelector('.modal-dialog .modal-content .modal-footer .modal-confirm');
        confirmButton.addEventListener('click', function() {
            checkUpdateURL = modal.querySelector('.modal-dialog .modal-content .modal-footer .modal-confirm').getAttribute('data-update-check-url');
            fetch(checkUpdateURL, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                fetchHabitChecks();
            });
            modal.querySelector('.modal-dialog .modal-content .modal-footer .modal-close').click();
        });
    });

    habits = document.querySelectorAll('.habit-details');
    habits.forEach(habit => {
        const habitUrl = habit.getAttribute('data-habit-url');
        habit.addEventListener('click', function() {
            window.location.href = habitUrl;
        });
    });
});


function fetchHabitChecks() {
    habitChecks = document.querySelectorAll('.habit-check');
    habitChecks.forEach(habitCheck => {
        const fetchURL = habitCheck.getAttribute("data-fetch-url");
        fetch(fetchURL)
        .then(response => response.json())
        .then(data => {
            if (data.check == true) {
                habitCheck.innerHTML = 
                `<div class="text-center me-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                        <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                    </svg>
                </div>`;
            }
            else {
                habitCheck.innerHTML = 
                `<div class="text-center text-secondary me-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                    </svg>
                </div>`;
            }
        });
    });
};