var CONECTION_MSG = 0 /* message says that client is connected */

var ws = new WebSocket("ws://webwork.ngrok.io/websocketClient");
var output = $("#output");

ws.onopen = function() {
};
ws.onmessage = function (evt) {
    var serverMsg = JSON.parse(evt.data);
    processMsg(serverMsg);
};

function processMsg(serverMsg) {
    if (serverMsg.type == CONECTION_MSG)
    {
        $('<h2/>', {
            text: "You`re connected to server under id = " + serverMsg.id,
            class: "text-center"
        }).appendTo("#main");
    }

}