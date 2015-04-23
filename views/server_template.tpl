<!DOCTYPE html>
<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <!-- Optional theme -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        <!--angular -->
        <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>
        <script src="serverMainScript.js"></script>
        <script src="socket.js"></script>
    </head>
    <body data-ng-app="serverApp" data-ng-controller="serverController">
        <nav class="navbar navbar-inverse">
          <div class="container">
            <div class="navbar-header">
              <a class="navbar-brand" href="#">
                Server
              </a>
            </div>
          </div>
        </nav>

        <div class="container">
            <button ng-click="test='socket.clients[0].id'"></button>
            <div class="row">
                <div class="col-md-4 col-sm-4 col-ld-4" data-ng-repeat="cl in socket.clients">
                    <p data-ng-bind="cl.id"></p>
                    <img src="cluster.png" class="img-responsive" />
                </div>
            </div>
        </div>
    </body>
</html>