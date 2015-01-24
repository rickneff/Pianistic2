(function() {
  var app = angular.module('piano', []);

  app.controller("DBController", ['$http', function($http){
    var pianistic = this;
    pianistic.piano = {};
    pianistic.service_history = [];

    // This gets the number we tacked onto the query string
    // and uses it to get the appropriate piano.
    pianoId = window.location.search.substring(1);
    $http.get('/piano?id=' + pianoId).success(function(data) {
      pianistic.piano = data;
      pianistic.piano.age = pianistic.getAge(pianistic.piano.year);

      var lsdate = new Date(pianistic.piano.last_service_date);
      var days = 180 - Math.floor(Math.abs(new Date - lsdate) / (1000 * 60 * 60 * 24));

      pianistic.piano.next_service = days;
    });

    $http.get('/service_records?piano_id=' + pianoId).success(function(data) {
      pianistic.service_history = data;
    });

    this.getAge = function(year) {
      return (new Date()).getFullYear() - year;
    };

    


  }]);

})();
