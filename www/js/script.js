/* File: script.js
 * Author: Matthew Leeds
 * Last Edit: 7.28.2014
 */

function main() {
    $.ajax({ url: "classes.json", success: function(data) {
            console.log(data);
            var select = $("<select/>");
            for (var subject in data) {
                select.append($("<option/>")
                      .attr("value", subject)
                      .text(subject));
            }
            $("#inputform").append(select);
        }
    });
}

$(document).ready(function() {
    main();
});
