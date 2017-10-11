/********** DUMMY VARS ************/
var time_blocks = {
  0: {day: "monday", start: 12, end: 14},
  1: {day: "monday", start: 16, end: 20},
  2: {day: "tuesday", start: 14, end: 18},
  3: {day: "thursday", start: 16, end: 20},
  4: {day: "friday", start: 11, end: 14},
  5: {day: "friday", start: 16, end: 18},
  6: {day: "sunday", start: 12, end: 15}
}

var final_schedule = {
  0: {time_id: 0, members: ["user_1"], leaders: ["user_2"]},
  1: {time_id: 4, members: ["user_1"], leaders: ["user_2"]}
}





$(document).ready(function(){

  var blocks = findUniqueTimeBlocks(time_blocks);
  console.log(blocks);
  displayCalander(blocks);
  displaySchedule(final_schedule);
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
