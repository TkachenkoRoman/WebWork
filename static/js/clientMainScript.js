var CONECTION_MSG = 0 /* message says that client is connected */
var TASK_MSG = 1 /* new task (start calculating it) */

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
    if (serverMsg.type == TASK_MSG)
    {
        $("#taskInfo").empty();
        $('<h2/>', {
            text: "You have a new task! ",
            class: "text-center"
        }).appendTo("#taskInfo");
        $('<p/>', {
            text: "substring to search: " + serverMsg.substringToSearch,
            class: "text-center"
        }).appendTo("#taskInfo");
        $('<p/>', {
            text: "start position in text: " + serverMsg.startPos,
            class: "text-center"
        }).appendTo("#taskInfo");
    }
}