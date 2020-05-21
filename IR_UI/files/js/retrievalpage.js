//----------------------------------------------------------------------------
// Function: createCalendar
//
// Description: Assigns a text box to pop up with a calendar upon selection.
//
// Inputs: None
//
// Outputs: None
//----------------------------------------------------------------------------
function createCalendar()
{
  var foopicker = new FooPicker({
    id: 'datepicker',
    dateFormat: 'MM-dd-yyyy'
  });
  var foopicker2 = new FooPicker({
    id: 'datepicker2'
  });
}

//----------------------------------------------------------------------------
// Function: DateButtonHandler
//
// Description: sends a GET request to the server based on the value in a
// calendar/text box combination
//
// Inputs: None
//
// Outputs: None
//----------------------------------------------------------------------------
function DateButtonHandler()
{
   var path = "/get.zip?id=time_data&ts=" + document.getElementById("datepicker").value;
   var name = document.getElementById("datepicker").value + ".zip";

//  create and click a link that gets cleaned up by the garbage collector
   var a = document.createElement("a");
   a.style = "display: none";
   a.href = path;
   a.download = name;
   a.click();
}

//----------------------------------------------------------------------------
// Function: retrieval_buttonHandler
//
// Description: sends a GET request to the server based on different buttons
// pressed, either for all data, all the image data, or all the spreadsheets
//
// Inputs: vnum: a number that represents which button was pressed and
//               determines which process to follow
//
// Outputs: None
//----------------------------------------------------------------------------
function retrieval_buttonHandler(vnum)
{
    var path = "/get.zip?id=all_data";
    var file_name = "all_data.zip";
    switch(vnum)
    {
        case 1:
            break;
        case 2:
            path = "/get.zip?id=images";
            file_name = "images.zip";
            break;
	      case 3:
            path = "/get.zip?id=data";
            file_Name = "numbers.zip";
            break;
    }

//  create and click a link that gets cleaned up by the garbage collector
    var a = document.createElement("a");
    a.style = "display: none";
    a.href = path;
    a.download = file_name;
    a.click();
}
