$(document).ready(function() {
  formJson = jQuery.parseJSON($('#form').val())
  collegesJson = formJson.colleges

  $('select[name="collegeSelect"]').change(function() {
    let collegeCode = $('select[name="collegeSelect"] option:selected').val()
    for (let i = 0; i < collegesJson.length; i++) {
      if (collegesJson[i].code == collegeCode) {
        let termOptions = '<option value=""></option>'
        for (let j = 0; j < collegesJson[i].terms.length; j++)
          termOptions += '<option value="' + collegesJson[i].terms[j].code + '">' + collegesJson[i].terms[j].name + '</option>'
        $('select[name="termSelect"]').html(termOptions)

        let careerOptions = '<option value=""></option>'
        for (let j = 0; j < collegesJson[i].careers.length; j++)
          careerOptions += '<option value="' + collegesJson[i].careers[j].code + '">' + collegesJson[i].careers[j].name + '</option>'
        $('select[name="careerSelect"]').html(careerOptions)

        // let campusOptions = '<option value=""></option>'
        // for (let j = 0; j < collegesJson[i].campuses.length; j++)
        //   campusOptions += '<option value="' + collegesJson[i].campuses[j].code + '">' + collegesJson[i].campuses[j].name + '</option>'
        // $('select[name="campusSelect"]').html(campusOptions)
        //
        // let locationOptions = '<option value=""></option>'
        // for (let j = 0; j < collegesJson[i].locations.length; j++)
        //   locationOptions += '<option value="' + collegesJson[i].locations[j].code + '">' + collegesJson[i].locations[j].name + '</option>'
        // $('select[name="locationSelect"]').html(locationOptions)
      }
    }
  })

  $('select[name="termSelect"]').change(function() {
    let collegeCode = $('select[name="collegeSelect"] option:selected').val()
    let termCode = $('select[name="termSelect"] option:selected').val()
    for (let i = 0; i < collegesJson.length; i++) {
      if (collegesJson[i].code == collegeCode) {
        courseOptions = '<option value=""></option>'
        for (let j = 0; j < collegesJson[i].terms.length; j++) {
          if (collegesJson[i].terms[j].code == termCode) {
            try {
              for (let k = 0; k < collegesJson[i].terms[j].subjects.length; k++)
                courseOptions += '<option value="' + collegesJson[i].terms[j].subjects[k].code + '">' + collegesJson[i].terms[j].subjects[k].name + '</option>'
            }
            catch(err) {
              $('select[name="courseSelect"]').empty()
              return
            }
          }
        }
        $('select[name="courseSelect"]').html(courseOptions)
      }
    }
  })

})
