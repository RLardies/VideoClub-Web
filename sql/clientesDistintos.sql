create or replace function clientesDistintos(fecha integer, totalAmount integer)
    returns integer

begin
    return query



end;
$$  language plpgsql;

select * from  clientesDistintos(19000, 320000);