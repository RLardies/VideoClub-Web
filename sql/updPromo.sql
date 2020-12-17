
alter table customers add column promo integer default 0;
alter table orders alter column netamount type numeric(10,2);
alter table orders alter column totalamount type numeric(10,2);

create or replace function update_promos() returns trigger as $update_promos$
    begin

        PERFORM pg_sleep(5);

        update orders
        set netamount = (netamount * (1 + (old.promo / 100.0))) * (1 - ( new.promo / 100.0)), totalamount = (netamount * (1 + (old.promo / 100.0))) * (1 - ( new.promo / 100.0)) * ( 1 + tax/100)
        where orders.customerid = new.customerid and 
            orders.status is NULL;
        
        return new;
     
    end;
    
$update_promos$ language plpgsql;



create trigger update_promo 
after update 
of promo
on customers for each row 
execute procedure update_promos();