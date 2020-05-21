var curStatus;

function reqListener()
{
    curStatus = this.responseText
    document.getElementById("IR_STATUS").innerHTML = curStatus;
}

function updateStatusBar()
{
    var path = "getStatus";        
    var req = new XMLHttpRequest();
    req.open("GET", path);
    req.addEventListener("load", reqListener);
    req.send();

}

updateStatusBar();
var timer = setInterval(updateStatusBar, 5000);