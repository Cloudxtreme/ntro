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
    });
