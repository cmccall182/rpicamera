//----------------------------------------------------------------------------
// Function: stream_startStream
//
// Description: Replaces the stream frame place holder in the HTML document with 
// the stream, and sends stream.dat + timestamp get request to server
//
// Inputs: None
//
// Outputs: None
//----------------------------------------------------------------------------
function stream_startStream()
{
    //send inject stream into html
    html_insert = '<img id="streamframe" src="stream.mjpg"><br/><br/>';
    document.getElementById("image_Manipulate").innerHTML = html_insert;
} 

//----------------------------------------------------------------------------
// Function: stream_endStreamStartLog
//
// Description: Replaces the stream frame place holder in the HTML document with 
// the stream, and sends stream.dat + timestamp get request to server
//
// Inputs: None
//
// Outputs: None
//----------------------------------------------------------------------------
function stream_endStreamStartLog()
{
    html_insert = '<p>Data is logging</p>';
    document.getElementById("image_Manipulate").innerHTML = html_insert;
    //get request
    var url = "/done.dat?id=streamStop&ts=" + (new Date()).toLocaleString().replace(/ /g, "");
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.send(null);
}
