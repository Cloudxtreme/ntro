angular
    .module("pimp.app", ["pimp.config", "pimp.api"])
    .config(function ($routeProvider) {
        var partialsUrl = "static/partials/"
        $routeProvider
            .when("/", {templateUrl: partialsUrl + "makeConnection.html", controller: "MakeConnectionCtrl"})
            .when("/connection/make", {templateUrl: partialsUrl + "makeConnection.html", controller: "MakeConnectionCtrl"})
            .when("/connections", {templateUrl: partialsUrl + "connections.html", controller: "ConnectionsCtrl"})
            .otherwise({redirectTo: "/"});
    })
    .config(function($locationProvider) {
        $locationProvider.html5Mode(true);
    })
    .controller("MakeConnectionCtrl", function($scope, Restangular, $timeout) {
        $scope.connection = {
            twitterHandle: null,
            pitch: null
        };

        $scope.step = "enterName";
        $scope.lookupInProgress = false;
        $scope.person = null;

        $scope.lookupPerson = function() {
            $scope.lookupInProgress = true;
            $scope.person = null;

            Restangular.one("person", $scope.connection.twitterHandle).get()
                .then(function(person) {
                    if (person === undefined) {
                        $timeout(function() {
                            $scope.lookupPerson();
                        }, 1000);
                    } else {
                        $scope.person = person;
                        $scope.step = "lookupSuccessful";
                        $scope.lookupInProgress = false;
                    }
                }, function(response) {
                    $scope.error = "Person not found";
                    $scope.lookupInProgress = false;
                });
        };
        $scope.gotoPitch = function() {
            $scope.step = "enterPitch";
        };
        $scope.createConnection = function() {
            $scope.step = "confirmation";
        };

        $scope.topUsers = Restangular.all("user").getList();
    })
    .controller("ConnectionsCtrl", function($scope, Restangular) {
        $scope.queryString = null;
        $scope.connections = Restangular.all("connection").getList();
    });
