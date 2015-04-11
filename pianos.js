(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("PianosController", ['$http', function($http){
    var pianistic = this;
    pianistic.pianos = [];
    pianistic.numPianos = 0;

    $http.get('/pianos').success(function(data){
      pianistic.pianos = data;
      pianistic.numPianos = pianistic.pianos.length;
      // This is necessary for the search function.  There should
      // really be a better way of doing this.
      for (var i = 0; i < pianistic.pianos.length; i++) {
        pianistic.pianos[i].age = pianistic.getAge(pianistic.pianos[i].year)
        pianistic.pianos[i].days_until_service = pianistic.getDaysToService(pianistic.pianos[i]);
        pianistic.pianos[i].room = parseInt(pianistic.pianos[i].room);
      }
    });

    this.getDaysToService = function(piano) {
      var lsdate = new Date(piano.last_service_date);
      return piano.service_interval - Math.floor(Math.abs(new Date() - lsdate) / (1000 * 60 * 60 * 24));
    };

    this.getAge = function(year) {
      return (new Date()).getFullYear() - year;
    };

    this.cSort = {sortColumn: ['building', 'room'], reverse: false};
    this.sort = function($event, column) {

      if (column == this.cSort.sortColumn ||
          (typeof column == "object" &&
           typeof this.cSort.sortColumn == "object")) {
        this.cSort.reverse = !this.cSort.reverse;

        if (this.cSort.reverse) {
          $event.currentTarget.className = "glyphicon glyphicon-chevron-up";
        } else {
          $event.currentTarget.className = "glyphicon glyphicon-chevron-down";
        }
      } else {
         this.cSort = {sortColumn:column, reverse:false};
        $event.currentTarget.className = "glyphicon glyphicon-chevron-down";

        var reset = document.getElementsByClassName("sorted");
        for (var i = 0; i < reset.length; i++) {
          reset[i].className = "";
        }

        $event.currentTarget.parentNode.className = "sorted";
      }
    };

    this.openPage = function(selectedPiano) {
      window.open("pianoInfo.html?" + selectedPiano.id, "_self");
    };

  }]);
})();

