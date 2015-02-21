(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("ConditionsController", ['$http', function($http){
    var pianistic = this;
    pianistic.conditions = [];

    $http.get('/enum/piano_condition').success(function(data){
      pianistic.conditions = data;
    });
  }]);
})();

