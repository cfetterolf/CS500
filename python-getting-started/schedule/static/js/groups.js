var selectedGID = 0

$(document).ready(function(){
  getGroups()
  resetSettings()

  // Clicked Group
  $(document).on('click', '.portfolio-item-footer p a', function() {
    setGroupID($(this).attr('data-group-id'));
  });

  // Edit Groups
  $(document).on('click', '#editBtn', function() {
    if ( $('.del-img').css('display') == 'none' ){
      $('.del-img').show()
      $('#editBtn').html('Done')
    } else {
      $('.del-img').hide()
      $('#editBtn').html('Edit')
    }
  });

  // Delete group
  $(document).on('click', '.del-img', function() {
    selectedGID = $(this).attr('data-group-id')
    $('#myModal').modal('show');
  });
  $(document).on('click', '#deleteBtn', function() {
    deleteGroup(selectedGID)
  });


});

function resetSettings() {
  $.get("/ajax/gid/", function(data, status){
    console.log(data);
  })
}


/******** DATABSE FUNCTIONS **********/

function getGroups() {
  $.get("/ajax/db/groups/", function(data, status){
    displayGroups(data)
  })
}

function setGroupID(gid) {
  console.log(gid);
  // Set the group ID in python
  $.post( "/ajax/gid/", JSON.stringify({'gid': gid}), function(data, status) {
    console.log("Response:");
    console.log(data);
  });
}

function deleteGroup(gid) {
  $.ajax({
    url: "/groups/del/",
    type: "GET",
    data: {
      gid: gid,
    },
    success: function(response) {
      console.log(response);
    },
    error: function(xhr) {
      console.log(xhr);
    }
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

/***********************************/

function displayGroups(groups) {
  var group_list = document.getElementById('groupItems');
  for (var gid in groups) {
    var html = `
      <div class="col-xs-6 col-md-6 col-lg-4 portfolio-item" style="background-color:  inherit;">
        <div class="padded-item">
          <img class="del-img" data-group-id="`+gid+`" src="/static/img/delete_icon.png"/>
          <div class="portfolio-item-body">
            <h3 class="portfolio-item-title">`+groups[gid].name+`</h3>
            <p>`+groups[gid].term+`</p>
          </div>
          <div class="portfolio-item-footer footer-blue">
            <p><a data-group-id="`+gid+`" href="/" class="btn btn-default"  role="button">Select Group &raquo;</a></p>
          </div>
        </div>
      </div>
    `;
    group_list.innerHTML = html + group_list.innerHTML
  }
}
