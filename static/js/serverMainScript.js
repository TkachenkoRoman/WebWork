
var app = angular.module('serverApp', []);

app.controller('serverController', function($scope, DataService) {
    $scope.socket = DataService.soc;

    $scope.$watch('clientsChange',
     function (newVal, oldVal) { console.log("INSIDE LISTENER!! newVal = " + newVal + "; oldVal = " + oldVal);
                                 $scope.socket = DataService.soc;
                                 });

    console.log("im inside serverController");
    $scope.test = "hello";

});

app.factory("DataService", function () {
    var mySocket = new socket();
    console.log("i`m inside factory");
    return {
        soc: mySocket
    };
});

