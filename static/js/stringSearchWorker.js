onmessage = function (evt) {
    var msg = JSON.parse(evt.data);
    var substring = msg.substringToSearch;
    var string = msg.string;
    console.log("webworker achieved message");
    if (msg.string.length > 0 && msg.substringToSearch.length > 0)
        searchSubstring(substring, string, msg.startPos);
};

function workerMessage(status, substringFound, time) {
    this.status = status;
    this.substringFound = substringFound;
    this.time = time;
};

function searchSubstring(substringToSearch, string, startPos) {
    var substrPosList = []
    var percent = Math.floor(string.length / 100);
    var status = 0;

    var start = new Date().getTime();

    for (i = 0; i < string.length; ++i) {
        // If you want to search case insensitive use
        // if (source.substring(i, i + find.length).toLowerCase() == find) {
        if (string.substring(i, i + substringToSearch.length) == substringToSearch) {
          substrPosList.push(i + startPos);
        }
        if (i % percent == 0)
        {
            msg = new workerMessage(status, substrPosList.length);
            postMessage(JSON.stringify(msg));
            if (status < 99)
                status = status + 1;
        }
      }

    var end = new Date().getTime();
    msg = new workerMessage(100, substrPosList.length, end - start);
    postMessage(JSON.stringify(msg));
};