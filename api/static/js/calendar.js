function createCalendar(date, doctorId) {

    $('#calendar').empty();

    var day_of_week = new Array('Dom','Lun','Mar','Mie','Jue','Vie','Sáb');
    var month_of_year = new Array('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre');

    //  DECLARE AND INITIALIZE VARIABLES
    var today = new Date();
    // var weekday = today.getDay();    // Returns day (1-31)
    today = format(today)

    var Calendar = new Date();
    if (typeof date != 'undefined') {
        Calendar = date;
    }

    var year = Calendar.getFullYear();     // Returns year
    var month = Calendar.getMonth();    // Returns month (0-11)

    var originalDate = new Date(Calendar.getTime());

    var DAYS_OF_WEEK = 7;    // "constant" for number of days in a week
    var DAYS_OF_MONTH = 31;    // "constant" for number of days in a month
    var cal;    // Used for printing

    Calendar.setDate(1);    // Start the calendar day at '1'
    Calendar.setMonth(month);    // Start the calendar month at now


    /* VARIABLES FOR FORMATTING
     NOTE: You can format the 'BORDER', 'BGCOLOR', 'CELLPADDING', 'BORDERCOLOR'
     tags to customize your caledanr's look. */

    var TR_start = '<TR>';
    var TR_start_week = '<TR class="week-row">';
    var TR_end = '</TR>';
    var TD_start = '<TD WIDTH="30" class="day">';
    var TD_start_data_date = '<TD WIDTH="30" class="day selectable" data-date=';
    var TD_end = '</TD>';

    cal =  '<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=0 BORDERCOLOR=BBBBBB><TR><TD>';
    cal += '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=2>' + TR_start;
    cal += '<TD COLSPAN=1  BGCOLOR="#e1e1e1"><CENTER><B><div class="calendarButton prevMonth"><</div>' + '</B>' + TD_end;
    cal += '<TD COLSPAN=5  BGCOLOR="#e1e1e1"><CENTER><B>' + month_of_year[month]  + ' ' + year + '</B>' + TD_end;
    cal += '<TD COLSPAN=1  BGCOLOR="#e1e1e1"><CENTER><B><div class="calendarButton nextMonth">></div>' + '</B>' + TD_end;
    cal += TR_start_week;

    // LOOPS FOR EACH DAY OF WEEK
    for(index=0; index < DAYS_OF_WEEK; index++) {

        // if(weekday == index) {
        //     // BOLD TODAY'S DAY OF WEEK
        //     cal += TD_start + '<B>' + day_of_week[index] + '</B>' + TD_end;
        // } else {
            // PRINTS DAY
            cal += TD_start + day_of_week[index] + TD_end;
        // }
    }

    cal += TD_end + TR_end;
    cal += TR_start;

    // FILL IN BLANK GAPS UNTIL TODAY'S DAY
    for(index=0; index < Calendar.getDay(); index++) {
        cal += TD_start + '  ' + TD_end;
    }

    // LOOPS FOR EACH DAY IN CALENDAR
    for(index=0; index < DAYS_OF_MONTH; index++) {
        if( Calendar.getDate() > index ) {
            // RETURNS THE NEXT DAY TO PRINT
            week_day = Calendar.getDay();

            // START NEW ROW FOR FIRST DAY OF WEEK
            if(week_day == 0) {
                cal += TR_start;
            }

            if(week_day != DAYS_OF_WEEK) {

                // SET VARIABLE INSIDE LOOP FOR INCREMENTING PURPOSES
                var day = Calendar.getDate();

                if( today==format(Calendar) ) {
                    // HIGHLIGHT TODAY'S DATE
                    cal += TD_start_data_date + format(Calendar) + " data-day=" + getDay(Calendar) + " id='today'>" + day + TD_end;
                } else {
                    // PRINTS DAY
                    cal += TD_start_data_date + format(Calendar) + " data-day=" + getDay(Calendar) + " >" + day + TD_end;
                }
            }

            // END ROW FOR LAST DAY OF WEEK
            if(week_day == DAYS_OF_WEEK) {
                cal += TR_end;
            }
        }

        // INCREMENTS UNTIL END OF THE MONTH
        Calendar.setDate(Calendar.getDate()+1);

    }// end for loop

    cal += '</TD></TR></TABLE></TABLE>';

    //  PRINT CALENDAR
    $('#calendar').append(cal);

    setEvents(originalDate, doctorId);

    highlightNotEmptyDays(doctorId, originalDate.getMonth() + 1, originalDate.getFullYear());

}

