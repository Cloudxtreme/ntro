angular
    .module("pimp.app", ["pimp.config", "pimp.api"])
    .config(function ($routeProvider) {
        var partialsUrl = "static/partials/"
        $routeProvider
            .when("/home", {templateUrl: partialsUrl + "home.html", controller: "HomeCtrl"})
            .when("/connections", {templateUrl: partialsUrl + "connections.html", controller: "ConnectionsCtrl"})
            .otherwise({redirectTo: "/home"});
    })
    .controller("HomeCtrl", function ($scope, $http) {
        $scope.user = null;

        $http
            .get("static/mock/" + "user.json")
            .success(function (response) {
                $scope.user = response.user;
            });
    })
    .controller("ConnectionsCtrl", function($scope, Restangular) {
        $scope.queryString = null;
        $scope.connections = Restangular.all("connection").getList();
    });
