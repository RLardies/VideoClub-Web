create or replace function setOrderAmount() returns void as $$
begin

    update orders
    set netamount = table_aux.suma, totalamount = netamount * ( 1 + tax/100)
    from (SELECT orderid, sum(price*quantity) as suma FROM orders NATURAL INNER JOIN orderdetail group by orderid) as table_aux
    where table_aux.orderid = orders.orderid;

end; 
$$  language plpgsql;


select * from setOrderAmount();

