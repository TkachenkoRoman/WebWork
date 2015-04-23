function socket ()
{
    this.ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");
    this.clients = [];
    this.clientsChange = 0;

    var self = this;
    this.ws.onopen = function() {
            self.ws.send("Server greeting");
    };

    this.ws.onmessage = function (evt) {

        self.clientsChange = self.clientsChange + 1;
        self.clients = JSON.parse(evt.data);
        console.log("server page received ", self.clients);
        self.clients.forEach(function(cl) {
            console.log("client with id " + cl.id + " was added to server page");
        });
    };
}
