document.addEventListener('DOMContentLoaded', function() {
    var elems;
    var mainNav = M.Sidenav.init(document.querySelectorAll('#main-nav'), null);
    var userNav = M.Sidenav.init(document.querySelectorAll('#user-nav'), {edge: 'right'});
    elems = document.querySelectorAll('.collapsible');
    var collapsibles = M.Collapsible.init(elems, {accordion: true});
    elems = document.querySelectorAll('.datepicker');
    var datepickers = M.Datepicker.init(elems, {});
    elems = document.querySelectorAll('.timepicker');
    var timepickers = M.Timepicker.init(elems, {});
});