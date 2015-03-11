(function() {
  // Will fail if pianistic.js is not run first
  var app = angular.module('pianistic');

  app.controller("AddPianoController", ['$http', function($http){
    var pianistic = this;
    pianistic.makes = [];

    this.addPiano = function() {
      if (!document.getElementById("mfg_serial").value ||
          !document.getElementById("room").value) {
        alert("Serial # and Room # fields are mandatory");
        return;
      }

      $http.post('/piano', {
        'inventory_id':document.getElementById("inventory_id").value,
        'make':document.getElementById("make").value,
        'model':document.getElementById("model").value,
        'type':document.getElementById("type").value,
        'mfg_serial':document.getElementById("mfg_serial").value,
        'year':document.getElementById("year").value,
        'building':document.getElementById("building").value,
        'room':document.getElementById("room").value,
        'room_type':document.getElementById("room_type").value,
        'condition':document.getElementById("condition").value,
        'notes':document.getElementById("notes").value,
        'cost':document.getElementById("cost").value,
        'value':document.getElementById("value").value,
        'service_interval':document.getElementById("service_interval").value,
        'previous_building':document.getElementById("previous_building").value,
        'previous_room':document.getElementById("previous_room").value,
        'service_notes':document.getElementById("service_notes").value,
        'last_service_date':document.getElementById("last_service_date").value
      }).success(function(data){
        document.getElementById("submitPiano").reset();
      }).error(function(data){
        alert(data['error']);
      });
    };

    $("#last_service_date").datepicker();
    $("#last_service_date").datepicker("option", "dateFormat", "yy-mm-dd");

  }]);
})();

