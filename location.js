(function() {
  // pianistic.js must run before this
  var app = angular.module('pianistic');

  app.controller("LocationController", [function(){
    var pianistic = this;

    // This gets the building and room from the query string
    pianistic.building = decodeURI(window.location.search.substring(1)).split("&");
    pianistic.room = pianistic.building[1];
    pianistic.building = pianistic.building[0];

  }]);
})();
