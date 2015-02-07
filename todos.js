(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("TodosController", ['$http', function($http){
    var pianistic = this;
    pianistic.todos = [];
    pianistic.numTodos = 0;

    $http.get('/todos').success(function(data){
      pianistic.todos = data;
      pianistic.numTodos = pianistic.todos.length;
    });

    this.cSort = {sortColumn: 'id', reverse: false};
    this.sort = function($event, column) {

      if (column == this.cSort.sortColumn) {
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
  }]);
})();

