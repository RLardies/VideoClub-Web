$(document).ready(function() {
	users_connected();
	setInterval('users_connected()', 3000);
	
})

function users_connected(){

	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	    	document.getElementById("connected_users").innerHTML = this.responseText;
	    }
  	};
  	xhttp.open("GET", "connected_users", true);
  	xhttp.send();
}