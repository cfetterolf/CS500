/********** USER INFO ***********/
var name = "";
var leaders = [];
var member = true;
var leader = false;
var user_schedule = {};

/********** GLOBAL VARS ************/
var users = {}
var time_blocks = {}
var leader_groups = {}
var matched_time_blocks = {}


// function testPHP() {
//   alert('sent')
//   var json = '{"firstkey":"firstvalue","secondkey":"secondvalue"}';
//       $.ajax({ type: 'POST', url: 'php/test.php', data: {json: json}, success : function(data){
//           alert(data);
//       }});
// }

$(document).ready(function(){
  getGroupInfo();
  handleUserInfo();
  handleUserList();

});

function getGroupInfo() {
  console.log("requesting data...");
  // Get the group data
  $.get("/ajax/db/", function(data, status){
        console.log(data);
        console.log(status);
        users = data.users
        time_blocks = data.time_blocks
        leader_groups = data.leader_groups

        // Display the users
        setUserTable(users);
        displayScheduleData();
    });
}

/* ALGORITHM */
var indexes = []
var lg_map = []
var tb_map = []
var member_matrix = []

function runAlgorithm() {
  $.get("/ajax/alg/", function(data, status){
        console.log(data);
        console.log(status);
        indexes = data.indexes
        lg_map = data.lg_map
        tb_map = data.tb_map
        member_matrix = data.member_matrix
        handleResults()
    });
}

function handleResults() {
  for (var i = 0; i < indexes.length; i++) {
    var tb = indexes[i][0]
    var lg = indexes[i][1]
    // matched_time_blocks[tb_map[tb]] = {}
    console.log("Time Block "+i+":");
    console.log(tb_map[tb]);
    console.log("Leader Group "+i+":");
    console.log(lg_map[lg]);
    console.log("Members matched: ");
    console.log(member_matrix[tb][lg]);
    console.log();
  }
}

/* ./ALGORITHM */

function displayScheduleData() {

  for (var id in time_blocks) {
    var block = time_blocks[id];
    var day = block['day'];
    var start = block['start'];
    var end = block['end'];
    console.log(block);
    var day_col = document.getElementById(day);
    day_col.innerHTML += '<div class="form-check"><label class="form-check-label"><input class="form-check-input timeCheckbox" type="checkbox" data-block-id="' + id +'">' + formatTime(start) + ' - ' + formatTime(end) + '</input></label></div>';
  }
}

function handleUserList() {

  // Click to see a user's availability
  $(".request-user-schedule").click(function (event) {
    // TODO

  });

  // Click to add new user
  $("#addUserButton").click(function (event) {
    $("#addUserForm").show();
  });

}

function handleUserInfo() {

  $(".leaderCheckbox").click(function (event) {
    if ($(this).is(":checked")) {
      leaders.push($(this).val());
    } else {
      leaders.splice( $.inArray($(this).val(), leaders), 1 );
    }
  });

  $("#memberCheckbox").click(function (event) {
    if ($(this).is(":checked")) {
      member = true;
    } else {
      member = false;
    }
  });

  $("#leaderCheckbox").click(function (event) {
    if ($(this).is(":checked")) {
      leader = true;
    } else {
      leader = false;
    }
  });

  // select times free
  $(".timeCheckbox").click(function (event) {
    var id = $(this).attr("data-block-id");
    if ($(this).is(":checked")) {
      time_blocks[id];
      user_schedule[id] = {day: time_blocks[id]['day'], start: time_blocks[id]['start'], end: time_blocks[id]['end']};
    } else {
      delete user_schedule[id];
    }
  });

  $("#submitNewUser").click(function(){

    // TODO - check if form is filled out

    var num_users = Object.keys(users).length;
    var name = $("#nameInput").val().split(" ");
    console.log(name);
    user = {
      first_name: name[0],
      last_name: name[1],
      email: $("#emailInput").val(),
      member: member,
      leader: leader,
      schedule: user_schedule
    }

    var user_id = "user_"+(num_users+1);
    users[user_id] = user;
    console.log(users);

    // Update user table
    updateUserTable(user);

    // Close new user form
    $("#addUserForm").hide();

  });

  // Click to hide new user form
  $(".cancel").click(function() {
    $("#addUserForm").hide();
  })

}

function setUserTable(users) {
  for(var user in users) {
    var newRow = $("<tr>");
    var cols = "";
    var mem = '';
    var lead = '';
    if(users[user].member == true) {mem = 'X';}
    if(users[user].leader == true) {lead = 'X';}

    cols += '<td>' + users[user].first_name + ' ' + users[user].last_name + '</td>';
    cols += '<td>' + mem + '</td>';
    cols += '<td>' + lead + '</td>';
    cols += '<td><a href="#" class="request-user-schedule">Click Here<a></td>';
    newRow.append(cols);
    $("table.user-table").append(newRow);
  }
}

function updateUserTable(user) {
  var newRow = $("<tr>");
  var cols = "";
  var mem = '';
  var lead = '';
  if(user.member == true) {mem = 'X';}
  if(user.leader == true) {lead = 'X';}

  cols += '<td>' + user.first_name + ' ' + user.last_name + '</td>';
  cols += '<td>' + mem + '</td>';
  cols += '<td>' + lead + '</td>';
  cols += '<td><a href="#" class="request-user-schedule">Click Here<a></td>';
  newRow.append(cols);
  $("table.user-table").append(newRow);
}

function resetUserSchedule() {
  user_schedule = {};
}

function formatTime(decimal_time){
 var time = ""+decimal_time
 time = time.split('.')
 var hours = Number(time[0]);
 var minutes = Number(time[1]);

  // calculate
  var timeValue;

  if (hours > 0 && hours <= 12) {
    timeValue= "" + hours;
  } else if (hours > 12) {
    timeValue= "" + (hours - 12);
  } else if (hours == 0) {
    timeValue= "12";
  }

  minutes = Math.round(60 * (decimal_time - hours))
  timeValue += (minutes < 10) ? ":0" + minutes : ":" + minutes;
  timeValue += (hours >= 12) ? " pm" : " am";  // get AM/PM
  return timeValue
}

function showUserList() {
  $(".user-list").show();
  $(".schedule").hide();
}