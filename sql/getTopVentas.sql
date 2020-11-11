create or replace function getTopVentas() returns text as $$

declare 
    in_uno alias for $1;
    in_dos alias for $2;

begin

    (select  prod_id, extract(year from orderdate) as date, sum(quantity) as ventas from orderdetail natural inner join orders
    group by  prod_id, date
    order by ventas desc);

    
        select  prod_id, extract(year from orderdate) as d, sum(quantity) as ventas from orderdetail natural inner join orders
        where orderdate = '2016'
        group by  prod_id, d
        order by ventas desc
    
end;
$$  language plpgsql;