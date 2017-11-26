var alg_results;
var group_info;


$(document).ready(function(){
  getGroupInfo()
});


function displaySchedule(schedule) {
  for (var id in schedule) {
    var block = schedule[id];
    var time_block = time_blocks[block['time_id']];
    var members = block['members'];
    var leaders = block['leaders'];
    var row = $('td[data-block-start="'+time_block['start']+'"]')
    row.css("color", "red");
  }
}

function displayCalander(unique_blocks) {
  for(var i = 0; i < unique_blocks.length; i++) {
    block = unique_blocks[i];
    block_arr = block.split("-");
    var newRow = $("<tr>");
    var cols = "";

    cols += '<td data-block-start="'+block_arr[0]+'" data-block-end="'+block_arr[1]+'"><strong>' + formatTimeBlock(block) + '</strong></td>';
    cols += '<td /><td /><td /><td /><td /><td /><td />'

    newRow.append(cols);
    $("table.schedule-table").append(newRow);
  }
}



function findUniqueTimeBlocks(time_blocks) {
  var unique_blocks = [];
  for(var id in time_blocks){
    var block = time_blocks[id];
    var day = block['day'];
    var start = block['start'];
    var end = block['end'];
    var str = start+"-"+end
    if ($.inArray(str, unique_blocks) == -1) { //if the block isn't in the array, add it
      unique_blocks.push(str);
    }
  }
  return unique_blocks;
}

function formatTimeBlock(block) {
  block = block.split('-');
  var new_block = '';
  var start = block[0];
  var end = block[1];

  if (Number(start) < 12) {start+='am';}
  else if (Number(start) == 12) {start += 'pm';}
  else {start = (Number(start) - 12) + 'pm'}

  if (Number(end) < 12) {end+='am';}
  else if (Number(end) == 12) {end += 'pm';}
  else {end = (Number(end) - 12) + 'pm'}

  return start + '-' + end;
}

function showSchedule() {
  $(".user-list").hide();
  $(".schedule").show();
}


/******** DATABSE FUNCTIONS **********/

function getGroupInfo() {
  console.log("requesting data...");
  // Get the group data
  $.get("/ajax/db/", function(data, status){
        group_info = data;
        console.log(data);
        console.log(status);
        users = data.users
        time_blocks = data.time_blocks
        leader_groups = data.leader_groups

        // Set the header
        // $('#groupName').html(data.group_name)
        // $('#groupTerm').html(data.group_term)

        var blocks = findUniqueTimeBlocks(time_blocks);
        displayCalander(blocks);
        //displaySchedule(final_schedule);

        runAlgorithm()
    });
}



/******************   ALGORITHM  *********************/
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

/*****************  END ALGORITHM  *****************/


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
