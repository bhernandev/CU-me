$(document).ready(function() {
  let loggingIn = false
  $('#step').html('Logging you in :)')
  $('#step').css('visibility', 'hidden')
  $('#login').height($('#login').height() + 30)
  $('#loginForm').submit(function(e) {
    if (loggingIn)
      e.preventDefault()
    else {
      loggingIn = true
      $('#step').css('visibility', 'visible')
      $('#login').append('<div class="spinner spinnerLogin"><div class="double-bounce1"></div><div class="double-bounce2"></div></div>')
      let willstop = 0
      var poll = function() {
        $.ajax({
          url:'poll_state/',
          type: 'POST',
          data: {
              csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
              id: $('#id').val(),
          },
          success: function(pollResult) {
            step = pollResult.data
            if (step == 'Done')
              willstop = 1
            $('#step').html(step)
          }
        })
      }
      let refreshIntervalId = setInterval(function() {
        poll()
        if(willstop == 1){
          clearInterval(refreshIntervalId);
        }
      }, 500)
    }
  })
})
