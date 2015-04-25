onmessage = function (evt) {
    var msg = JSON.parse(evt.data);
    var substring = msg.substringToSearch;
    var string = msg.string;
    console.log("webworker achieved message");
    if (msg.string.length > 0 && msg.substringToSearch.length > 0)
        searchSubstring(substring, string, msg.startPos);
};

function workerMessage(status, substringPositions) {
    this.status = status;
    this.substringPositions = substringPositions;
};

function searchSubstring(substringToSearch, string, startPos) {
    var substrPosList = []
    var percent = Math.floor(string.length / 99);
    var status = 0;

    for (i = 0; i < string.length; ++i) {
        // If you want to search case insensitive use
        // if (source.substring(i, i + find.length).toLowerCase() == find) {
        if (string.substring(i, i + substringToSearch.length) == substringToSearch) {
          substrPosList.push(i + startPos);
        }
        if (i % percent == 0)
        {
            msg = new workerMessage(status, substrPosList);
            postMessage(JSON.stringify(msg));
            status = status + 1;
        }
      }
    msg = new workerMessage(100, substrPosList);
    postMessage(JSON.stringify(msg));
};