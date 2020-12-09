-- Analizamos los resultados de las querys sin indices
EXPLAIN ANALYZE
select count(*)
from orders
where status is null;

EXPLAIN ANALYZE
select count(*)
from orders
where status ='Shipped';

-- Creamos un indice en la tabla orders
create index index_status on orders(status);

EXPLAIN ANALYZE
select count(*)
from orders
where status is null;

EXPLAIN ANALYZE
select count(*)
from orders
where status ='Shipped';

-- Ejecutamos la sentencia ANALYZE y volvemos a analizar los costes
ANALYZE orders;

EXPLAIN ANALYZE
select count(*)
from orders
where status is null;

ANALYZE orders;

EXPLAIN ANALYZE
select count(*)
from orders
where status ='Shipped';

--Las otras dos consultas que se nos pedían
ANALYZE orders;
EXPLAIN ANALYZE
select count(*)
from orders
where status ='Paid';

ANALYZE orders;
EXPLAIN ANALYZE
select count(*)
from orders
where status ='Processed';