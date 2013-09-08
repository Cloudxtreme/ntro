angular
    .module("pimp.api", ["restangular", "pimp.config"])
    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl("/api/v1");
        RestangularProvider.setRequestSuffix("/");
        if (pimp.user) {
            RestangularProvider.setDefaultRequestParams({
                api_key: pimp.user.api_key,
                api_user: pimp.user.username
            });
        }

        RestangularProvider.setResponseExtractor(function (data, operation, what, url, response) {
            var newResponse;
            if (operation === "getList") {
                newResponse = data.objects;
                newResponse.meta = data.meta;
            } else {
                newResponse = data;
            }
            if (!angular.isObject(newResponse)) {
                newResponse = {};
            }
            newResponse.statusCode = function () {
                return response.status;
            };
            newResponse.headers = response.headers;
            return newResponse;
        });
    });
