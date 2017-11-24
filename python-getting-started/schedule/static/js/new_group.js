
// SETTING VARIABLES: GROUP NAME + TIME
var groupName, schoolSemYear;
groupName = "";
schoolSemYear = "";

//SETTING VARIABLES: TIME SLOTS
var lastIndexTB = 0;   //starting time slot ID for each group

// Object Constructor + Functions
function TimeSlot(timeSlotID, startTime, endTime, day) {
  //this.variable = input;
  this.timeSlotID = timeSlotID;
  this.startTime = startTime;
  this.endTime = endTime;
  this.day = day;
  this.printTimeSlot = function() {
    return timeSlotID + ": " + day + " " + start + " - " + end;
  };
}

// TIME BLOCK TABLE
function addNewTBRow() {
  //Adds new row to time block table with empty fields
  lastIndexTB++;
  $('#timeBlockTable tr:last').after(
    //HOW TO MULTILINE STRING????
    '<tr class="tb_row" id="rowTBID_' + lastIndexTB + '"> \
        <td>' + lastIndexTB + '</td> \
        <td> \
          <input class="form-control startTime" type="time" value="--:--:--" \
          name="startTime"> \
        </td> \
        <td> \
          <input class="form-control endTime" type="time" value="--:--:--" \
          name="startTime"> \
        </td> \
        <td> \
          <select class="form-control day" name="day"> \
            <option selected>Choose...</option> \
            <option value="Monday">Monday</option> \
            <option value="Tuesday">Tuesday</option> \
            <option value="Wednesday">Wednesday</option> \
            <option value="Thursday">Thursday</option> \
            <option value="Friday">Friday</option> \
            <option value="Saturday">Saturday</option> \
            <option value="Sunday">Sunday</option> \
          </select> \
        </td> \
        <td> \
          <button type="button" class="close" aria-label="Close" \
          onclick="deleteRowTB(this)"> \
            <span aria-hidden="true">&times;</span> \
          </button> \
        </td> \
    </tr>');
}

// Delete Time Block Row
function deleteRowTB(o) {
  lastIndexTB--;
  // NEED TO FIX NUMBERING OF PREV ROWS!!!
  // https://stackoverflow.com/questions/11673322/numbering-dynamic-table-rows
  var p=o.parentNode.parentNode;
  p.parentNode.removeChild(p);
}

function createNewGroup() {

  /* check if empty */
  var empty = false
  var name, term;
  if ((name = $('#groupName').val()) === "") {
    console.log('ERROR in name');
    $('#nameHelp').html('Please Enter a Name').attr('style', 'color: red !important');
    empty = true
  }
  if ((term = $('#groupTerm').val()) === "") {
    $('#termHelp').html('Please Enter a Term').attr('style', 'color: red !important');
    empty = true
  }

  time_blocks = {}
  $('.tb_row').each(function(i) {
    start = timeToDecimal($(this).find(".startTime").val())
    end = timeToDecimal($(this).find(".endTime").val())
    day = $(this).find(".day").val()

    if (start && end && (day && day != "Choose...")) {
      time_blocks[i] = {}
      time_blocks[i]['start'] = start
      time_blocks[i]['end'] = end
      time_blocks[i]['day'] = day.toLowerCase()
    }
  });
  console.log(time_blocks);

  if (!empty) {
    group = {
      'name': name,
      'term': term,
      'time_blocks': time_blocks
    }
    createGroupDB(group)
  }
}

function timeToDecimal(t) {
    var arr = t.split(':');
    return parseFloat(parseInt(arr[0], 10) + '.' + parseInt((arr[1]/6)*10, 10));
}


function createGroupDB(group) {
  $.post( "/ajax/db/groups/new", JSON.stringify(group), function(data, status) {
    console.log("DB response:");
    console.log(data);
  });
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});


/**
$(document).ready(function() {
    var startTimeValidators = {
            row: '.col-xs-4',   // The title is placed inside a <div class="col-xs-4"> element
            validators: {
                notEmpty: {
                    message: 'The start time is required'
                }
            }
        },
        endTimeValidators = {
            row: '.col-xs-4',
            validators: {
                notEmpty: {
                    message: 'The end time is required'
                },

                isbn: {
                    message: 'The ISBN is not valid'
                }

            }
        },
        dayValidators = {
            row: '.col-xs-2',
            validators: {
                notEmpty: {
                    message: 'The day is required'
                },

                numeric: {
                    message: 'The price must be a numeric number'
                }

            }
        },
        timeSlotID = 0;

    $('#newGroupForm')
        .formValidation({
            framework: 'bootstrap',
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                'timeSlot[0].startTime': startTimeValidators,
                'timeSlot[0].endTime': endTimeValidators,
                'timeSlot[0].day': dayValidators
            }
        })

        // Add button click handler
        .on('click', '.addButton', function() {
            timeSlotID++;
            var $template = $('#timeSlotTemplate'),
                $clone    = $template
                                .clone()
                                .removeClass('hide')
                                .removeAttr('id')
                                .attr('data-book-index', timeSlotID)
                                .insertBefore($template);

            // Update the name attributes
            $clone
                .find('[name="startTime"]').attr('name', 'timeSlot[' + timeSlotID + '].startTime').end()
                .find('[name="endTime"]').attr('name', 'timeSlot[' + timeSlotID + '].endTime').end()
                .find('[name="day"]').attr('name', 'timeSlot[' + timeSlotID + '].day').end();

            // Add new fields
            // Note that we also pass the validator rules for new field as the third parameter
            $('#newGroupForm')
                .formValidation('addField', 'book[' + timeSlotID + '].startTime', startTimeValidators)
                .formValidation('addField', 'book[' + timeSlotID + '].endTime', endTimeValidators)
                .formValidation('addField', 'book[' + timeSlotID + '].day', dayValidators);
        })

        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row  = $(this).parents('.form-group'),
                index = $row.attr('data-book-index');

            // Remove fields
            $('#newGroupForm')
                .formValidation('removeField', $row.find('[name="timeSlot[' + index + '].startTime"]'))
                .formValidation('removeField', $row.find('[name="timeSlot[' + index + '].endTime"]'))
                .formValidation('removeField', $row.find('[name="timeSlot[' + index + '].day"]'));

            // Remove element containing the fields
            $row.remove();
        });
});
**/
