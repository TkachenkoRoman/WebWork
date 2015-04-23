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
        var clientId = "client" + cl.id;

        $('<div/>', {
            class: "col-md-4 col-sm-4 col-ld-4",
            id: clientId
        }).appendTo('#clients');

        $('<h4/>', {
            text: clientId,
            class: "text-center"
        }).appendTo("#" + clientId);

        $('<img/>', {
            class: "img-responsive center-block",
            src: "cluster.png"
        }).appendTo("#" + clientId);

        console.log("client with id " + cl.id + " was added to server page");
    });
};