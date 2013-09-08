angular
    .module("pimp.api", ["restangular"])
    .config(function(RestangularProvider) {
        RestangularProvider.setBaseUrl("/api/v1");
        RestangularProvider.setRequestSuffix("/")

        RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
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
