--pruebas
drop index index_year;
create index index_year on orders(extract(year from orderdate));
drop index index_month;
create index index_month on orders(extract(month from orderdate));

--nuestro elegido
drop index index_yearmonth;
create index index_yearmonth on orders(extract(year from orderdate), extract(month from orderdate));


EXPLAIN
select count(distinct customerid)
from orders
where totalamount > 100 and extract(year from orderdate) = 2015 and extract(month from orderdate)= 4