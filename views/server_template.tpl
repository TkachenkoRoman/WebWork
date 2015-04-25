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
        <script src="serverMainScript.js"></script>
    </head>
    <body>
        <nav class="navbar navbar-inverse">
          <div class="container-fluid">
            <div class="navbar-header">
              <a class="navbar-brand" href="#">
                Server
              </a>
            </div>
          </div>
        </nav>

        <div class="container-fluid" id="main">
            <div class="col-md-6 col-sm-6 col-ld-6">
                <h2>Connected clients:</h2>
                <div class="row" id="clients">
                </div>
            </div>
            <div class="col-md-6 col-sm-6 col-ld-6">
                <h2>Server task:</h2>
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="Search for..." id="substringToSearch">
                  <span class="input-group-btn">
                    <button class="btn btn-default" type="button" id="goButton" data-loading-text="loading stuff...">Go</button>
                  </span>
                </div><!-- /input-group -->
                <h2 id="resultsHeader"></h2>
                <div class="col-md-6 col-sm-6 col-ld-6">
                    <ul class="list-group" id="results"></ul>
                </div>

            </div>
        </div>
    </body>
</html>