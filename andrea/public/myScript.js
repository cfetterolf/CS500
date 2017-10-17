//INSERT JAVASCRIPT/JQUERY HERE

//Notes
// no "-" in js
// use camel case e.g. myName, emailAd
// later TO DO: make this into an object per user

var name, email, member, leader, avail;
name = ""; email = ""; avail = [];
member = false; leader = false;

function submitFunction() {
  //alert("Form submitted!");
  document.getElementById("submit_confirm").innerHTML =
  "You submitted the form!";

  // SET VARIABLES
  name = document.getElementById("name-input").value;
  email = document.getElementById("email");
  //Doesn't work
  //alert(document.getElementById("name-input").value); //Works!!!
  //alert(document.getElementById("name-input"));
  //alert(document.getElementById("name-input")[0].value);

  member = document.getElementById("member-input").checked;
  leader = document.getElementById("leader-input").checked;

  // OUTPUT

  // Output Hard Code Testing
  //document.getElementById("name_out").innerHTML = "name outputs here";
  //document.getElementById("email_out").innerHTML = "email outputs here";

  // Output: Name and Email
  document.getElementById("name_out").innerHTML = name;
  document.getElementById("email_out").innerHTML = email.value;

  // Output: Member and Leader
  document.getElementById("member_out").innerHTML = member;
  document.getElementById("leader_out").innerHTML = leader;

  //Testing
  //if (document.getElementById("avail_M").checked) alert("Monday checked!");
  //if (document.getElementById("avail_M".checked)) avail.push("avail_M".value);

  //Hard Coded: Pushing Avail Times to Array
  /*
  if (document.getElementById("avail_M").checked) avail.push("M");
  if (document.getElementById("avail_Tu").checked) avail.push("Tu");
  if (document.getElementById("avail_W").checked) avail.push("W");
  if (document.getElementById("avail_Th").checked) avail.push("Th");
  if (document.getElementById("avail_F").checked) avail.push("F");

  //Testing
  if (document.getElementById("avail_M").checked) {
    avail.push(document.getElementById("avail_M").value);
    //avail.push("Monday");
  }*/
  //pushToArray("avail_Tu");
  //avail.push("Kiwi");
  //document.getElementById("avail_out").innerHTML = avail.toString();
  pushToArray("avail_M");
  pushToArray("avail_Tu");
  pushToArray("avail_W");
  pushToArray("avail_Th");
  pushToArray("avail_F");
  document.getElementById("avail_out").innerHTML = avail.join(", ");
}


function pushToArray(timeAvailID) {
  if (document.getElementById(timeAvailID).checked) {
    avail.push(document.getElementById(timeAvailID).value);
  }
}

/*
$(document).ready(function(){
  $("form").submit(function(){
    submitFunction();
    alert("Submitted");
  });
});
*/
