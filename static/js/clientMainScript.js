var CONECTION_MSG = 0 /* message says that client is connected */
var TASK_MSG = 1 /* new task (start calculating it) */
var STATUS = 10;

function message(type, status) {
    this.type = type;
    this.status = status;
    this.substringFound = 0;
    this.time = 0;
};


//var ws = new WebSocket("ws://webwork.ngrok.io/websocketClient");
var ws = new WebSocket("ws://localhost:8080/websocketClient");

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
        var start = new Date().getTime();

        msg = new message(STATUS, "0"); /* 2nd argument will be percents proceed */
        ws.send(JSON.stringify(msg));

        $("#taskInfo").empty();

        var well = $('<div/>', {
            class: "well well-sm",
            style: "display: none;"
        }).appendTo("#taskInfo");

        $('<h2/>', {
            text: "Task",
            class: "text-center"
        }).appendTo(well);

        var taskInfoListGroup = $('<ul/>', {
            class: "list-group"
        }).appendTo(well);

        $('<li/>', {
            class: "list-group-item",
            html: "<b>Substring to search:</b> " + serverMsg.substringToSearch
        }).appendTo(taskInfoListGroup);

        $('<li/>', {
            class: "list-group-item",
            html: "<b>String length:</b> " + serverMsg.string.length
        }).appendTo(taskInfoListGroup);

        $('<li/>', {
            class: "list-group-item",
            html: "<b>Start position in text:</b> " + serverMsg.startPos
        }).appendTo(taskInfoListGroup);

        $('<li/>', {
            id: "foundedSubstrings",
            class: "list-group-item",
            html: "<b>Founded substrings:</b> 0"
        }).appendTo(taskInfoListGroup);

        var progressBar = $('<div/>', {
            class: "progress"
        }).appendTo(well);

        $('<div/>', {
            id: "progressBar",
            class: "progress-bar",
            role: "progressbar",
            'aria-valuenow': "0",
            'aria-valuemin': "0",
            'aria-valuemax': "100",
            style: "min-width: 2em;",
            text: "0%"
        }).appendTo(progressBar);

        well.fadeIn(50);

        var webWorker = new Worker("stringSearchWorker.js");
        webWorker.postMessage(JSON.stringify(serverMsg));

        webWorker.onmessage = function(evt) {
            var msg = JSON.parse(evt.data);
            statusMsg = new message(STATUS, msg.status); /* 2nd argument will be percents proceed */
            statusMsg.substringFound = msg.substringFound;
            if (msg.status == 100) // if work done
            {
                var end = new Date().getTime();
                //statusMsg.time = msg.time;
                statusMsg.time = end - start;
                webWorker.terminate();

                $("#taskInfo > .well.well-sm > h2").text("Task is completed");
                $("#progressBar").css('width', "0%").attr('aria-valuenow', 0);
                $("#progressBar").text("0%");
            }
            else
            {
                $("#progressBar").css('width', msg.status + "%").attr('aria-valuenow', msg.status);
                $("#progressBar").text(msg.status + "%");
            }
            $("#foundedSubstrings").html("<b>Founded substrings:</b> " + msg.substringFound);

            ws.send(JSON.stringify(statusMsg));
            console.log("client send message to server: ", JSON.stringify(statusMsg));
        };
    }
}