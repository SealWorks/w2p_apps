document.addEventListener('DOMContentLoaded', function() {
  var mainNav = M.Sidenav.init(document.querySelectorAll('#main-nav'), null);
  var userNav = M.Sidenav.init(document.querySelectorAll('#user-nav'), {edge: 'right'});
});