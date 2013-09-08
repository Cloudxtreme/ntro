angular
    .module("pimp.api", ["restangular", "pimp.config"])
    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl("/api/v1");
        RestangularProvider.setRequestSuffix("/");
        if (pimp.user) {
            RestangularProvider.setDefaultRequestParams({
                api_key: pimp.user.api_key
            });
        }

        RestangularProvider.setResponseExtractor(function (response, operation, what, url) {
            if (operation === "getList") {
                var newResponse;
                newResponse = response.objects;
                newResponse.meta = response.meta;
                console.log(newResponse);
                return newResponse;
            } else {
                return response;
            }
        });
    });
