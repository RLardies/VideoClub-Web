var fname = document.getElementById("fname").value;
var lname = document.getElementById("lname").value;
var username = document.getElementById("username").value;
var email = document.getElementById("email").value;
var pwd = document.getElementById("pwd").value;
var creditcard = document.getElementById("creditcard").value;
var gender = document.getElementById("campo").selectedIndex;

function validacion(){

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

	if( !(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)/.test(email)) ) {
		alert('[ERROR] El correo introducido no es valido');
 		return false;
	}

	if( pwd == null || pwd.length < 8 || /^\s+$/.test(pwd)) {
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