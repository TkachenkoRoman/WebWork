var ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");

ws.onopen = function() {
    ws.send("Server greeting");
};

ws.onmessage = function (evt) {
    var msg = JSON.parse(evt.data);

    switch(msg.type) {
    case "id":
      var client = '<div>client</div>'
      $("#clients").append(client);
      break;
    }
};


