var ws = new WebSocket("ws://webwork.ngrok.io/websocketClient");
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