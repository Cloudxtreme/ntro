angular
    .module("pimp.app", ["pimp.config", "pimp.api"])
    .config(function ($routeProvider) {
        var partialsUrl = "/static/partials/"
        $routeProvider
            .when("/", {templateUrl: partialsUrl + "makeConnection.html", controller: "MakeConnectionCtrl"})
            .when("/connection/make", {templateUrl: partialsUrl + "makeConnection.html", controller: "MakeConnectionCtrl"})
            .when("/connection/pitch/:twitterHandle", {templateUrl: partialsUrl + "writePitch.html", controller: "WritePitchCtrl"})
            .when("/connections", {templateUrl: partialsUrl + "connections.html", controller: "ConnectionsCtrl"})
            .otherwise({redirectTo: "/"});
    })
    .controller("MakeConnectionCtrl", function ($scope, $location) {
        $scope.isLoggedIn = pimp.user !== undefined;

        $scope.loginUrl = function() {
            return '#/login/twitter/?returnUrl=/connection/pitch/' + $scope.twitterHandle;
        }
    })
    .controller("WritePitchCtrl", function ($scope, Restangular, $timeout, $routeParams) {
        debugger;
        $scope.connection = {
            twitterHandle: $routeParams.twitterHandle,
            pitch: null
        };

        $scope.step = "enterName";
        $scope.lookupInProgress = false;
        $scope.person = null;

        $scope.lookupPerson = function () {
            $scope.lookupInProgress = true;
            $scope.person = null;

            Restangular.all("person").post({twitter_handle: $scope.connection.twitterHandle})
                .then(function () {
                    $scope.updatePerson();
                }, function (response) {
                    $scope.error = "Person not found";
                    $scope.lookupInProgress = false;
                });
        };

        $scope.updatePerson = function () {
            Restangular.one("person", $scope.connection.twitterHandle).get()
                .then(function (person) {
                    if (person.score && person.score !== null) {
                        $scope.person = person;
                        $scope.lookupInProgress = false;
                        $scope.step = "lookupSuccessful";
                    } else {
                        $timeout($scope.updatePerson, 1000);
                    }
                });
        };


        $scope.requestIntroduction = function () {
            $scope.step = "requestIntroduction";
            Restangular.all("connection").post({person: $scope.connection.twitterHandle})
                .then(function (connection) {
                    $scope.updateConnection(connection);
                });
        };

        $scope.updateConnection = function (connection) {
            Restangular.one("connection", connection.id).get().
                then(function (connection) {
                    if (connection.price && connection.price !== null) {
                        $scope.connection = connection;
                    } else {
                        $timeout(function () {
                            $scope.updateConnection(connection.id);
                        }, 1000);
                    }
                });
        };

        $scope.topUsers = Restangular.all("user").getList();
    })
    .controller("ConnectionsCtrl", function ($scope, Restangular) {
        $scope.queryString = null;
        $scope.connections = Restangular.all("connection").getList();
    });
