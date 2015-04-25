ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");

ws.onopen = function() {
    msg = new message(GREATING_MSG, "WS opened");
    ws.send(JSON.stringify(msg));
};

ws.onmessage = function (evt)
{
    var serverMsg = JSON.parse(evt.data);
    processMsg(serverMsg);
};

var START_SHARING_TASKS_MSG = 1;
var GREATING_MSG = 0;

var NEW_CLIENT_MSG = 10
var CLIENT_LEAVED_MSG = 11
var WARNING_MSG = 12
var CLIENT_STATUS_MSG = 13

function processMsg(serverMsg) {
    $("#warning").remove();
    if (serverMsg.type == NEW_CLIENT_MSG)
    {
        appendClient(serverMsg);
    }
    if (serverMsg.type == CLIENT_LEAVED_MSG)
    {
        removeClient(serverMsg);
    }
    if (serverMsg.type == WARNING_MSG)
    {
        $('<h2/>', {
            text: serverMsg.message,
            id: "warning",
            class: "text-center"
        }).prependTo('#main');
    }
    if (serverMsg.type == CLIENT_STATUS_MSG)
    {
        var clientId = "client" + serverMsg.clientId;
        $('<p/>', {
            text: "status:  " + "busy", /* here will be percents */
        }).appendTo("#" + clientId);
    }
};

function message(type, data) {
    this.type = type;
    this.data = data;
};

$(document).ready(function(){
    $("#goButton").click(function() {
        msg = new message(START_SHARING_TASKS_MSG, $("#substringToSearch").val());
        ws.send(JSON.stringify(msg));
    });
});

function appendClient(cl) {
    var clientId = "client" + cl.id;
    var clientInfoId = "clientInfo" + cl.id;

    $('<div/>', {
        class: "well well-sm",
        id: clientId
    }).appendTo('#clients');

    $('<h4/>', {
        text: "Client id: " + cl.id,
    }).appendTo("#" + clientId);

    $('<p/>', {
        text: "http_user_agent:  " + cl.httpUserAgent,
    }).appendTo("#" + clientId);


    /*$('<img/>', {
        class: "img-responsive",
        src: "cluster.png"
    }).appendTo("#" + clientId);*/
};

function removeClient(cl) {
    var clientId = "client" + cl.id;

    $("#" + clientId).remove();
};