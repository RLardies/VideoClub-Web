drop function if exists getTopVentas(integer, integer);
create or replace function getTopVentas(anoInicial integer, anoFinal integer)
    returns table(anoVenta integer, titulo varchar,id integer, totalVentas bigint) as $$

begin

    return query

        select distinct on (ventasAno.anoVenta) ventasAno.anoVenta, ventasAno.titulo, ventasAno.id, ventasAno.totalVentas from (

            select imdb_movies.movietitle as titulo, imdb_movies.movieid as id, cast(extract(year from orders.orderdate) as integer) as anoVenta, sum(orderdetail.quantity) as totalVentas
            from imdb_movies, orders, orderdetail, products
            where anoInicial <= cast(extract(year from orders.orderdate) as integer) and
                anoFinal >= cast(extract(year from orders.orderdate) as integer) and
                orders.orderid = orderdetail.orderid and 
                orderdetail.prod_id = products.prod_id and 
                products.movieid = imdb_movies.movieid 
            group by id, titulo, anoVenta
            order by anoVenta, totalVentas desc ) as ventasAno;


end;
$$  language plpgsql;


select * from getTopVentas(2016, 2018);