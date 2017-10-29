// NEW GROUP: JAVASCRIPT/JQUERY

//Notes
// no "-" in js
// use camel case e.g. myName, emailAd
//conole.log(INSERT);     --> have console open on opera/web
//alert();

//SETTING VARIABLES: GROUP NAME + TIME
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

//SETTING VARIABLES: ACCOUNT ADMIN
//var currentAccountAdmin, accountAdmin;
//currentAccountAdmin = ""; // edit later once get into accounts??
//accountAdmin = [];      //you + others entered    **add later?

/**
currentAccountAdmin = "This Person"; // edit later once get into accounts??
accountAdmin = [currentAccountAdmin];      //you + others entered
**/

/**
// TIME SLOTS: LEARNING OBJECTS

// Hard Coded Objects = {name:value, };
var timeSlotEx1 = {start:2100, end:2200, day:"Monday"};
var timeSlotEx2 = {
                  start:2200,
                  end:2300,
                  day:"Monday"
                };
// timeSlotEx1 <-- ID is assigned

// TIme Slots : Hard Coded Variables
var timeSlotIDHD, startTimeHC, endTimeHC, dayHC;
timeSlotIDHD = timeSlotIndex;
startTimeHC = "";
endTimeHC = "";
dayHC = "";
**/

// Create Objects fr Constructor
// var timeSlotEx3 = new TimeSlot(1, 2300, 2400, "Monday");

// Access Object/Method Properties
// objectName.prop OR objectName["property"]
//timeSlotEx3.start;
//timeSlotEx3["start"];
//timeSlotEx3.printTimeSlot();

// TB: EMPTY ROW

// TIME BLOCK TABLE
function addNewTBRow() {
  //Adds new row to time block table with empty fields
  //alert("Added New Row!");
  lastIndexTB++;
  $('#timeBlockTable tr:last').after(
    //HOW TO MULTILINE STRING????
    '<tr id="rowTBID_' + lastIndexTB + '"> \
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
          <select class="form-control col-2 day" name="day"> \
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
  //alert("Form submitted!");
  document.getElementById("newGroupSubmitConfirm").innerHTML =
  "You created a new group!";

  // SET VARIABLES

  groupName = document.getElementById("groupNameIn").value;
  schoolSemYear = document.getElementById("schoolSemYearIn").value;
  //accountAdmin = document.getElementById("addAccountAdminEmail").value;
  /**
  timeSlotEx4 = new TimeSlot(timeSlotIndex,
                             document.getElementById("startTime").value,
                             document.getElementById("endTime").value,
                             document.getElementById("day").value);
  **/
  startTimeHC = document.getElementById("startTime").value;
  endTimeHC = document.getElementById("endTime").value;
  dayHC = document.getElementById("day").value;

  // OUTPUT

  // Output: Name and Email
  document.getElementById("groupTitleOut").innerHTML = groupName + " " +
  schoolSemYear;
  //document.getElementById("timeBlockOutputSample").innerHTML = timeSlotEx4.printTimeSlot();
  document.getElementById("timeBlockOutputSample").innerHTML = dayHC + ": " +
  startTimeHC + " - " + endTimeHC;


}


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
