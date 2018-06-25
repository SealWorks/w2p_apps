document.addEventListener('DOMContentLoaded', function() {
    var mainNav = M.Sidenav.init(document.querySelectorAll('#main-nav'), null);
    var userNav = M.Sidenav.init(document.querySelectorAll('#user-nav'), {edge: 'right'});
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, {accordion: true});
});