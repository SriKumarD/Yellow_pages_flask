$(document).on('keyup','#search',(e) =>
{
    $("#sform").submit((e) => {
        e.preventDefault(); // prevent actual form submit
        var form = $(this);
        var url = form.attr('action'); //get submit url [replace url here if desired]
        $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes form input
        });
    });
});
$(document).on('keyup','#onup',(e) =>
{
    $("#upform").submit((e) => {
        e.preventDefault(); // prevent actual form submit
        var form = $(this);
        var url = form.attr('action'); //get submit url [replace url here if desired]
        $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes form input
        });
    });
});
$(document).on('keyup','#onEnter',(e) =>
{
    $("#student_form").submit((e) => {
        e.preventDefault(); // prevent actual form submit
        var form = $(this);
        var url = form.attr('action'); //get submit url [replace url here if desired]
        $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes form input
        });
    });
});
$(document).on('keyup','#onUpdate',(e) =>
{
if (e.KeyboardEvent.keyCode === 13) {
    $("#update_form").submit((e) => {
        e.preventDefault(); // prevent actual form submit
        var form = $(this);
        var url = form.attr('action'); //get submit url [replace url here if desired]
        $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes form input
        });
    });
}});

