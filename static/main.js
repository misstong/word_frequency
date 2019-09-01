(function() {
    'use strict';

    angular.module('WordcountApp',[])

    .controller('WordcountController',['$scope','$log','$http','$timeout',
    function($scope,$log,$http,$timeout) {
        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.getWordCount=function (jobID) {
            var timeout = "";
          
            var poller = function() {
              // fire another request
              $http.get('/results/'+jobID).
                success(function(data, status, headers, config) {
                  if(status === 202) {
                    $log.log(data, status);
                  } else if (status === 200){
                    $log.log(data);
                    $scope.wordcounts = data;
                    $scope.loading = false;
                    $scope.submitButtonText = "Submit";
                    $timeout.cancel(timeout);
                    $log.log('data in scope:')
                    $log.log($scope.wordcounts)
                    return false;
                  }
                  // continue to call the poller() function every 2 seconds
                  // until the timeout is cancelled
                  
                }).error(function(error){
                  $log.log(error);
                  $scope.loading = false;
                  $scope.submitButtonText = "Submit";
                  $scope.urlerror = true;
                });
            };
            timeout = $timeout(poller, 2000);
          }
        $scope.getResults = function() {
            $log.log('test')

            var userInput = $scope.url

            $http.post('/start',{'url':userInput}).
            success(function(results){
                $log.log(results);
                $scope.getWordCount(results['id'])
                $scope.wordcounts = null;
                $scope.loading=true;
                $scope.submitButtonText = 'Loading...'
                $scope.urlerror = false;
            }).
            error(function(error){
                $log.log(error);
                $scope.urlerror = false;
            })
        }
    }])
    .directive('wordCountChart',['$parse',function($parse){
      return {
        restrict: 'E',
        replace: true,
        template: '<div id="chart"></div>',
        link:function(scope){
          scope.$watch('wordcounts',function(){
            d3.select('#chart').selectAll('*').remove();
            var data = scope.wordcounts;
            for (var word in data) {
              d3.select('#chart')
              .append('div')
              .selectAll('div')
              .data(word[0])
              .enter()
              .append('div')
              .style('width',function(){
                return (data[word][1]*5) + 'px';
              })
              .text(function(d){
                return data[word][0];
              })
            }
          },true);
        }
      }
    }])
}())