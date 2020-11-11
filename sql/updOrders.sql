create or replace function update_orders() returns trigger as $update_orders$
    begin

        select * from setOrderAmount();
       
    end;
    
$update_orders$ language plpgsql;



create trigger update_orders 
after update or insert or delete
on orders
execute procedure update_orders();
