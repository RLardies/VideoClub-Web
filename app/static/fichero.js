

function validacion(){

	var fname = document.getElementById("fname").value;
	var lname = document.getElementById("lname").value;
	var username = document.getElementById("username").value;
	var email = document.getElementById("email").value;
	var pwd = document.getElementById("pwd").value;
	var creditcard = document.getElementById("creditcard").value;
	var gender = document.getElementById("gender").selectedIndex;

	if(fname == null || fname.length == 0 || /^\s+$/.test(fname)){
		alert('[ERROR] El campo debe tener un nombre valido');
		return false;
	}

	if(lname == null || lname.length == 0 || /^\s+$/.test(lname)){

		alert('[ERROR] El campo debe tener un nombre valido');
		return false;
	}

	if(username == null || username.length == 0 || /^\s+$/.test(username)){

		//Comprobar si existe
		alert('[ERROR] El usuario no es valido o ya existe');
		return false;
	}

	if( /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(email) == false)  {
		alert('[ERROR] El correo introducido no es valido');
 		return false;
	}

	if( pwd == null || pwd.length < 7 || /^\s+$/.test(pwd)) {
		alert('[ERROR] El correo introducido no es valido');
 		return false;
	}

	//Comprobamos genero
	if(gender == null || gender == 0){
		alert('[ERROR] Seleccione un genero valido');
		return false;
	}

	return true;
}



$(document).ready(function() {

   $('#pwd').on('change keyup paste', function() {

   $('#password-strength-text').html(checkStrength($('#pwd').val()))

})})

function checkStrength(password) {

	var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
    var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
    var enoughRegex = new RegExp("(?=.{6,}).*", "g");

	if (enoughRegex.test(password) == false){
		$('#password-strength-text').css("color","#FF0000")
		return "Too short";
	}
	else  if( strongRegex.test(password)){
		$('#password-strength-text').css("color","#008F39")
		return "Strong"
	}
	else  if( mediumRegex.test(password)){
		$('#password-strength-text').css("color","#E5BE01")
		return "Medium"
	} else{
		$('#password-strength-text').css("color","#FF0000")
		return "Weak"
	}

}