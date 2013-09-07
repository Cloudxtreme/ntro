angular
    .module("pimp.app", ["pimp.config"])
    .config(function ($routeProvider) {
        $routeProvider
            .when("/home", {templateUrl:  "static/partials/" + "home.html", controller: "HomeCtrl"})
            .otherwise({redirectTo: "/home"});
    })
    .controller("HomeCtrl", function ($scope, $http) {
        $scope.user = null;

        $scope.auth = function () {
            $http
                .get("static/mock/" + "user.json")
                .success(function (response) {
                    $scope.user = response.user;
                });
        };


        $scope.auth();
    });
