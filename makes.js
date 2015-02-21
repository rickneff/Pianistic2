(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("MakesController", ['$http', function($http){
    var pianistic = this;
    pianistic.makes = [];

    $http.get('/enum/piano_make').success(function(data){
      pianistic.makes = data;
    });
  }]);
})();

