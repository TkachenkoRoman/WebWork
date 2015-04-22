<!DOCTYPE html>
<html>
    <head>
      <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
      <script type="text/javascript">
        var ws = new WebSocket("ws://webwork.ngrok.io/websocket");
        var output = $("#output");

        ws.onopen = function() {
            print("CONNECTED");
        };
        ws.onmessage = function (evt) {
            print(evt.data);
        };

        function print(message) {
            var pre = document.createElement("p");
            pre.style.wordWrap = "break-word";
            pre.innerHTML = message;
            $("#output").append(pre);
        };

        $(document).ready(function(){
            $("#sendButton").click(function(){
                ws.send($("#message").val());
                $("#message").val("");
            });
        });

      </script>
    </head>
    <body>
        <div id="output">
        </div>
        <input id="message" type="text" />
        <input type="button" id="sendButton" value="send">
    </body>
</html>