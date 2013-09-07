angular
    .module("pimp.config", [])
    .factory("config", function () {
        return {
            resources: {
                rest: {
                    baseUrl: "static/mock/"
                },
                partials: {
                    baseUrl: "static/partials/"
                }

            }
        };
    });
