/********** GLOBAL VARS ************/
var alg_results;
var users = {};
var time_blocks = {};
var leader_groups = {};
var matched_time_blocks = {};
var group_info;

$(document).ready(function(){
  getGroupInfo();
});

// DELETE LATER
// function displaySchedule() {
//   for (var id in schedule) {
//     var block = time_blocks[id];
//     var day = block['day'];
//     var start = block['start'];
//     var end = block['end'];
//     var day_col = document.getElementById(day);
//     day_col.innerHTML += '<div><div class="" type="checkbox" data-block-id="' + id +'">' + formatTime(start) + ' - ' + formatTime(end) + '</div></label></div>';
//   }
// }

/******** DATABSE FUNCTIONS **********/

function getGroupInfo() {
  console.log("requesting data...");
  // Get the group data
  $.get("/ajax/db/", function(data, status){
        group_info = data;
        // console.log(data);
        // console.log(status);
        users = data.users;
        time_blocks = data.time_blocks;
        leader_groups = data.leader_groups;
        // console.log('Users @ getGroupInfo: ');
        // console.log(users);

        // Set the header
        // $('#groupName').html(data.group_name)
        // $('#groupTerm').html(data.group_term)

        // var blocks = findUniqueTimeBlocks(time_blocks);
        // displayCalendar(blocks);
        //displaySchedule(final_schedule);

        runAlgorithm();
    });
}

/******************   ALGORITHM  *********************/
var indexes = [];
var lg_map = [];
var tb_map = [];
var member_matrix = [];

function runAlgorithm() {
  $.get("/ajax/alg/", function(data, status){
        // console.log(data);
        // console.log(status);
        // users = data.users;
        indexes = data.indexes;
        lg_map = data.lg_map;
        tb_map = data.tb_map;
        member_matrix = data.member_matrix;

        // console.log('Users @ runAlgorithm: ');
        // console.log(users);
        setSchedTable();
    });
}

/*****************  END ALGORITHM  *****************/


/******** HTML/JS OUTPUT FUNCTIONS **********/

function setSchedTable() {
  // console.log("Indices: ");
  // console.log(indexes);
  // console.log("Time Blocks: ");
  // console.log(time_blocks);
  console.log('leader_groups: ');
  console.log(leader_groups);
  console.log('users: ');
  console.log(users);

  for (var tblg_match in indexes) {
    // console.log(tblg_match);
    $("table.schedule-table").append(newRow(tblg_match));
  }
}

function newRow(tblg_match) {
  var tb_index = indexes[tblg_match][0];
  var lg_index = indexes[tblg_match][1];
  var tb_id = tb_map[tb_index];
  var lg_id = lg_map[lg_index];

  //TB Output
  var block = time_blocks[tb_id];
  var day = block.day;
  var start = block.start;
  var end = block.end;
  var tb_output = '<div><div class="" type="" data-block-id="' + tb_id +'">' + day + ' ' + formatTime(start) + ' - ' + formatTime(end) + '</div></label></div>';

  //LG Output
  var lg_user_id = leader_groups[lg_id].leaders;
  var lg_name = users[lg_user_id].first_name + ' ' + users[lg_user_id].last_name;
  var lg_output = '<div><div class="" type="" data-block-id="' + lg_id +'">' + lg_name + '</div></label></div>';

  //Member Output
  var mem_array = member_matrix[tb_index][lg_index];
  var mem_output = '<div><div class="" type="" data-block-id="' + 'mem_' + tb_id +'">';
  for (var mem_index in mem_array) {
    var mem_id = mem_array[mem_index];
    // console.log(mem_id);
    mem_output += users[mem_id].first_name + ' ' + users[mem_id].last_name + '<br>';
  }
  mem_output += '</div></label></div>';

  // Final Row Output
  var newRow = $("<tr data-user-id="+ tblg_match +">");
  var cols = "";

  // console.log('tb_index: ' + tb_index + ', tb_id: ' + tb_id);
  // console.log('lg_index: '+ tb_index + ', lg_id: ' + lg_id);

  cols += '<td>' + tb_output + '</td>';
  cols += '<td>' + lg_output + '</td>';
  cols += '<td>' + mem_output + '</td>';
  // cols += '<td>' + users[user].first_name + ' ' + users[user].last_name + '</td>';
  // cols += '<td>' + users[user].email + '</td>';
  // cols += '<td><a class="show-leader-pref blue-link">Click Here<a></td>';
  newRow.append(cols);
  return newRow;
}

function showSchedule() {
  $(".user-list").hide();
  $(".schedule").show();
}



function formatTime(decimal_time){
 var time = ""+decimal_time;
 time = time.split('.');
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

  minutes = Math.round(60 * (decimal_time - hours));
  timeValue += (minutes < 10) ? ":0" + minutes : ":" + minutes;
  timeValue += (hours >= 12) ? " pm" : " am";  // get AM/PM
  return timeValue;
}
