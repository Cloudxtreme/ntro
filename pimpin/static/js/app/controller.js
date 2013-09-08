angular
    .module("pimp.app", ["pimp.config", "pimp.api"])
    .config(function ($routeProvider) {
        var partialsUrl = "/static/partials/"
        $routeProvider
            .when("/", {templateUrl: partialsUrl + "home.html", controller: "MakeConnectionCtrl"})
            .when("/connection/pitch/:twitterHandle", {templateUrl: partialsUrl + "writePitch.html", controller: "WritePitchCtrl"})
            .when("/connections", {templateUrl: partialsUrl + "connections.html", controller: "ConnectionsCtrl"})
            .when("/profile", {templateUrl: partialsUrl + "profile.html", controller: "ProfileCtrl"})
            .otherwise({redirectTo: "/"});
    })
    .controller("MakeConnectionCtrl", function ($scope) {
        $scope.isLoggedIn = pimp.user !== undefined;

        $scope.loginUrl = function() {
            return '/login/twitter/?returnUrl=/connection/pitch/' + $scope.twitterHandle;
        };

        $scope.connectUrl = function() {
            return "#/connection/pitch/" + $scope.twitterHandle;
        };
    })
    .controller("WritePitchCtrl", function ($scope, Restangular, $timeout, $routeParams) {
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
            Restangular.all("connection").post({person: "/api/v1/person/" + $scope.connection.twitterHandle + "/"})
                .then(function (connection) {
                    if (connection.statusCode() === 201) {
                        var absResourcePath = connection.headers().location;
                        var items = absResourcePath.split("/");
                        var connectionId = items[items.length - 2];
                        $scope.updateConnection(connectionId)
                    } else {
                        $scope.updateConnection(connection.id)
                    }
                });
        };

        $scope.updateConnection = function (connectionId) {
            Restangular.one("connection", connectionId).get().
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

        $scope.createIntro = function() {
            $scope.connection.put();
        };

        if ($routeParams.twitterHandle) {
            $scope.lookupPerson();
        }
    })
    .controller("ConnectionsCtrl", function ($scope, Restangular) {
        $scope.queryString = null;
        $scope.connections = Restangular.all("connection").getList();
    })
    .controller("ProfileCtrl", function($scope, Restangular) {
        $scope.user = Restangular.one("user", pimp.user.username);
        $scope.connections = Restangular.all("connection").getList();
    });
