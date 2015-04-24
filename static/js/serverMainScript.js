ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");

ws.onopen = function() {
    msg = new message(GREATING_MSG, "WS opened");
    ws.send(JSON.stringify(msg));
};

ws.onmessage = function (evt)
{
    var clients = JSON.parse(evt.data);
    console.log("server page received ", clients);

    $('#clients').empty();

    clients.forEach(function(cl)
    {
        appendClient(cl);
        console.log("client with id " + cl.id + " was added to server page");
    });
};

var START_SHARING_TASKS_MSG = 1;
var GREATING_MSG = 0;
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