function setEvents(originalDate, doctorId) {
    $('.prevMonth').off('click');
    $('.prevMonth').click(function() {
        originalDate.setMonth(originalDate.getMonth() - 1)
        createCalendar(originalDate, doctorId);
    });

    $('.nextMonth').off('click');
    $('.nextMonth').click(function() {
        originalDate.setMonth(originalDate.getMonth() + 1)
        createCalendar(originalDate, doctorId);
    });

    $('.day.selectable').off('click');
    $('.day.selectable').click(function() {
        onSelectDay($(this), doctorId)
    });

    $('#saveScheduleButton').off('click');
    $('#saveScheduleButton').click(function () {
        saveSchedule(doctorId)
    });
}

function format(date) {
    return date.getTime();
}

function getDay(date) {
    return date.getDate();
}

function highlightNotEmptyDays(doctorId, month, year) {
    $.ajax({
        type: "GET",
        url: '/api/doctors/' + doctorId + '/days/' + month + '/' + year,
        success: function(response) {
            if(response.success){
                console.log(response.payload);
                response.payload.forEach(function(item) {
                    $('.day.selectable[data-day="' + item.day+ '"]').addClass('filled');
                })
            } else {

            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            if(xhr.status==404) {
                console.log(thrownError);
            }
        }
    });
}

function initTimeSelects() {
    var i ,j;
    for(i=8; i<20; i++) {
        for(j=0; j<2; j++) {
            item = i + ":" + (j===0 ? "00" : "30");
            $('#scheduleSelect select').append($('<option>', {
                value: item,
                text : item
            }));
        }
    }

    $('#scheduleSelect select').material_select();
}

function showScheduleSelect(schedule) {
    console.log(schedule);
    $('#scheduleSelect').removeClass('hidden');
    $('#scheduleSelect select').val('');
    $('#existing').val('');
    if(schedule){
        $('#existing').val(1);
        var from = new Date(schedule.start);
        var to = new Date(schedule.end);
        $('#from').val(getHoursAndMinutes(from));
        $('#to').val(getHoursAndMinutes(to));
    }
    $('#scheduleSelect select').material_select();
}

function onSelectDay(element, doctorId) {
    var date = element.data('date');
    var calendar = new Date(date);
    $('.day').removeClass('selected');
    element.addClass('selected');
    $('.dayLabel').text(dateToString(calendar));

    $.ajax({
        type: "GET",
        url: '/api/doctors/' + doctorId + '/schedule/' + date,
        success: function(response) {
            if(response.success){
                showScheduleSelect(response.payload);
            } else {
                showScheduleSelect();
            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            if(xhr.status==404) {
                console.log(thrownError);
            }
        }
    });
}

function dateToString(date) {
    var monthNames = [
      "Enero", "Febrero", "Marzo",
      "Abril", "Mayo", "Junio", "Julio",
      "Agosto", "Septiembre", "Octubre",
      "Noviembre", "Diciembre"
    ];

    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();

    console.log(day, monthNames[monthIndex], year);
    return day + ' de ' + monthNames[monthIndex] + ' de ' + year;
}

function saveSchedule(doctorId) {
    var selected = getSelectedDate();
    var startValue = $('#from').val().split(':');
    var start = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate(), startValue[0], startValue[1], 0);
    var endValue = $('#to').val().split(':');
    var end = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate(), endValue[0], endValue[1], 0);
    var existing = $('#existing').val()
    $.ajax({
        type: (existing?"PUT":"POST"),
        data: JSON.stringify({start: start.getTime().toString(), end: end.getTime().toString()}),
        dataType: 'json',
        contentType: 'application/json',
        url: '/api/doctors/' + doctorId + '/schedule',
        success: function(response) {
            $('#existing').val(1);
            $('.day.selected').addClass('filled');
            console.log(response)
        },
        error: function(xhr, ajaxOptions, thrownError) {
            if(xhr.status==404) {
                console.log(thrownError);
            }
        }
    });
}

function getSelectedDate() {
    var selected = new Date($('.day.selected').data('date'));
    return selected;
}

function getHoursAndMinutes(date) {
    var minutes = (date.getMinutes()<10?'0':'') + date.getMinutes();
    return date.getHours() + ':' + minutes
}