(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("RoomTypesController", ['$http', function($http){
    var pianistic = this;
    pianistic.roomtypes = [];

    $http.get('/enum/room_type').success(function(data){
      pianistic.roomtypes = data;
    });
  }]);
})();

