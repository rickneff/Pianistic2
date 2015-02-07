(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("BuildingsController", ['$http', function($http){
    var pianistic = this;
    pianistic.buildings = [];

    $http.get('/enum/building').success(function(data){
      pianistic.buildings = data;
    });
  }]);
})();

