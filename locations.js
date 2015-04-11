(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("LocationsController", [function(){
    var pianistic = this;
    pianistic.building = "None";

    this.set = function(building) {
      pianistic.building = building;
    };
  }]);
})();

