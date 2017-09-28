/********** DUMMY VARS ************/
var time_blocks = {
  monday: {0:"12-14", 1:"16-18", 2:"20-22"},
  tuesday: {0:"14-18"},
  wednesday: {0:"12-14", 1:"16-18", 2:"20-22"},
  thursday: {0:"10-12", 1:"18-20"},
  friday: {0:"12-14", 1:"16-18", 2:"20-22"},
  saturday: {0:"12-16", 1:"17-19"},
  sunday: {0:"10-14"}
}

$(document).ready(function(){

  var blocks = findUniqueTimeBlocks(time_blocks);
  console.log(blocks);
  displaySchedule(blocks);

});

function displaySchedule(unique_blocks) {
  for(var i = 0; i < unique_blocks.length; i++) {
    block = unique_blocks[i];
    var newRow = $("<tr>");
    var cols = "";

    cols += '<td><strong>' + block + '</strong></td>';

    newRow.append(cols);
    $("table.schedule-table").append(newRow);
  }
}



function findUniqueTimeBlocks(time_blocks) {
  var unique_blocks = [];
  for(var i in time_blocks){
    var day = time_blocks[i];
    for(var j in day){
      var block = day[j];
      if ($.inArray(block, unique_blocks) == -1) { //if the block isn't in the array, add it
        unique_blocks.push(block);
      }
    }
  }
  return unique_blocks;
}

function showSchedule() {
  $(".user-list").hide();
  $(".schedule").show();
}
