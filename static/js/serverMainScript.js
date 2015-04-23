var ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");
var app = angular.module('serverApp', []);

ws.onopen = function() {
    ws.send("Server greeting");
};

ws.onmessage = function (evt) {
    var msg = JSON.parse(evt.data);
    console.log("server page received ", msg);
    msg.forEach(function(cl) {
        console.log("client with id " + cl.id + " was added to server page");
        var div = document.createElement('div');
        div
        $("#clients").append(client);
    });

};


