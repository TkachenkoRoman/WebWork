var CONECTION_MSG = 0 /* message says that client is connected */
var TASK_MSG = 1 /* new task (start calculating it) */
var STATUS = 10;

function message(type, status) {
    this.type = type;
    this.status = status;
};

var ws = new WebSocket("ws://webwork.ngrok.io/websocketClient");
var output = $("#output");

ws.onopen = function() {
    msg = new message(CONECTION_MSG, "");
    ws.send(JSON.stringify(msg));
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
        msg = new message(STATUS, "0"); /* 2nd argument will be percents proceed */
        ws.send(JSON.stringify(msg));

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
            text: "string length: " + serverMsg.string.length,
            class: "text-center"
        }).appendTo("#taskInfo");
        $('<p/>', {
            text: "start position in text: " + serverMsg.startPos,
            class: "text-center"
        }).appendTo("#taskInfo");
    }
}