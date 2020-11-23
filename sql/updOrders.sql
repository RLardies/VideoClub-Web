create or replace function update_orders() returns trigger as $update_orders$
    begin


        if (TG_OP = 'DELETE') then

            update orders
            set netamount = table_aux.suma, totalamount = table_aux.suma * ( 1 + tax/100)
            from (SELECT orderid, sum(price*quantity) as suma FROM orders NATURAL INNER JOIN orderdetail group by orderid) as table_aux
            where table_aux.orderid = orders.orderid and
                orders.orderid = old.orderid;
            
            delete from orders 
            where orderid = old.orderid and 
                netamount = 0;

            --Borramos el order si no tiene ningun articulo

            return old;

        end if;

        update orders
        set netamount = table_aux.suma, totalamount = table_aux.suma * ( 1 + tax/100)
        from (SELECT orderid, sum(price*quantity) as suma FROM orders NATURAL INNER JOIN orderdetail group by orderid) as table_aux
        where table_aux.orderid = orders.orderid and
            orders.orderid = new.orderid;

        return new;
     
    end;
    
$update_orders$ language plpgsql;



create trigger update_orders 
after update or insert or delete
on orderdetail for each row 
execute procedure update_orders();
