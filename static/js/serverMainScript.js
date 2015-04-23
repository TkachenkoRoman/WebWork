ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");

ws.onopen = function() {
    ws.send("Server greeting");
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