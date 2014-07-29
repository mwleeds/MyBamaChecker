/* 
 * File: script.js
 * Author: Matthew Leeds
 * Last Edit: 7.28.2014
 *
 */

var courseData;
var subject;
var course;
var section; 

function main() {
    $.ajax({ url: "classes.json", success: function(data) {
            courseData = data;
            addSubjects();
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
                                        .attr("onchange", "addCourses()");
    for (var i = 0; i < subjects.length; i++) {
        $select.append($("<option></option>").attr("value", subjects[i])
                                             .text(subjects[i]));
    }
    $("tbody tr:nth-child(2)").empty().append($("<td></td>").text("Select a subject: ")
                                                            .css("text-align", "right"))
                                      .append($("<td></td>").append($select)
                                                            .css("text-align", "left"));
}

// populate a dropdown with courses based on the selected subject
function addCourses() {
    subject = $("#subjectsSelect").val();
    var $select = $("<select></select>").attr("id", "coursesSelect")
                                        .attr("onchange", "addSections()");
    var courses = courseData[subject];
    for (var i = 0; i < courses.length; i++) {
        $select.append($("<option></option>").attr("value", courses[i])
                                             .text(courses[i]));
    }
    $("tr:nth-child(3)").empty().append($("</td><td>").text("Select a course: ")
                                                      .css("text-align", "right"))
                                .append($("<td></td>").append($select)
                                                      .css("text-align", "left"));
}

/*function addSections() {
    $("#sectionsSelect").remove();
    course = $("#coursesSelect").val();
    var select = $("<select/>");
    select.attr("id", "sectionsSelect");

}*/

$(document).ready(function() {
    main();
});
