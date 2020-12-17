
alter table customers add column promo integer default 10;

create or replace function update_promos() returns trigger as $update_promos$
    begin

        update orders
        set netamount = (netamount * (1 + (old.promo / 100.0))) * (1 - ( new.promo / 100.0)), totalamount = (netamount * (1 + (old.promo / 100.0))) * (1 - ( new.promo / 100.0)) * ( 1 + tax/100)
        where orders.customerid = new.customerid and 
            orders.status is NULL;

        PERFORM pg_sleep(10)
        
        return new;
     
    end;
    
$update_promos$ language plpgsql;



create trigger update_promo 
after update 
of promo
on customers for each row 
execute procedure update_promos();