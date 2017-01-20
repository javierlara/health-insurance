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
    var TD_start_date_date = '<TD WIDTH="30" class="day selectable" data-date=';
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
                    cal += TD_start_date_date + format(Calendar) + " id='today'>" + day + TD_end;
                } else {
                    // PRINTS DAY
                    cal += TD_start_date_date + format(Calendar) + ">" + day + TD_end;
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

}

function setEvents(originalDate, doctorId) {
    $('.prevMonth').click(function() {
        originalDate.setMonth(originalDate.getMonth() - 1)
        createCalendar(originalDate, doctorId);
    });

    $('.nextMonth').click(function() {
        originalDate.setMonth(originalDate.getMonth() + 1)
        createCalendar(originalDate, doctorId);
    });

    $('.day.selectable').click(function() {
        $('.day').removeClass('selected');
        $(this).addClass('selected');
        $.ajax({
            type: "GET",
            url: '/api/doctors/' + doctorId + '/schedule/' + $(this).data('date'),
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                if(xhr.status==404) {
                    console.log(thrownError);
                }
            }
        });
    });
}

function format(date) {
    // var dd = date.getDate();
    // var mm = date.getMonth()+1; //January is 0!
    //
    // var yyyy = date.getFullYear();
    // if(dd<10){
    //     dd='0'+dd;
    // }
    // if(mm<10){
    //     mm='0'+mm;
    // }
    // return dd+'/'+mm+'/'+yyyy;

    return date.getTime();
}
