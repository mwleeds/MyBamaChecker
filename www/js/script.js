/* 
 * File: script.js
 * Author: Matthew Leeds
 * Last Edit: 8.02.2014
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
    $('#inputform').submit(function(event) {
        $.ajax({
            url: 'callpython.php',
            type: 'POST',
            dataType: 'json',
            data: { 'username': $('#username').val(),
                    'password': $('#password').val(),
                    'term': $('#termsSelect').val(),
                    'subject': $('#subjectsSelect').val(),
                    'course': $('#coursesSelect').val(),
                    'section': $('#sectionsSelect').val()
                  }, 
            success: function(response) {
                console.log(response);
                }
            });
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
                                        .attr("onchange", "addCourses()");
    for (var i = 0; i < subjects.length; i++) {
        $select.append($("<option></option>").attr("value", subjects[i])
                                             .text(subjects[i]))
               .prop("selectedIndex", -1);
    }
    $("tbody tr:nth-child(4)").empty().append($("<td></td>").text("Select a subject: ")
                                                            .css("text-align", "right"))
                                      .append($("<td></td>").append($select)
                                                            .css("text-align", "left"));
}

// populate a dropdown with courses based on the selected subject
function addCourses() {
    subject = $("#subjectsSelect").val();
    var courses = []
    for (var key in courseData[subject]) {
        courses.push(key)
    }
    courses.sort();
    var $select = $("<select></select>").attr("id", "coursesSelect")
                                        .attr("onchange", "addSections()");
    for (var i = 0; i < courses.length; i++) {
        $select.append($("<option></option>").attr("value", courses[i])
                                             .text(courses[i]))
               .prop("selectedIndex", -1);
    }
    $("tr:nth-child(5)").empty().append($("<td></td>").text("Select a course: ")
                                                      .css("text-align", "right"))
                                .append($("<td></td>").append($select)
                                                      .css("text-align", "left"));
}

function addSections() {
    course = $("#coursesSelect").val();
    var sections = courseData[subject][course];
    var $select = $("<select></select>").attr("id", "sectionsSelect")
                                        .attr("onchange", "enableSubmit()");
    for (var i = 0; i < sections.length; i++) {
        $select.append($("<option></option>").attr("value", sections[i])
                                             .text(sections[i]))
               .prop("selectedIndex", -1);
    }
    $("tr:nth-child(6)").empty().append($("<td></td>").text("Select a section: ")
                                                      .css("text-align", "right"))
                                .append($("<td></td>").append($select)
                                                      .css("text-align", "left")); 
}

function enableSubmit() {
    $('#checkButton').prop('disabled', false);
}

$(document).ready(function() {
    main();
});
