/********** USER INFO ***********/
var name = "";
var leaders = [];
var member = true;
var leader = false;
var user_schedule = {
  monday: {0: false, 1: false, 2: false},
  tuesday: {0: false},
  wednesday: {0: false, 1: false, 2: false},
  thursday: {0: false, 1: false},
  friday: {0: false, 1: false, 2: false},
  saturday: {0: false, 1: false},
  sunday: {0: false}
};

/********** DUMMY VARS ************/
var users = {
  user_1: {
    first_name: "Chris",
    last_name: "Fetterolf",
    email: "chris.fetterolf@gmail.com",
    member: true,
    leader: false,
    schedule: {
      monday: {0:"12-14", 1:"16-18", 2:"20-22"},
      wednesday: {0:"12-14", 1:"16-18", 2:"20-22"},
      friday: {0:"12-14", 1:"16-18", 2:"20-22"},
      saturday: {0:"12-16", 1:"17-19"}
    }
  },
  user_2: {
    first_name: "Andrea",
    last_name: "Narciso",
    email: "anarciso@middlebury.edu",
    member: true,
    leader: true,
    schedule: {
      monday: {0:"12-14", 1:"16-18", 2:"20-22"},
      wednesday: {0:"12-14", 1:"16-18", 2:"20-22"},
      friday: {0:"12-14", 1:"16-18", 2:"20-22"},
      saturday: {0:"12-16", 1:"17-19"}
    }
  }
};

var time_blocks = {
  monday: {0:"12-14", 1:"16-18", 2:"20-22"},
  tuesday: {0:"14-18"},
  wednesday: {0:"12-14", 1:"16-18", 2:"20-22"},
  thursday: {0:"10-12", 1:"18-20"},
  friday: {0:"12-14", 1:"16-18", 2:"20-22"},
  saturday: {0:"12-16", 1:"17-19"},
  sunday: {0:"10-14"}
}

/********** ./DUMMY VARS ************/


$(document).ready(function(){
  setUserTable(users);
  displayScheduleData();

  handleUserInfo();
  handleUserList();

});

function displayScheduleData() {

  var i = 0;
  for (var key in time_blocks) {

    var day_blocks = time_blocks[key];
    var day_html = '<div class="col col-3" id="' + key + '"><h5>'+ (key.charAt(0).toUpperCase() + key.slice(1)) +'</h5>';

    for(var i in day_blocks) {
      var block = day_blocks[i];
      day_html += '<div class="form-check"><label class="form-check-label"><input class="form-check-input timeCheckbox" type="checkbox" data-block="' + i +'">' + block + '</input></label></div>';
    }

    if(i < 4) {
      $('.mon-thurs').html( $('.mon-thurs').html() + day_html );
    } else if (i < 7) {
      $('.fri-sun').html( $('.fri-sun').html() + day_html );
    }

    i++;
  }

  // for (var i = 0; i < arrReportscheckBoxItems.length; i++) {
  //     reportscheckBoxhtml += '<label style="font-weight: 600; color: #00467f !important;"><input type="checkbox" value=' + arrReportscheckBoxItems[i] + '>' + arrReportscheckBoxItems[i] + '</label>&nbsp;';
  // }
  // $('#ReportRow > .col-md-12').html(reportscheckBoxhtml);

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
    var day = $(this).parent().parent().parent().attr('id');
    var data_block = $(this).attr("data-block");
    if ($(this).is(":checked")) {
      user_schedule[day][data_block] = true;
    } else {
      user_schedule[day][data_block] = false;
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
  user_schedule = {
    monday: {0: false, 1: false, 2: false},
    tuesday: {0: false},
    wednesday: {0: false, 1: false, 2: false},
    thursday: {0: false, 1: false},
    friday: {0: false, 1: false, 2: false},
    saturday: {0: false, 1: false},
    sunday: {0: false}
  };
}

function showUserList() {
  $(".user-list").show();
  $(".schedule").hide();
}
