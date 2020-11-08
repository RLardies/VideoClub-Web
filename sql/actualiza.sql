--actualizamos el serial de customers, orders y products por posibles pérdidas de sincronización para que se incrementen
--los id's a partir del último presente
--(que es lo que se actualizará en nuestra base de datos segun se inscriban usuarios y compren peliculas, o añadamos pelis)
--usamos lock table en exclusive para que mientras estamos actualizando los id's de las tablas no se produzcan
--otras transacciones (no haya una condicion de carrera)
--usamos setval() con 3er parametro false para especificar el "siguiente valor a usar" y manejar correctamente las tablas
--en cualquier caso, incluso vacias
begin;
lock table orders in exclusive mode;
select setval('orders_orderid_seq', coalesce((select max(orderid) + 1 from orders), 1), false);
commit;

begin;
lock table customers in exclusive mode;
select setval('customers_customerid_seq', coalesce((select max(customerid) + 1 from customers), 1), false);
commit;

--borramos las columnas de usuario que no utilizamos en nuestra base de datos (al registrarse no se le piden esos datos)
alter table customers drop column address1;
alter table customers drop column address2;
alter table customers drop column city;
alter table customers drop column state;
alter table customers drop column zip;
alter table customers drop column country;
alter table customers drop column region;
alter table customers drop column phone;
alter table customers drop column creditcardtype;
alter table customers drop column creditcardexpiration;
alter table customers drop column age;
alter table customers drop column income;
--le metemos una columna de saldo
alter table customers add saldo numeric default 0;

--no se si el email es obligatorio al registrarse, por si lo es
alter table customers alter column email set NOT NULL;

--eliminamos también los atributos no necesarios de otras tablas

--eliminamos los atributos ascharacter y participation pues en la base de datos casi siempre
--se encuentran vacíos y además no los necesitamos en nuestra aplicacion

alter table imdb_directormovies drop column ascharacter;
alter table imdb_directormovies drop column participation;

alter table imdb_movielanguages drop column extrainformation;

--eliminamos ascharacter pues aparece en muchas ocasiones como vacío en nuestra base de datos
--y además no es relevante para nuestra aplicación, así como las columnas isvoice, isarchivefootage,
--isuncredited y creditsposition
alter table imdb_actormovies drop column ascharacter;
alter table imdb_actormovies drop column isvoice;
alter table imdb_actormovies drop column isarchivefootage;
alter table imdb_actormovies drop column isuncredited;
alter table imdb_actormovies drop column creditsposition;

--vamos a crear una tabla nueva para los distintos países, para evitar que este se repita en imdb_countries
create table countries (
    country_id serial primary key,
    country_name varchar(50) not null

);
--insertamos los distintos paises que haya en imdb_countries
--select distinct para seleccionar todos los países que sean distintos (una sola vez)

insert into countries(country_name) select distinct country from imdb_moviecountries;

--actualizamos los datos en la tabla imdb_countries tras los cambios creados con la nueva tabla
--el tipo de dato de country será ahora un entero, asi que lo cambiamos
--(no se si el orden del alter y el update es importante)

--actualizamos los datos de la tabla imdb_moviecountries, y cambiamos los paises por su id correspondiente
update imdb_moviecountries
set country = countries.country_id
from countries
where countries.country_name = imdb_moviecountries.country;

alter table imdb_moviecountries alter column country type integer using country::integer;

--vamos a hacer el mismo proceso con las tablas de imdb_moviegenres y imdb_movielanguages
create table genres (
    genre_id serial primary key,
    genre_name varchar(50) not null

);

insert into genres(genre_name) select distinct genre from imdb_moviegenres;

update imdb_moviegenres
set genre = genres.genre_id
from genres
where genres.genre_name = imdb_moviegenres.genre;

alter table imdb_moviegenres alter column genre type integer using genre::integer;

create table languages (
    language_id serial primary key,
    language_name varchar(50) not null

);

insert into languages(language_name) select distinct language from imdb_movielanguages;

update imdb_movielanguages
set language = languages.language_id
from languages
where languages.language_name = imdb_movielanguages.language;

alter table imdb_movielanguages alter column language type integer using language::integer;

--Vamos a establecer las claves primarias en aquellas tablas que no tienen una PK
--dado que la PK no se puede repetir, no podemos coger únicamente uno de los campos (un actor
--puede interpretar varias peliculas y una pelicula tiene varios actores)
alter table imdb_actormovies add constraint actormovies_PK primary key (actorid, movieid);

