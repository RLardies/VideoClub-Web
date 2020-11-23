create function update_inventory() returns trigger as $update_inventory$
    begin 
        if (new.status = 'Paid') then
            update products
            set stock = stock - orderdetail.quantity, sales = sales + orderdetail.quantity
            from orderdetail
            where new.orderid = orderdetail.orderid and 
                orderdetail.prod_id = products.prod_id;

        
            insert into no_stock (prod_id, orderdate)
            select products.prod_id, orders.orderdate
            from orders, orderdetail, products
            where orders.orderid = new.orderid and
                orders.orderid = orderdetail.orderid and
                orderdetail.prod_id = products.prod_id and 
                products.stock = 0 ;


        end if;

        return new;
        

    end;
$update_inventory$ language plpgsql;


create trigger updInventory 
after update
on orders for each row
execute procedure update_inventory();