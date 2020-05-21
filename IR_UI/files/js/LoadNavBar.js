//----------------------------------------------------------------------------
// Function: createNavBar()
//
// Description: This piece of code inserts the HTML for the nav bar across any
// html file that loads it, under the assumption that the nav bar will be the
// exact same across the website
//
// Inputs: None
//
// Outputs: None
//----------------------------------------------------------------------------
function createNavBar(){
  var html = '<container id="leftsidebar">\
                <ul>\
                  <li><label id="sidebar_title">IR Hub</label><br/><br/>\
                  <li><a href="/../index.html">Home</a></li><br/>\
                  <li><a href="/files/html/retrievalpage.html">Get Data</a></li><br/>\
                  <li><a href="/files/html/stream.html">Stream</a></li><br/>\
                  <li><a href="/files/html/about.html">About</a></li><br/>\
                  <br/><br/>\
                  <li><label>IR STATUS:</label></li>\
                  <li><a id="IR_STATUS"></a></li><br/>\
                </ul>\
              </container>';

  //replace any element with the id of "nav" with the above html
  document.getElementById("nav").innerHTML = html;
}

createNavBar();
