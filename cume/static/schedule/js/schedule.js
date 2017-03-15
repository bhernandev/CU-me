let college_dictionary = {
  "Baruch College": "BAR01",
  "Borough of Manhattan CC": "BMC01",
  "Bronx Community College": "BCC01",
  "Brooklyn College": "BCC01",
  "CUNY School of Law": "LAW01",
  "CUNY School of Medicine": "MED01",
  "CUNY School of Public Health": "SPH01",
  "City College": "CTY01",
  "College of Staten Island": "CSI01",
  "Guttman Community College": "NCC01",
  "Hostos Community College": "HOS01",
  "Hunter College": "HTR01",
  "John Jay College": "JJC01",
  "Kingsborough CC": "KCC01",
  "LaGuardia Community College": "LAG01",
  "Lehman College": "LEH01",
  "Medgar Evers College": "MEC01",
  "NYC College of Technology": "NYT01",
  "Queens College": "QNS01",
  "Queensborough CC": "QCC01",
  "School of Professional Studies": "SPS01",
  "The Graduate Center": "GRD01",
  "York College": "YRK01"
}
let searchFormShown = false;
let searching = false
$(document).ready(function() {
  $('.reqContainer').each(function(i) {
    $(this).hide()
  })
  $('#searchHidden').height($('#searchHidden').children('img').height());
  $('header').height($('#logo img').height());
  $('#searchHidden').hide()
  $('#degreeContent').height($('#degree').height() - $('#degreeCollapse').height())
  let degreeOpen = true
  let searchOpen = true

  let newUser = $('#newUser').val()
  if (newUser) {
    $('#newUser').val('')
    $('#tut5').popup({
      type: 'overlay',
      horizontal: 'center',
      vertical: 'center',
      transition: 'all 0.3s',
      opacity: 0.8,
    })
    $('#tut4').popup({
      type: 'tooltip',
      horizontal: 'center',
      vertical: 'top',
      transition: 'all 0.3s',
      opacity: 0.8,
      tooltipanchor: $('#schedule'),

      onclose: function() {
        $('#tut5').popup('show')
      }
    })
    $('#tut3').popup({
      type: 'tooltip',
      horizontal: 'left',
      vertical: 'top',
      transition: 'all 0.3s',
      opacity: 0.8,
      tooltipanchor: $('#search'),
      offsetleft: 350,

      onclose: function() {
        $('#tut4').popup('show')
      }
    })
    $('#tut2').popup({
      type: 'tooltip',
      horizontal: 'center',
      vertical: 'top',
      transition: 'all 0.3s',
      opacity: 0.8,
      tooltipanchor: $('#degree'),
      offsetleft: 160,

      onclose: function() {
        $('#tut3').popup('show')
      }
    })
    $('#tut1').popup({
      type: 'overlay',
      horizontal: 'center',
      vertical: 'center',
      transition: 'all 0.3s',
      opacity: 0.8,
      autoopen: true,
      detach: true,

      onclose: function() {
        $('#tut2').popup('show')
      }
    })
  }

  $('#help').popup({
    type: 'overlay',
    horizontal: 'center',
    vertical: 'center',
    transition: 'all 0.3s',
    opacity: 0.8
  })
  $('#about').popup({
    type: 'overlay',
    horizontal: 'center',
    vertical: 'center',
    transition: 'all 0.3s',
    opacity: 0.8
  })

  $('#degreeCollapse').click(function() {
    let newWidth = 0
    if (degreeOpen) {
      degreeOpen = false

      $('#degreeContent').hide()
      $('#degreeCollapse').html('>>')

      newWidth = 22
      $(this).parent().animate({width: "3%"}, "fast")
    }
    else {
      degreeOpen = true

      $('#degreeContent').show()
      $('#degreeCollapse').html('Core classes left to complete')

      newWidth = -22
      $(this).parent().animate({width: "25%"}, "fast")
    }

    updateWidth(newWidth, 0)
  })
  $('#searchCollapse').click(function() {
    let newWidth = 0
    if (searchOpen) {
      searchOpen = false

      $('#searchContent').hide()
      $('#searchCollapse').html('<<')

      newWidth = 22
      $(this).parent().animate({width: "3%"}, "fast")
    }
    else {
      searchOpen = true

      $('#searchContent').show()
      $('#searchCollapse').html('Search')

      newWidth = -22
      $(this).parent().animate({width: "25%"}, "fast")
    }

    updateWidth(0, newWidth)
  })

  $('.req').click(function() {
    $(this).next().toggle('fast')
  })

  $('#searchForm').submit(function(e) {
    if (searching)
      return false
    searching = true
    let college = $('select[name=collegeSelect]').val()
    let term = $('select[name=termSelect]').val()
    let dept = $('select[name=courseSelect]').val()

    let courseNbr = $('#numberInput').val()
    let contains = $('select[name=containsSelect]').val()

    let session = $('select[name=sessionSelect]').val()
    let classNbr = $('#classNumberInput').val()
    let courseCareer = $('select[name=careerSelect]').val()
    let reqdes = $('select[name=reqDesignationSelect]').val()
    let instructorName = $('#instructorInput').val()
    let instructorContains = $('select[name=instructorContainsSelect]').val()

    searchClasses(college, term, dept, session, contains, courseNbr, classNbr, courseCareer, reqdes, instructorName, instructorContains, function() {
      searching = false
    })
    return false
  })

  $('#searchContent').on('click', '.add', function() {
    let addCourse = $(this).parent().prevAll('.courseResult').first().text()
    let addTimes = $(this).parent().find('.times').text()
    let addInstructor = $(this).parent().find('.instructor').text()
    let addGrades = []
    $(this).parent().find('.grades').find('p').each(function(i) {
      addGrades.push($(this).text())
    })
    let addGradesString = addGrades.toString()
    let addRoom = $(this).parent().find('.room').text()
    let addDates = $(this).parent().find('.dates').text()
    addClass(addTimes, addCourse, addInstructor, addGradesString, addRoom, addDates, false, false)
  })

  $('.degreeClass').click(function(e) {
    e.preventDefault()
    if (searching)
      return false
    searching = true
    let college = college_dictionary[$('#collegeName').text()]
    let term = '1172'
    let linkString = $(this).text()
    linkList = linkString.split(' ')
    let dept = linkList[0]
    let courseNbr = linkList[1]
    let contains = 'E'
    let session = ''
    searchClasses(college, term, dept, session, contains, courseNbr, function() {
      searching = false
    })
    return false
  })

  $('#searchHidden').hover(function() {
    if (!searching) {
      searchFormShown = true;
      $('#searchForm').show('fast')
      $('#searchHidden').hide('fast')
      clearInterval(searchHoverChecker)
      searchHoverChecker = setInterval(checkSearchHover, 800)
    }
  })
  let searchHoverChecker = setInterval(checkSearchHover, 800)
})

