$(document).ready(function() {
  let loggingIn = false
  $('#step').html('Logging you in. Sit tight :)')
  $('#step').css('visibility', 'hidden')
  $('#login').height($('#login').height() + 30)
  $('#loginForm').submit(function(e) {
    if (loggingIn)
      e.preventDefault()
    else {
      loggingIn = true
      $('#step').css('visibility', 'visible')
      $('#login').append('<div class="spinner spinnerLogin"><div class="double-bounce1"></div><div class="double-bounce2"></div></div>')
    }
  })
})
