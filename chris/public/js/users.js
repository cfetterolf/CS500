/********** USER INFO ***********/
var name = "";
var leaders = [];
var member = true;
var leader = false;
var user_schedule = {};

/********** DUMMY VARS ************/
var users = {
  user_1: {
    first_name: "Chris",
    last_name: "Fetterolf",
    email: "chris.fetterolf@gmail.com",
    member: true,
    leader: false,
    schedule: {
      0: {day: "monday", start: 12, end: 14},
      3: {day: "thursday", start: 16, end: 20},
      4: {day: "friday", start: 11, end: 14}
    }
  },
  user_2: {
    first_name: "Andrea",
    last_name: "Narciso",
    email: "anarciso@middlebury.edu",
    member: true,
    leader: true,
    schedule: {
      2: {day: "tuesday", start: 14, end: 18},
      3: {day: "thursday", start: 16, end: 20},
      4: {day: "friday", start: 11, end: 14},
      5: {day: "friday", start: 16, end: 18},
      6: {day: "sunday", start: 12, end: 15}
    }
  }
};

var time_blocks = {
  0: {day: "monday", start: 12, end: 14},
  1: {day: "monday", start: 16, end: 20},
  2: {day: "tuesday", start: 14, end: 18},
  3: {day: "thursday", start: 16, end: 20},
  4: {day: "friday", start: 11, end: 14},
  5: {day: "friday", start: 16, end: 18},
  6: {day: "sunday", start: 12, end: 15}
}

/********** ./DUMMY VARS ************/


function testPHP() {
  alert('sent')
  var json = '{"firstkey":"firstvalue","secondkey":"secondvalue"}';
      $.ajax({ type: 'POST', url: 'php/test.php', data: {json: json}, success : function(data){
          alert(data);
      }});
}

// $('#testPHP').click(function() {
//   alert('sent')
//   var json = '{"firstkey":"firstvalue","secondkey":"secondvalue"}';
//   $.ajax({ type: 'POST', url: 'php/test.php', data: {json: json}, success : function(data){
//       alert(data);
//   }});
// })

$(document).ready(function(){
  setUserTable(users);
  displayScheduleData();

  handleUserInfo();
  handleUserList();

});

function displayScheduleData() {

  for (var id in time_blocks) {
    var block = time_blocks[id];
    var day = block['day'];
    var start = block['start'];
    var end = block['end'];
    //console.log(block);
    var day_col = document.getElementById(day);
    day_col.innerHTML += '<div class="form-check"><label class="form-check-label"><input class="form-check-input timeCheckbox" type="checkbox" data-block-id="' + id +'">' + start + '-' + end + '</input></label></div>';
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

function showUserList() {
  $(".user-list").show();
  $(".schedule").hide();
}
