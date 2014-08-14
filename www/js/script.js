/* 
 * File: script.js
 * Author: Matthew Leeds
 * Last Edit: 8.14.2014
 */

var courseData;
var subject;
var course;
var section; 

function main() {
    $.ajax({ url: "fall2014.json", success: function(data) {
            courseData = data;
            addSubjects();
        }
    });
    $('form').submit(function(event) {
        if ($('#username').val().length == 0 || 
            $('#password').val().length == 0) {
            $('#result').empty().append("<p> Please enter login credentials and try again.</p>");
            return false;
        } else if ($('#subjectsSelect').val().length == 0 ||
                   $('#coursesSelect').val().length == 0 ||
                   $('#sectionsSelect').val().length == 0) {
            $('#result').empty().append("<p> Please select a subject, course, and section, then try again.</p>");
            return false;
        } else {
            $('#result').empty().append("Checking myBama...");
            $.ajax({
                url: 'callpython.php',
                type: 'POST',
                dataType: 'json',
                data: { 'username': $('#username').val(),
                        'password': $('#password').val(),
                        'term': $('#termsSelect').val(),
                        'subject': $('#subjectsSelect').val(),
                        'course': $('#coursesSelect').val().substr(0,3),
                        'section': $('#sectionsSelect').val()
                      }, 
                success: function(response) {
                    console.log(response);
                    $('#result').empty().append("<p>" + response + " open spots</p>");
                    }
                });
            return false;
        }
    });
}

// populate a dropdown with Subjects 
function addSubjects() {
    var subjects = [];
    for (var key in courseData) {
        subjects.push(key);
    }
    subjects.sort();
    var $select = $("<select></select>").attr("id", "subjectsSelect")
                                        .attr("onchange", "addCourses()")
                                        .prop("selectedIndex", 0);
    $select.append($("<option></option>"));
    for (var i = 0; i < subjects.length; i++) {
        $select.append($("<option></option>").attr("value", subjects[i])
                                             .text(subjects[i]));
    }
    $("tbody tr:nth-child(4)").empty().append($("<td></td>").text("Select a subject: ")
                                                            .css("text-align", "right"))
                                      .append($("<td></td>").append($select)
                                                            .css("text-align", "left"));
}

// populate a dropdown with courses based on the selected subject
function addCourses() {
    subject = $("#subjectsSelect").val();
    if (subject.length > 0) {
        var courses = []
        for (var key in courseData[subject]) {
            courses.push(key)
        }
        courses.sort();
        var $select = $("<select></select>").attr("id", "coursesSelect")
                                            .attr("onchange", "addSections()")
                                            .prop("selectedIndex", 0);
        $select.append($("<option></option>"));
        for (var i = 0; i < courses.length; i++) {
            $select.append($("<option></option>").attr("value", courses[i])
                                                 .text(courses[i]));
        }
        $("tr:nth-child(5)").empty().append($("<td></td>").text("Select a course: ")
                                                          .css("text-align", "right"))
                                    .append($("<td></td>").append($select)
                                                          .css("text-align", "left"));
    }
}

function addSections() {
    course = $("#coursesSelect").val();
    if (course.length > 0) {
        var sections = courseData[subject][course];
        var $select = $("<select></select>").attr("id", "sectionsSelect")
                                            .attr("onchange", "enableSubmit()")
                                            .prop("selectedIndex", 0);
        $select.append($("<option></option>"));
        for (var i = 0; i < sections.length; i++) {
            $select.append($("<option></option>").attr("value", sections[i])
                                                 .text(sections[i]));
        }
        $("tr:nth-child(6)").empty().append($("<td></td>").text("Select a section: ")
                                                          .css("text-align", "right"))
                                    .append($("<td></td>").append($select)
                                                          .css("text-align", "left")); 
    }
}

function enableSubmit() {
    $('#checkButton').prop('disabled', false);
}

$(document).ready(function() {
    main();
});
