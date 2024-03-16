const currDetails = document.querySelector('.curr-details');
const currMonth = currDetails.getAttribute('data-curr-month');
const currYear = currDetails.getAttribute('data-curr-year');
calMiddleBtn = document.querySelector('.cal-middle-btn');
calRightBtn = document.querySelector('.cal-right-btn');
calMonth = parseInt(calMiddleBtn.getAttribute('data-cal-month'));
calYear = parseInt(calMiddleBtn.getAttribute('data-cal-year'));
calElement = document.querySelector('.cal');
h_id = document.querySelector('.habit-details').getAttribute('data-habit-id');

calButtons = document.querySelectorAll('.cal-btn');
calButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        calUpdateUrl = document.querySelector('.cal-btns').getAttribute('data-cal-update-url');
        cal_dir = btn.getAttribute('data-cal-dir')
        data = {
            "month": calMonth,
            "year": calYear,
            "dir": cal_dir,
            "h_id": h_id
        }
        fetch(calUpdateUrl, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data != null) {
                if (data.calRawHTML != null) {
                    calElement.innerHTML = data.calRawHTML;
                    calMiddleBtn.setAttribute('data-cal-month', data.new_month);
                    calMiddleBtn.setAttribute('data-cal-year', data.new_year);
                    calMiddleBtn.innerHTML = data.cal_title;
                    calMonth = parseInt(calMiddleBtn.getAttribute('data-cal-month'));
                    calYear = parseInt(calMiddleBtn.getAttribute('data-cal-year'));
                    updateCalButtons(calRightBtn, currMonth, currYear, calMonth, calYear);
                    calDayModals = document.querySelectorAll('.habit-cal-day-modal');
                    calDayUpdate(calDayModals);
                }
            }
        });
    });
});


calDayModals = document.querySelectorAll('.habit-cal-day-modal');
calDayUpdate(calDayModals);
getBestStreak(h_id);


function calDayUpdate(calDayModals) {
    calDayModals.forEach(modal => {
        const confirmBtn = modal.querySelector('.modal-dialog .modal-content .modal-body .modal-confirm');
        confirmBtn.addEventListener('click', function() {
            const calDayUpdateUrl = confirmBtn.getAttribute('data-update-day-url');
            fetch(calDayUpdateUrl, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                modal.querySelector('.modal-dialog .modal-content .modal-body .modal-close').click();
                calDate = data.date;
                calDayElements = document.querySelectorAll('#calDay-'+calDate);
                calErrorEl = document.querySelector('.cal-error');
                if (data.status == "success") {
                    calErrorEl.innerHTML = "";
                    if (data.msg == "new entry added") {
                        calDayElements.forEach(el => {
                            el.classList.remove('border-dark-subtle');
                            el.classList.add('btn-primary');
                        });
                    } else if (data.msg == "entry deleted") {
                        calDayElements.forEach(el => {
                            el.classList.remove('btn-primary');
                            el.classList.add('border-dark-subtle');
                        });
                    }
                    if (data.curr_streak != null) {
                        document.getElementById('habit-' + data.habit_id  + '-curr-streak').innerHTML = data.curr_streak;
                    }
                    getBestStreak(h_id);
                } else {
                    calErrorEl.innerHTML = "* " + data.msg;
                }
            });
        });
    });
};

function getBestStreak() {
    bestStreakEl = document.getElementById('habit-' + h_id  + '-best-streak');
    const getBSUrl = bestStreakEl.getAttribute('data-get-bs-url');
    fetch(getBSUrl)
    .then(response => response.json())
    .then(data => {
        if (data != null && data.status == "success") {
            if (bestStreakEl.innerHTML != data.best_streak) {
                bestStreakEl.innerHTML = data.best_streak;
            }
        }
    })
}


function updateCalButtons(calRB, currM, currY, calM, calY) {
    if (currY == calY) {
        if (currM > calM) {
            calRB.disabled = false;
        } else {
            calRB.disabled = true;
        }
    } else {
        calRB.disabled = false;
    }
};