create function update_inventory() 
    returns trigger 
    begin 
        

    end;
    language plpgsql
AS $$


create trigger updInventory 
after update
on orders row 
execute procedure update_inventory