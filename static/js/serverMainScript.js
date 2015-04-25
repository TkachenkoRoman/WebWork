ws = new WebSocket("ws://webwork.ngrok.io/websocketServer");

ws.onopen = function() {
    msg = new message(GREATING_MSG, "WS opened");
    ws.send(JSON.stringify(msg));

    $("#goButton").prop("disabled",false);
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
var WORK_DONE_MSG = 14

var totalResult = 0;

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

        $("#goButton").button('reset');
        $("#goButton").prop("disabled",true);

        if (serverMsg.status == 100) /* some task completed */
        {
            console.log(clientId + " completed task");
            $("#progressBar" + serverMsg.clientId).css('width', "0%").attr('aria-valuenow', 0);
            $("#progressBar" + serverMsg.clientId).text("0%");
            $("#resultsHeader").text("Results:");
            $("#" + clientId + " > #searchResult").empty(); /* results will be displayed on right part of screen*/
            $("#" + clientId + " > #status").text("status: ready");
            var res = $('<li/>', {
                class: "list-group-item",
                text: "client " + serverMsg.clientId + " complete task"
            }).appendTo('#results');
            $('<span/>', {
                            class: "badge",
                            text: serverMsg.substringPositions.length
                        }).appendTo(res);
            totalResult = totalResult + serverMsg.substringPositions.length;
        }
        else
        {
            $("#" + clientId + " > #status").text("status: computing...");
            $("#" + clientId + " > #searchResult").text("substrings found: " + serverMsg.substringPositions.length);
            $("#progressBar" + serverMsg.clientId).css('width', serverMsg.status + "%").attr('aria-valuenow', serverMsg.status);
            $("#progressBar" + serverMsg.clientId).text(serverMsg.status + "%");
        }
    }
    if (serverMsg.type == WORK_DONE_MSG)
    {
        $("#goButton").prop("disabled",false);
        var total = $('<li/>', {
                class: "list-group-item",
                text: "Total"
            }).appendTo('#results');
            $('<span/>', {
                            class: "badge",
                            text: totalResult
                        }).appendTo(total);
    }

};

function message(type, data) {
    this.type = type;
    this.data = data;
};

$(document).ready(function(){
    $("#goButton").click(function() {
        $("#results").empty();
        totalResult = 0;
        msg = new message(START_SHARING_TASKS_MSG, $("#substringToSearch").val());
        ws.send(JSON.stringify(msg));
        $("#goButton").button('loading');
    });
});

function appendClient(cl) {
    var clientId = "client" + cl.id;
    var clientInfoId = "clientInfo" + cl.id;

    var well = $('<div/>', {
        class: "well well-sm clearfix",
        id: clientId,
        style: "display: none;"
    }).appendTo('#clients');

    $('<a/>', {
        href: "#",
        class: "pull-right",
        html: $('<span/>', {
            class: "glyphicon glyphicon-remove  ",
            'aria-hidden': "true"
        })
    }).appendTo("#" + clientId);

    $('<h4/>', {
        text: "Client id: " + cl.id,
    }).appendTo("#" + clientId);

    $('<p/>', {
        text: "http_user_agent:  " + cl.httpUserAgent,
    }).appendTo("#" + clientId);

    $('<p/>', {
        text: "status: ready",
        id: "status"
    }).appendTo("#" + clientId);

    $('<p/>', {
        id: "searchResult"
    }).appendTo("#" + clientId);

    var progressBar = $('<div/>', {
        class: "progress"
    }).appendTo("#" + clientId);

    $('<div/>', {
        id: "progressBar" + cl.id,
        class: "progress-bar",
        role: "progressbar",
        'aria-valuenow': "0",
        'aria-valuemin': "0",
        'aria-valuemax': "100",
        style: "min-width: 2em;",
        text: "0%"
    }).appendTo(progressBar);

    well.fadeIn();

    /*$('<img/>', {
        class: "img-responsive",
        src: "cluster.png"
    }).appendTo("#" + clientId);*/
};

function removeClient(cl) {
    var clientId = "client" + cl.id;
    $("#" + clientId).fadeTo("fast", 0.00, function() { $(this).slideUp(function(){ $(this).remove() }) });
};