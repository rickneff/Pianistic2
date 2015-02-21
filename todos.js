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

    this.newTodo = function() {
      if (!document.getElementById("notes").value) {
        alert("Notes field is mandatory");
        return;
      }

      $http.post('/todo', {
        'building':document.getElementById("building").value,
        'room':document.getElementById("room").value,
        'mfg_serial':document.getElementById("mfg_serial").value,
        'notes':document.getElementById("notes").value
      }).success(function(data){
        document.getElementById("submitTodo").reset();

        $http.get('/todos').success(function(data){
          pianistic.todos = data;
          pianistic.numTodos = pianistic.todos.length;
        });
      }).error(function(data){
        alert(data['error']);
      });
    };
  }]);
})();

