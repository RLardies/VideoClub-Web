

function show(titulo, poster, colnum, id) {

  var link = document.getElementById(id);
  let columna = ".column"+colnum.toString();
  let div = document.querySelector(columna);
  div.appendChild(link);

  var container = document.createElement("div");
  container.setAttribute("class", "container");
  container.innerHTML = `<div class="container"> </div>`
  container.onmouseover = this.className = 'hover';
  container.onmouseout =this.className = '';
  link.appendChild(container);

  var title = document.createElement("div");
  title.setAttribute("class", "overlay");
  title.setAttribute("id", "titulo");
  title.className = "overlay";
  title.innerHTML = titulo;
  container.appendChild(title);

  var imagen = document.createElement("img");
  imagen.setAttribute("src", poster);
  imagen.setAttribute("alt", titulo);
  imagen.setAttribute("style", ".column" + colnum.toString() + "img")
 

  container.appendChild(imagen);

  }