
$(document).ready(function(){
	$('.despliegue').on('click',function(){
    	$(this).nextUntil('.findespliegue').slideToggle();
  	}
	);

	$('.despliegue').nextUntil('.findespliegue').hide();
});