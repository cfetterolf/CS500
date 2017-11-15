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


$(document).ready(function(){
  getGroupInfo();
  handleUserInfo();
  handleUserList();

});

/******** DATABSE FUNCTIONS **********/

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
        displayLeaderPreferences();
    });
}

function updateDB(user) {
  console.log("USER:");
  console.log(user);
  // user['csrfmiddlewaretoken'] = "{{ csrf_token }}"
  $.post( "/ajax/db/user/", JSON.stringify(user), function(data, status) {
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

/***************************************/

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

function displayLeaderPreferences() {
  var pref_l = $('#preferredLeaders');
  var html = ''
  var count = 0;
  for (lgid in leader_groups) {
    console.log(leader_groups[lgid]);
    var leaders = leader_groups[lgid]['leaders'] //array
    html += '<div class="form-check form-check-inline active mt-sm"><label class="form-check-label"><input class="form-check-input leaderCheckbox" type="checkbox" data-block-lgid="' + lgid +'">  '
    console.log(html);
    console.log(leaders.length);
    for (var i = 0; i < leaders.length; i++) {
      if (i > 0) {
        html += ', '
      }
      console.log(leaders[i]);
      html += users[leaders[i]]['first_name']
    }

    html += '</input></label></div>'

    if (count > 3) {
      console.log('break');
      html += '<br />' // new line
      count = 0
    }
    count += 1
  }
  pref_l.html(html)
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

  $('#preferredLeaders').on('change', '.leaderCheckbox', function() {
    if ($(this).is(":checked")) {
      console.log("add leader!");
      var lgid = $(this).attr("data-block-lgid");
      leaders.push(lgid);
    } else {
      leaders.splice( $.inArray(lgid, leaders), 1 );
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


  $('#timeBlocks').on('change', '.timeCheckbox', function() {
    var id = $(this).attr("data-block-id");
    console.log("id:");
    console.log(id);
    if(this.checked) { // checkbox is checked
      time_blocks[id];
      user_schedule[id] = {day: time_blocks[id]['day'], start: time_blocks[id]['start'], end: time_blocks[id]['end']};
    } else { // unchecked
      delete user_schedule[id];
    }
    console.log(user_schedule);
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
      schedule: user_schedule,
      preferred_leaders: leaders
    }

    var user_id = num_users+1;
    users[user_id] = user;
    console.log(users);

    // Update user table
    updateUserTable(user);

    // Add new user to DB
    updateDB(user);

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
