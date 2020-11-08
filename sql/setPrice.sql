--Sabiendo que los precios de las películas se han ido incrementando un 2% anualmente, elaborar la
--consulta setPrice.sql que complete la columna 'price' de la tabla 'orderdetail', sabiendo que el
--precio actual es el de la tabla 'products'. 

--obtenemos la diferencia de años entre cuando se hizo el pedido y la fecha actual
--multiplicamos el precio actual del producto por 0.98 pues cada año anterior era un 2% más barato
--luego por cada año habrá que multiplicar por 0.98, o lo que es lo mismo, elevar 0.98 al número 
--de años de diferencia. 

update orderdetail
set price = products.price * power(0.98, (select extract(year from CURRENT_DATE) - (select extract(year from orders.orderdate))))
from orders, products 
where orderdetail.orderid = orders.orderid and products.prod_id = orderdetail.prod_id;