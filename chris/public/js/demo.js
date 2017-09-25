var name = "";
var leaders = [];
var member = true;
var leader = false;

// $(function() {
//   $("#submit").click(function() {
//     alert('submit')
//     $("#member").html() = member;
//     $("#leader").html() = leader;
//
//     $('#submitResults').toggle();
//   })
// });

$(document).ready(function(){
    $(".submit").click(function(){

      $("#name").html($("#nameInput").val());
      $("#member").html(member);
      $("#leader").html(leader);
      $("#leaders").html(leaders.toString());

      $("#submitResults").show();
  });
});

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
