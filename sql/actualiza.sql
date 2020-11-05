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

--no se si el email es obligatorio al registrarse, por si lo es
alter table customers alter column email varchar NOT NULL;

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

)
--insertamos los distintos paises que haya en imdb_countries
--select distinct para seleccionar todos los países que sean distintos (una sola vez)

insert into countries(country_name) select distinct country from imdb_moviecountries;

--actualizamos los datos en la tabla imdb_countries tras los cambios creados con la nueva tabla
--el tipo de dato de country será ahora un entero, asi que lo cambiamos
--(no se si el orden del alter y el update es importante)

alter table imdb_moviecountries alter column country integer;

--actualizamos los datos de la tabla imdb_moviecountries, y cambiamos los paises por su id correspondiente
update imdb_moviecountries
set country = countries.country_id
from countries
where countries.country_name = imdb_moviecountries.country

--vamos a hacer el mismo proceso con las tablas de imdb_moviegenres y imdb_movielanguages
create table genres (
    genre_id serial primary key,
    genre_name varchar(50) not null

)

insert into genres(genre_name) select distinct genre from imdb_moviegenres;
alter table imdb_moviegenres alter column genre integer;

update imdb_moviegenres
set genre = countries.genre_id
from genres
where genres.genre_name = imdb_moviegenres.genre

create table languages (
    language_id serial primary key,
    language_name varchar(50) not null

)

insert into languages(laguage_name) select distinct language from imdb_movielanguages;
alter table imdb_movielanguages alter column language integer;

update imdb_movielanguages
set language = languages.language_id
from languages
where languages.language_name = imdb_movielanguages.language