(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("ModelsController", ['$http', function($http){
    var pianistic = this;
    pianistic.models = [];

    $http.get('/enum/piano_model').success(function(data){
      pianistic.models = data;
    });
  }]);
})();