function updateWidth(degreeUpdateWidth, searchUpdateWidth) {
  let currentScheduleWidth = $('#schedule').width() / $('#schedule').parent().width() * 100
  let scheduleWidth = currentScheduleWidth + degreeUpdateWidth + searchUpdateWidth
  let scheduleWidthString = scheduleWidth + "%"
  $('#schedule').animate({width: scheduleWidthString}, "fast", function() {
    redrawSchedule()
  })
}

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest()
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText)
  }
  xmlHttp.open("GET", theUrl, true) // true for asynchronous
  xmlHttp.send(null)
}

function searchClasses(college, term, dept, session, contains, courseNbr, classNbr, courseCareer, reqdes, instructorName, instructorContains, callback) {
  $('#searchResults').empty()
  $('#searchResults').append('<div class="progress"><p id="step">Searching for classes</p></div>')
  $('#searchResults').append('<div class="spinner spinnerSearch"><div class="double-bounce1"></div><div class="double-bounce2"></div></div>')

  let apiURL = "https://cufor.me/api/search/"
  let payload = "?college=" + college + "&term=" + term + "&dept=" + dept + "&session=" + session + "&contains=" + contains + "&courseNbr=" + courseNbr + "&classNbr=" + classNbr + "&courseCareer=" + courseCareer + "&reqdes=" + reqdes + "&instructor=" + instructorName + "&instrContains=" + instructorContains  
  let fullURL = apiURL + payload
  $.ajax({
    url: fullURL,
    type: 'GET',
    data: {
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    },
    success: function(data) {
      let json = data
      if (!json.hasOwnProperty('error')) {
        let courseLength = json.courses.length

        $('#searchResults').empty()
        let resultNum = 0
        for (let i = 0; i < courseLength; i++) {
          let course = json.courses[i]
          let courseName = course.courseName
          let sectionLength = course.sections.length
          $('#searchResults').append('<div class="courseResult"><hr><p><b>' + courseName + '</b></p></div>')
          for (let j = 0; j < sectionLength; j++) {
            let section = course.sections[j]

            let times = section.times
            let instructor = section.instructor
            let grades = ""
            if (!jQuery.isEmptyObject(section.instructorGrades))
              grades = '<div class="grades"><img class="rmpImg" src="/static/schedule/img/rmpLong.png"><div class="gradeId"><p>Overall</p><p>Difficulty</p></div><div><p>' + section.instructorGrades.overall + "</p><p>" + section.instructorGrades.difficulty + "</p></div></div>"
            let room = section.room
            let dates = section.meetingDates

            let newDiv = ""
            if (grades != "")
              newDiv = '<div class=result id="result' + resultNum + '"><p class="times">' + times + '</p>' + '<p class="instructor">' + instructor + '</p>' + grades + '<p class="room">' + room + '</p>' + '<p class="dates">' + dates + '</p>' + '<img class="add" src="/static/schedule/img/add.png" alt="Add Class"></div>'
            else
              newDiv = '<div class=result id="result' + resultNum + '"><p class="times">' + times + '</p>' + '<p class="instructor">' + instructor + '</p>' + '<p class="room">' + room + '</p>' + '<p class="dates">' + dates + '</p>' + '<img class="add" src="/static/schedule/img/add.png" alt="Add Class"></div>'

            if (j != 0)
              $('#searchResults').append('<hr class="smallLine">')
            $('#searchResults').append(newDiv)

            resultNum++
          }
        }
      }
      else {
        console.log(json.error)
        $('#searchResults').empty()
        if (json.error == "Not found") {
          $('#searchResults').append('<p class="error"><b>No results found :(</b></p>')
        }
        else {
          $('#searchResults').append('<p class="error"><b>Could not connect to CUNYFirst.</b></p><p class="error"><b>(it may be down)</b></p>')
        }
      }
      $('#searchForm').hide()
      $('#searchHidden').show()
      callback()
    }
  })
}

function checkSearchHover() {
  if (!$('#searchForm').is(":hover") && searchFormShown && !searching) {
    searchFormShown = false;
    $('#searchForm').hide('fast')
    $('#searchHidden').show('fast');
  }
}
