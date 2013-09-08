angular
    .module("pimp.config", [])
    .factory("config", function () {
        return {
            resources: {
                partials: {
                    baseUrl: "static/partials/"
                }
            }
        };
    })
    .directive('onEnter', function () {
        return function (scope, element, attrs) {
            element.bind("keydown keypress", function (event) {
                if (event.which === 13) {
                    scope.$apply(function () {
                        scope.$eval(attrs.onEnter);
                    });

                    event.preventDefault();
                }
            });
        };
    });
