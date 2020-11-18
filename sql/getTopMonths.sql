create or replace function getTopMonths(numProducts integer, totalAmount integer)
    returns table(anoVenta integer, monthVenta integer, totalVentas bigint, totalGanancia numeric) as $$

begin
    return query

        select monthVentas.anoVenta, monthVentas.monthVenta, monthVentas.totalVentas, monthVentas.totalGanancia
        from (
            select cast(extract(year from orders.orderdate) as integer) as anoVenta, cast(extract(month from orders.orderdate) as integer) as monthVenta, sum(orderdetail.quantity) as totalVentas, sum(orders.totalamount) as totalGanancia
            from orders, orderdetail
            where orders.orderid = orderdetail.orderid 
                   
            group by anoVenta, monthVenta
            order by anoVenta, monthVenta) as monthVentas
        where monthVentas.totalVentas >= 19000 or
            monthVentas.totalGanancia >= 320000;

end;
$$  language plpgsql;

select getTopMonths(19000, 320000);