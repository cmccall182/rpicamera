//----------------------------------------------------------------------------
// Function: index_buttonHandler
//
// Description: This function controls the raspberry pi remotely from the
// server. Depending on which button is pressed, it will either start, stop,
// or restart a given process.
//
// Inputs: vnum, a value which varies based on the button pressed.
//
// Outputs: None
//----------------------------------------------------------------------------
function index_buttonHandler(vnum)
{
    var path = "something that triggers default :)";
    switch(vnum)
    {
        case 1:
            path = "resetPI"
            break;
        case 2:
            path = "squigglyshit"
            break;
	case 3:
            path = "startIR";
	    break;

        case 4:
  	    path = "stopIR";
  	    break;

        default:
            break;
    }

//  create and click a link that gets cleaned up by the garbage collector
    var a = document.createElement("a")
    a.style = "display: none";
    a.href = path;
    a.click();
}
