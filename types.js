(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("TypesController", ['$http', function($http){
    var pianistic = this;
    pianistic.types = [];

    $http.get('/enum/piano_type').success(function(data){
      pianistic.types = data;
    });
  }]);
})();

