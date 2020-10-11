//var data = JSON.parse(catalogue);

      len = 12;
      var elemscolumn = Math.ceil(len/4);
      var i = 0;
      var a = 0;


      let contain = document.querySelector(".row");
      for (var colnum = 0; colnum <= 3; colnum++) {
          var div = document.createElement("div");
          div.setAttribute("class", "column");
          div.innerHTML = `<div class="column"> </div>`

          for (i = 0; i < elemscolumn; i++ ) {
            var link = document.createElement("a");
            link.href = "filmdescription";

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
            title.innerHTML = `<div class="overlay">Moonlight</div>`
            container.appendChild(title);

            var imagen = document.createElement("img");
            imagen.setAttribute("src", "../static/images/moonlight.jpg");
            imagen.setAttribute("alt", "moonlight");
            imagen.setAttribute("style", ".column img")
            

            container.appendChild(imagen);

          }
        
          contain.appendChild(div);
      }
