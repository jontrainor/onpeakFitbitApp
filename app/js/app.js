var app = angular.module('fitbitApp', []);

app.controller('userInfoCtrl', function($scope) {
	$scope.user = {
		name: 'test user',
		steps: 10000
	};
});
