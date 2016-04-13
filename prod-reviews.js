$(document).ready(function() {
  $('.datepicker').datepicker();
});

function getOutput(){
	document.getElementById("reviewForm").submit();
	setTimeout(getOutput1, 10000); //wait ten seconds before continuing
}

// handles the click event for button click, sends the query
function getOutput1() {
  getRequest(
      'process.php', // URL for the PHP file
       drawOutput,  // handle successful request
       drawError    // handle error       
  );
  return false;
}

// handles drawing an error message
function drawError() {
    var container = document.getElementById('disabledInput');
    container.innerHTML = 'Bummer: there was an error!';
    console.log("Error");
}

// handles the response, updates the html
function drawOutput(responseText) {
    var container = document.getElementById('disabledInput');
    container.value = responseText;
    console.log("Response: ");
    console.log(responseText);
    console.log("Value: ");
    console.log(container.value);
}

// helper function for cross-browser request object
function getRequest(url, success, error) {
    var req = false;
    try{
        // most browsers
        req = new XMLHttpRequest();
    } catch (e){
        // IE
        try{
            req = new ActiveXObject("Msxml2.XMLHTTP");
        } catch(e) {
            // try an older version
            try{
                req = new ActiveXObject("Microsoft.XMLHTTP");
            } catch(e) {
                return false;
            }
        }
    }
    if (!req) return false;
    if (typeof success != 'function') success = function () {};
    if (typeof error!= 'function') error = function () {};
    req.onreadystatechange = function(){
        if(req.readyState == 4) {
            return req.status === 200 ? 
                success(req.responseText) : error(req.status);
        }
    }
    req.open("GET", url, true);
    req.send(null);
    console.log(req);
    return req;
}