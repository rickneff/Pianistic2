(function() {
  // pianistic.js must run before this
  var app = angular.module('pianistic');

  app.controller("PianoController", ['$http', function($http){
    var pianistic = this;
    pianistic.piano = {};
    pianistic.service_history = [];

    // This gets the number we tacked onto the query string
    // and uses it to get the appropriate piano.
    var pianoId = window.location.search.substring(1);
    $http.get('/piano?id=' + pianoId).success(function(data) {
      pianistic.piano = data;
      pianistic.piano.age = pianistic.getAge(pianistic.piano.year);

      var lsdate = new Date(pianistic.piano.last_service_date);
      var days = pianistic.piano.service_interval - Math.floor(Math.abs(new Date() - lsdate) / (1000 * 60 * 60 * 24));

      pianistic.piano.next_service = days;
    });

    $http.get('/service_records?piano_id=' + pianoId).success(function(data) {
      pianistic.service_history = data;
    });


    this.addRecord = function() {
      var fields = [
        'date',
        'action',
        'technician',
        'temperature',
        'humidity',
        'pitch',
        'resetInterval'
      ];

      var form = {'piano_id' : pianistic.piano.id}

      for (field in fields) {
        if (document.getElementById(fields[field]).value != "") {
          form[fields[field]] = document.getElementById(fields[field]).value;
        }
      }

      $http.post('/service_record', form
      ).success(function(data){
        $http.get('/service_records?piano_id=' + pianoId).success(function(data) {
          pianistic.service_history = data;
        });
        document.getElementById("recordForm").reset();
        $("#addRecordModal").modal('hide');
      }).error(function(data){
        console.log(data);
        alert("Error: " + data.error);
      });
    };

    this.updatePiano = function() {
      var fields = [
        'building',
        'room',
        'room_type',
        'make',
        'model',
        'type',
        'year',
        'condition',
        'mfg_serial',
        'inventory_id',
        'cost',
        'value',
        'service_interval',
        'previous_building',
        'previous_room',
        'service_notes',
        'notes'
      ];

      var form = {'id' : pianistic.piano.id};

      for (field in fields) {
        form[fields[field]] = document.getElementById(fields[field]).value;
      }

      $http.post('/piano', form
      ).success(function(data){
        $http.get('/piano?id=' + pianoId).success(function(data) {
          pianistic.piano = data;
          pianistic.piano.age = pianistic.getAge(pianistic.piano.year);

          var lsdate = new Date(pianistic.piano.last_service_date);
          var days = pianistic.piano.service_interval - Math.floor(Math.abs(new Date() - lsdate) / (1000 * 60 * 60 * 24));

          pianistic.piano.next_service = days;
        });

        $("#editModal").modal('hide');
      }).error(function(data){
        console.log(data);
        alert("Error: " + data.error);
      });
    };


    this.getAge = function(year) {
      return (new Date()).getFullYear() - year;

    };
  }]);
})();
