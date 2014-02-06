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
    .controller("MakeConnectionCtrl", function ($scope, $location) {
        $scope.isLoggedIn = pimp.user !== undefined;
        $scope.twitterHandle = null;

        $scope.doSubmit = function() {
            if ($scope.isLoggedIn) {
                $location.path("/connection/pitch/" + $scope.normalizedTwitterHandle());
            } else {
            }
        };

        $scope.normalizedTwitterHandle = function() {
            if ($scope.twitterHandle && $scope.twitterHandle !== null && $scope.twitterHandle.match(/^@.*/)) {
                return $scope.twitterHandle.substring(1);
            } else {
                return $scope.twitterHandle;
            }
        }
        $scope.loginUrl = function () {
            return '/login/twitter/?next=/%23/connection/pitch/' + $scope.normalizedTwitterHandle();
        };

        $scope.connectUrl = function () {
            return "#/connection/pitch/" + $scope.normalizedTwitterHandle();
        };
    })
    .controller("WritePitchCtrl", function ($scope, Restangular, $timeout, $routeParams, $location) {
        $scope.connection = {
            twitterHandle: $routeParams.twitterHandle,
            pitch: null
        };

        $scope.user = Restangular.one("user", pimp.user.username).get();
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
                        $scope.requestIntroduction();
                    } else {
                        $timeout($scope.updatePerson, 1000);
                    }
                });
        };


        $scope.requestIntroduction = function () {
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

        $scope.createIntro = function () {
            $location.path("/profile");
        };

        if ($routeParams.twitterHandle) {
            $scope.lookupPerson();
        }
    })
    .controller("ConnectionsCtrl", function ($scope, Restangular) {
        $scope.queryString = null;
        Restangular.all("connection").getList().then(function (response) {
            var fixedResponse = response.map(function (connection) {
                connection.title = "ntro - Connect With Anyone";
                connection.pitch = "Hey Mark, we'have this great idea of making money with connections. People with connection can make money utilizing their network for the benefit of everyone. Introduce hi-quality people to highly-connected people for the benefit of both. Love to hear from you.";
                connection.website = "http://ntro.co";
                return connection;
            });
            $scope.connections = fixedResponse;
        });
    })
    .controller("ProfileCtrl", function ($scope, Restangular) {
        $scope.user = Restangular.one("user", pimp.user.username).get();
        Restangular.all("connection").getList().then(function (response) {
            var fixedResponse = response.map(function (connection) {
                connection.title = "ntro - Connect With Anyone";
                connection.pitch = "Hey Mark, we'have this great idea of making money with connections. People with connection can make money utilizing their network for the benefit of everyone. Introduce hi-quality people to highly-connected people for the benefit of both. Love to hear from you.";
                connection.website = "http://ntro.co";
                return connection;
            });
            $scope.myConnections = fixedResponse;
        });
    })
    .controller("NavCtrl", function ($scope, $location) {
        $scope.isLoggedIn = pimp.user !== undefined;
        $scope.isHomeActive = function () {
            return $location.path().match(/^\/$/);
        };
        $scope.isConnectionsActive = function () {
            return $location.path().match(/^\/connections$/);
        };
        $scope.isProfileActive = function () {
            return $location.path().match(/^\/profile$/);
        };
    });