--de nuevo una misma pelicula puede estar en varios idiomas y por supuesto hay muchas peliculas en el mismo idioma
alter table imdb_movielanguages add constraint movielanguages_PK primary key (movieid, language);

--tenemos que crear una tabla auxiliar de orderdetail pues al intentar crear la PK da un duplicado 
--con la tupla (orderid, prod_id) con atributo quantity 2 y 1, en lugar de la suma, y esto no deberia ocurrir
create table orderdetail_aux as
    select orderid, prod_id, price, sum(quantity) as quantity
    from orderdetail
    group by orderid, prod_id, price;

drop table orderdetail;
alter table orderdetail_aux rename to orderdetail;

alter table orderdetail alter column quantity type integer using quantity::integer;
alter table orderdetail alter column quantity set not null;
alter table orderdetail alter column orderid set not null;
alter table orderdetail alter COLUMN prod_id set not null;

comment on column public.orderdetail.price IS 'price without taxes when the order was paid';

--un producto puede haber sido comprado en muchos pedidos diferentes, y un pedido puede tener muchos productos
alter table orderdetail add constraint orderdetail_PK primary key (orderid, prod_id);


--añadamos ahora las FK necesarias para relacionar nuestras tablas
--orderdetail esta relacionada con la tabla products y orders (products lo haremos mas abajo pues vamos a fusionar tablas)

alter table orderdetail add constraint orderdetail_FK1 foreign key (orderid) references orders(orderid) on delete cascade;

--orders estan relacionada con customers
--no pongo delete on cascade porque aunque se borre un usuario igual quiero mantener los pedidos que hizo
--con fines estadísticos
alter table orders add constraint orders_FK foreign key (customerid) references customers(customerid);

--imdb_actormovies esta relacionada con imdb_movies y imdb_actors
--si se elimina un actor o pelicula, se elimina su relacion en la tabla
alter table imdb_actormovies add constraint actormovies_FK1 foreign key (actorid) references imdb_actors(actorid);
alter table imdb_actormovies add constraint actormovies_FK2 foreign key (movieid) references imdb_movies(movieid);

--imdb_languages relacionada con nuestra nueva tabla languages
alter table imdb_movielanguages add constraint languages_FK1 foreign key (language) references languages(language_id) on delete cascade;

--imdb_countries relacionada con nuestra nueva tabla countries
alter table imdb_moviecountries add constraint countries_FK1 foreign key (country) references countries(country_id) on delete cascade;

--imdb_genres relacionada con nuestra nueva tabla genres
alter table imdb_moviegenres add constraint lgenres_FK1 foreign key (genre) references genres(genre_id) on delete cascade;

--no usamos en ningun momento on update cascade porque no se debe usar respecto a campos autoincrementales
--como son las primary keys, y en principio no queremos que se actualice ninguna pk que esté linkeada con cualquier otra tabla

--podriamos fusionar las tablas inventory y products porque realmente no ganamos nada teniendolas por separado
create table products_aux as
  (select products.*, 
          inventory.stock, 
          inventory.sales
   from   products 
          left join inventory 
                  on products.prod_id = inventory.prod_id);

drop table inventory;
drop table products;
alter table products_aux rename to products;

alter table products add constraint prod_pkey primary key (prod_id); 
alter table products add constraint prod_fkey foreign key (movieid) references imdb_movies (movieid);

alter table products alter column prod_id set NOT NULL;
alter table products alter column movieid set NOT NULL;
alter table products alter column price set NOT NULL;
alter table products alter column description set NOT NULL;
alter table products alter column stock set default 0;
alter table products alter column sales set default 0;

--creamos la secuencia que tenia asociada;
create sequence products_prod_id_seq owned by products.prod_id;

alter table products alter column  prod_id set default nextval('products_prod_id_seq');

begin;
lock table products in exclusive mode;
select setval('products_prod_id_seq', coalesce((select max(prod_id) + 1 from products), 1), false);
commit;

--añadimos las foreign key que dependian de products
alter table orderdetail add constraint orderdetail_FK2 foreign key (prod_id) references products(prod_id);

--añadimos una tabla nueva para alertar de la falta de stock de alguna pelicula, sin primary key pues puede 
--agotarse el mismo producto varias veces, y con la fecha en la que se agotó para saber cuales son los productos más populares

create table no_stock (
    prod_id integer not null,
    orderdate date,
    foreign key (prod_id) references products(prod_id)
);
