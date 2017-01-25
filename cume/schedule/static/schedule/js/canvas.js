$(document).ready(function() {
  let dayCanvas = document.getElementById('dayCanvas')
  let timeCanvas = document.getElementById('timeCanvas')
  dayCanvas.width = $('#schedule').width()
  dayCanvas.height = $('#schedule').height()
  timeCanvas.width = $('#schedule').width()
  timeCanvas.height = $('#schedule').height()
  let dayContext = dayCanvas.getContext('2d')
  let timeContext = timeCanvas.getContext('2d'),
  width = timeCanvas.width, height = timeCanvas.height

  let rectBounds = []

  dayContext.font = '500 13pt Lato, sans-serif'
  timeContext.font = '500 13pt Lato, sans-serif'

  let days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

  let timeOffset = 3, lineOffset = 7
  let timeWordEnd = timeContext.measureText('00:00am').width + timeOffset + 10, dayWordEnd = 37
  let widthOfSchedule = width - timeWordEnd - lineOffset
  let heightOfSchedule = height - dayWordEnd

  let currentScheduleStartDay = 0, currentScheduleEndDay = 4
  let currentScheduleStartTime = 9, currentScheduleEndTime = 18

  let heightOfScheduleForClasses = 0
  let classCount = 0
  let addedClasses = []

  $(window).resize(function() {
    redrawSchedule()
  })

  $('#schedule').on('mouseenter', '.classOverlay', function() {
    let classId = $(this).attr('id')
    let idSplit = classId.split('-')
    let hoverID = 'classOverlayHover-' + idSplit[1]
    $('#' + hoverID).show('fast')
  })
  $('#schedule').on('click', '.removeClassButton', function() {
    let thisHoverID = $(this).parent().parent().attr('id')
    let idSplit = thisHoverID.split('-')

    let canvasID = 'class' + idSplit[1][0]
    $('#' + canvasID).remove()

    let largestIndex = 0
    while ($('#schedule').find('#classOverlay-' + idSplit[1][0] + largestIndex).length > 0)
      largestIndex++

    for (let i = 0; i < largestIndex; i++) {
      let classID = 'classOverlay-' + idSplit[1][0] + i
      let hoverID = 'classOverlayHover-' + idSplit[1][0] + i
      $('#' + classID).remove()
      $('#' + hoverID).remove()
    }

    let classObject = $.grep(addedClasses, function(item){ return item.id === Number(idSplit[1][0]); })
    deleteClassFromDB(classObject[0].course)
    addedClasses.splice(addedClasses.indexOf(classObject[0]), 1)
    classCount--
  })
  $('#schedule').on('mouseleave', '.classOverlayHover', function() {
    $(this).hide('fast')
  })

  $("#btnSave").click(function() {
    html2canvas($("#schedule"), {
      background: '#FFFFFF',
      onrendered: function(canvas) {
        // Convert and download as image
        let dataURL = canvas.toDataURL('image/png');
        let link = document.createElement('a');
        link.download = "schedule.png";
        link.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        link.click();
      }
    })
  })

  var CP = window.CanvasRenderingContext2D && CanvasRenderingContext2D.prototype;
  if (CP && CP.lineTo) {
    CP.dashedLine = function(x,y,x2,y2,dashArray) {
      if (!dashArray) dashArray=[10,5];
      if (dashLength==0) dashLength = 0.001; // Hack for Safari
      var dashCount = dashArray.length;
      this.moveTo(x, y);
      var dx = (x2-x), dy = (y2-y);
      var slope = dx ? dy/dx : 1e15;
      var distRemaining = Math.sqrt( dx*dx + dy*dy );
      var dashIndex=0, draw=true;
      while (distRemaining>=0.1) {
        var dashLength = dashArray[dashIndex++%dashCount];
        if (dashLength > distRemaining) dashLength = distRemaining;
        var xStep = Math.sqrt( dashLength*dashLength / (1 + slope*slope) );
        if (dx<0) xStep = -xStep;
        x += xStep
        y += slope*xStep;
        this[draw ? 'lineTo' : 'moveTo'](x,y);
        distRemaining -= dashLength;
        draw = !draw;
      }
    }
  }

  function addDays(start, end) {
    dayContext.clearRect(0, 0, width, height)

    let numberOfLines = end - start + 2
    for (let i = 0; i <= numberOfLines; i++) {
      if (i < numberOfLines) {
        dayContext.beginPath()
        if (i == 0 || i == numberOfLines - 1)
          dayContext.lineWidth = 2
        else
          dayContext.lineWidth = 1
        dayContext.moveTo(timeWordEnd + i*widthOfSchedule/(numberOfLines - 1), 0)
        dayContext.lineTo(timeWordEnd + i*widthOfSchedule/(numberOfLines - 1), height)
        dayContext.strokeStyle = '#dca2ef'
        dayContext.stroke()
      }

      dayContext.fillStyle = '#44474c'
      dayContext.fillText(days[i], timeWordEnd + i*widthOfSchedule/(numberOfLines - 1) + (widthOfSchedule/(numberOfLines - 1) - dayContext.measureText(days[i]).width)/2 , height/40)
    }
    console.log('added day lines')
  }

  function addTimes(start, end) {
    timeContext.clearRect(0, 0, width, height)

    let numberOfLines = 2 * (end - start) + 1
    for (let i = 0; i < numberOfLines; i++) {
      timeContext.font = '100 13pt Lato, sans-serif'
      timeContext.fillStyle = '#44474c'
      timeContext.textAlign = 'right'
      let time = '', timePost = ''
      if (start + 0.5*i < 13) {
        time = Math.floor(start + 0.5*i)
        timePost = 'am'
      }
      else {
        time = Math.floor(start + 0.5*i) - 12
        timePost = 'pm'
      }
      if (i%2 == 0)
        time += ':00'
      else
        time += ':30'
      time += timePost
      timeContext.fillText(time, timeWordEnd - 10, dayWordEnd + i*heightOfSchedule/numberOfLines + timeOffset)

      timeContext.beginPath()
      timeContext.strokeStyle = '#dca2ef'
      if (i == 0 || i == numberOfLines - 1) {
        timeContext.lineWidth = 2
        timeContext.moveTo(timeWordEnd - lineOffset, dayWordEnd + i*heightOfSchedule/numberOfLines)
        timeContext.lineTo(width, dayWordEnd + i*heightOfSchedule/numberOfLines)
      }
      else
        timeContext.dashedLine(timeWordEnd - lineOffset, dayWordEnd + i*heightOfSchedule/numberOfLines, width, dayWordEnd + i*heightOfSchedule/numberOfLines, [1,2])
      timeContext.stroke()
      //context.lineCap = 'round'
      //context.lineWidth = 2
      //context.dashedLine(20,150,170,10,[30,10,0,10])
    }
    heightOfScheduleForClasses = ((numberOfLines-1)*heightOfSchedule/numberOfLines)
    console.log('added time lines')
  }

  window.addClass = function (times, course, instructor, grades, room, dates, redrawing, fromDB) {
    let newClass = {'id': classCount, 'times': times, 'course': course, 'instructor': instructor, 'grades': grades, 'room': room, 'dates': dates}
    let classExists = containsObject(newClass, addedClasses)
    //to prevent adding the same class to the schedule (creating more than one canvas)
    if (!redrawing && classExists)
      return

    let redrawTime = false, redrawDays = false

    let daysToNums = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    let timesSplit = times.split(" ")
    let daysUnsplit = timesSplit[0]
    let timeStart = timesSplit[1]
    let timeEnd = timesSplit[3]

    let days = []
    for (let i = 0; i < daysUnsplit.length; i+=2) {
      let day = times[i] + times[i+1]
      if (currentScheduleEndDay < daysToNums.indexOf(day)) {
        currentScheduleEndDay = daysToNums.indexOf(day)
        redrawDays = true
      }
      days.push(day)
    }

    let timeStartNum = 0
    if (timeStart.length == 6) {
      let addTwelveHours = 0
      if (timeStart[4] == 'P')
        addTwelveHours = 12

      if (currentScheduleStartTime >= addTwelveHours + Number(timeStart[0])) {
        currentScheduleStartTime = addTwelveHours + Number(timeStart[0]) - 1
        redrawTime = true
      }

      timeStartNum = (addTwelveHours + Number(timeStart[0]))*60 + Number(timeStart[2])*10 + Number(timeStart[3])
    }
    else if (timeStart.length == 7) {
      let addTwelveHours = 0
      if (timeStart[5] == 'P' && timeStart[1] != '2')
        addTwelveHours = 12
      else if (timeStart[5] == 'A' && timeStart[1] == '2')
        timeStart[0] = timeStart[1] = '0'

      if (currentScheduleStartTime >= addTwelveHours + (Number(timeStart[0])*10 + Number(timeStart[1]))) {
        currentScheduleStartTime = addTwelveHours + (Number(timeStart[0])*10 + Number(timeStart[1])) - 1
        redrawTime = true
      }

      timeStartNum = (addTwelveHours + (Number(timeStart[0])*10 + Number(timeStart[1])))*60 + Number(timeStart[3])*10 + Number(timeStart[4])
    }

    let timeEndNum = 0
    if (timeEnd.length == 6) {
      let addTwelveHours = 0
      if (timeEnd[4] == 'P')
        addTwelveHours = 12

      if (currentScheduleEndTime <= addTwelveHours + Number(timeEnd[0])) {
        currentScheduleEndTime = addTwelveHours + Number(timeEnd[0]) + 1
        redrawTime = true
      }

      timeEndNum = (addTwelveHours + Number(timeEnd[0]))*60 + Number(timeEnd[2])*10 + Number(timeEnd[3])
    }
    else if (timeEnd.length == 7) {
      let addTwelveHours = 0
      if (timeEnd[5] == 'P' && timeEnd[1] != '2')
        addTwelveHours = 12
      else if (timeEnd[5] == 'A' && timeEnd[1] == '2')
        timeEnd[0] = timeEnd[1] = '0'

      if (currentScheduleEndTime <= addTwelveHours + (Number(timeEnd[0])*10 + Number(timeEnd[1]))) {
        currentScheduleEndTime = addTwelveHours + (Number(timeEnd[0])*10 + Number(timeEnd[1])) + 1
        redrawTime = true
      }

      timeEndNum = (addTwelveHours + (Number(timeEnd[0])*10 + Number(timeEnd[1])))*60 + Number(timeEnd[3])*10 + Number(timeEnd[4])
    }

    timeStartNum -= currentScheduleStartTime*60
    timeEndNum -= currentScheduleStartTime*60

    if (redrawDays)
      addDays(currentScheduleStartDay, currentScheduleEndDay)
    if (redrawTime)
      addTimes(currentScheduleStartTime, currentScheduleEndTime)
    if (redrawTime || redrawDays) {
      $('.classCanvas').remove()
      $('.classOverlay').remove()
      $('.classOverlayHover').remove()
      classCount = 0
      for (let i = 0; i < addedClasses.length; i++) {
        addClass(addedClasses[i]['times'], addedClasses[i]['course'], addedClasses[i]['instructor'], addedClasses[i]['grades'], addedClasses[i]['room'], addedClasses[i]['dates'], true, false)
      }
    }

    $('#schedule').append('<canvas id=class' + classCount + ' class="classCanvas"><p>Your browser doesn’t currently support HTML5 Canvas. Please check caniuse.com/#feat=canvas for information on browser support for canvas.</p></canvas>')
    let newClassCanvas = document.getElementById('class' + classCount)
    let newClassContext = newClassCanvas.getContext('2d')
    newClassCanvas.width = $('#schedule').width()
    newClassCanvas.height = $('#schedule').height()

    let minutesInSchedule = (currentScheduleEndTime - currentScheduleStartTime) * 60
    let heightOfMinute = heightOfScheduleForClasses/minutesInSchedule

    let classRectY = dayWordEnd + heightOfMinute * timeStartNum
    let rectWidth = widthOfSchedule/(currentScheduleEndDay - currentScheduleStartDay + 1)
    let rectHeight = (timeEndNum - timeStartNum)*heightOfMinute

    newClassContext.fillStyle = 'hsl(' + 360 * Math.random() + ', 50%, 50%)'
    for (let i = 0; i < days.length; i++) {
      let classRectX = timeWordEnd + daysToNums.indexOf(days[i])*rectWidth
      newClassContext.beginPath()
      newClassContext.rect(classRectX, classRectY, rectWidth, rectHeight)
      newClassContext.fill()
      newClassContext.lineWidth = 1
      newClassContext.strokeStyle = 'black'
      newClassContext.stroke()

      let rectGlobalX = $('#schedule').offset().left + classRectX
      let rectGlobalY = $('#schedule').offset().top + classRectY
      // let newRectBounds = {'x1': rectGlobalX,'y1': rectGlobalY, 'x2': rectGlobalX + rectWidth, 'y2': rectGlobalY + rectHeight}
      // rectBounds.push(newRectBounds)
      let courseName = course.split('-')
      $('#schedule').append('<div class="classOverlay" id="classOverlay-' + classCount + i + '"><div><p><b>' + courseName[0] + '</b></p><p>' + instructor + '</p><p>' + room + '</p></div></div>')
      $('#classOverlay-' + classCount + i).css({'top': classRectY, 'left': classRectX, 'width': rectWidth, 'height': rectHeight})
      while ($('#classOverlay-' + classCount + i + ' div').height() >= $('#classOverlay-' + classCount + i).height()) {
        if (parseInt($('#classOverlay-' + classCount + i + ' div').css('font-size')) > 10)
          $('#classOverlay-' + classCount + i + ' div').css('font-size', (parseInt($('#classOverlay-' + classCount + i + ' div').css('font-size')) - 1) + "px" )
        else
          $('#classOverlay-' + classCount + i).css('overflow', 'scroll')
      }

      let gradesArray = grades.split(',')
      if (gradesArray.length > 1) {
        $('#schedule').append('<div class="classOverlayHover" id="classOverlayHover-' + classCount + i + '"><section><div class="removeClassButton">x</div><p>' + courseName[1] + '</p><hr><div class="classOverlayImg"><img src="/static/schedule/img/rmp.png"></div><p class="grade">' + gradesArray[2] + '</p><p class="grade">' + gradesArray[3] + '</p><hr><p>' + dates + '</p></section></div>')
      }
      else
        $('#schedule').append('<div class="classOverlayHover" id="classOverlayHover-' + classCount + i + '"><section><div class="removeClassButton">x</div><p>' + courseName[1] + '</p><p>' + dates + '</p></section></div>')

      $('#classOverlayHover-' + classCount + i).css({'top': classRectY, 'left': classRectX, 'width': rectWidth, 'height': rectHeight})
      while ($('#classOverlayHover-' + classCount + i + ' section').height() >= $('#classOverlayHover-' + classCount + i).height()) {
        if (parseInt($('#classOverlayHover-' + classCount + i + ' section').css('font-size')) > 10)
          $('#classOverlayHover-' + classCount + i + ' section').css('font-size', (parseInt($('#classOverlayHover-' + classCount + i + ' section').css('font-size')) - 1) + 'px')
        // console.log('font size ' + parseInt($('#classOverlayHover-' + classCount + i + ' section').css('font-size')))
        // console.log('width ' + parseInt($('#classOverlayHover-' + classCount + i + ' .classOverlayImg').css('width')))
        if (parseInt($('#classOverlayHover-' + classCount + i + ' section').css('width')) > 33)
          $('#classOverlayHover-' + classCount + i + ' .classOverlayImg').css('width', (parseInt($('#classOverlayHover-' + classCount + i + ' .classOverlayImg').css('width')) - 2) + 'px')

        if (parseInt($('#classOverlayHover-' + classCount + i + ' section').css('width')) <= 33 && parseInt($('#classOverlayHover-' + classCount + i + ' section').css('font-size')) > 10)
          $('#classOverlayHover-' + classCount + i).css('overflow', 'scroll')
        // console.log('inner height ' + $('#classOverlayHover-' + classCount + i + ' section').height())
        // console.log('container height ' + $('#classOverlayHover-' + classCount + i).height())
      }
      $('#classOverlayHover-' + classCount + i).hide()
    }

    if (!classExists) {
      addedClasses.push(newClass)
      if (!fromDB)
        addClassToDB(course, times, instructor, grades, room, dates)
    }

    classCount++
  };

  addDays(currentScheduleStartDay, currentScheduleEndDay)
  addTimes(currentScheduleStartTime, currentScheduleEndTime)

  function containsObject(obj, list) {
    for (let i = 0; i < list.length; i++) {
      if (JSON.stringify(obj, filterOutID) == JSON.stringify(list[i], filterOutID))
        return true
    }
    return false
  }
  function filterOutID(key, value) {
    // Filtering out properties
    if (key == 'id')
      return undefined
    return value
  }

  window.redrawSchedule = function() {
    dayCanvas.width = $('#schedule').width()
    dayCanvas.height = $('#schedule').height()
    timeCanvas.width = $('#schedule').width()
    timeCanvas.height = $('#schedule').height()
    width = timeCanvas.width
    height = timeCanvas.height
    widthOfSchedule = width - timeWordEnd - lineOffset
    heightOfSchedule = height - dayWordEnd
    dayContext.font = '500 13pt Lato, sans-serif'
    addDays(currentScheduleStartDay, currentScheduleEndDay)
    addTimes(currentScheduleStartTime, currentScheduleEndTime)
    $('.classCanvas').remove()
    $('.classOverlay').remove()
    $('.classOverlayHover').remove()
    classCount = 0
    for (let i = 0; i < addedClasses.length; i++) {
      addClass(addedClasses[i]['times'], addedClasses[i]['course'], addedClasses[i]['instructor'], addedClasses[i]['grades'], addedClasses[i]['room'], addedClasses[i]['dates'], true, false)
    }
  };

  function addClassToDB(newClassName, newClassTimes, newClassInstructor, newClassRating, newClassRoom, newClassDates) {
    $.ajax({
      url:'http://104.131.45.74/class_add/',
      type: 'POST',
      data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          name: newClassName,
          times: newClassTimes,
          instructor: newClassInstructor,
          rating: newClassRating,
          room: newClassRoom,
          dates: newClassDates,
      },
      success: function(addResult) {
        let status = addResult.status
      }
    })
  }
  function deleteClassFromDB(removeClassName) {
    $.ajax({
      url:'http://104.131.45.74/class_delete/',
      type: 'POST',
      data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          name: removeClassName
      },
      success: function(deleteResult) {
        let status = deleteResult.status
      }
    })
  }
})
