-- СОЗДАНИЕ СХЕМЫ "main"

CREATE SCHEMA main AUTHORIZATION postgres;



-- СОЗДАНИЕ ТАБЛИЦЫ ЖАНРОВ МУЗЫКИ "genres" В СХЕМЕ "main"

CREATE TABLE main.genres (
	id serial4 NOT null primary key, -- Идентификатор
	genre_name varchar(25) NOT null unique, -- Название жанра
	description text null -- Описание жанра
);
COMMENT ON TABLE main.genres IS 'Жанры музыки';

-- Column comments

COMMENT ON COLUMN main.genres.id IS 'Идентификатор';
COMMENT ON COLUMN main.genres.genre_name IS 'Название жанра';
COMMENT ON COLUMN main.genres.description IS 'Описание жанра';



-- СОЗДАНИЕ ТАБЛИЦЫ ИСПОЛНИТЕЛЕЙ "singers" В СХЕМЕ "main"

CREATE TABLE main.singers (
	id serial4 NOT null primary key, -- Идентификатор
	singer_name varchar(100) NOT null unique, -- Имя исполнитея
	nickname varchar(25) null, -- Псевдоним исполнителя
	biography text null -- биография исполнителя
);
COMMENT ON TABLE main.singers IS 'Исполнители';

-- Column comments

COMMENT ON COLUMN main.singers.id IS 'Идентификатор';
COMMENT ON COLUMN main.singers.singer_name IS 'Имя исполнитея';
COMMENT ON COLUMN main.singers.nickname IS 'Псевдоним исполнителя';
COMMENT ON COLUMN main.singers.biography IS 'Биография исполнителя';



-- СОЗДАНИЕ СВЯЗНОЙ ТАБЛИЦЫ ИСПОЛНИТЕЛИ-ЖАНРЫ "singers_genres" В СХЕМЕ "main"

CREATE TABLE main.singers_genres (
	genre_id int4 references main.genres(id), -- Идентификатор жанра исполнителя
	singer_id int4 references main.singers(id), -- Идентификатор жанра исполнителя
	constraint pk_singers_genres primary key (genre_id, singer_id) 
);
COMMENT ON TABLE main.singers_genres IS 'Исполнители-жанры';

-- Column comments

COMMENT ON COLUMN main.singers_genres.genre_id IS 'Идентификатор жанра исполнителя';
COMMENT ON COLUMN main.singers_genres.singer_id IS 'Идентификатор исполнителя';



-- СОЗДАНИЕ ТАБЛИЦЫ АЛЬБОМОВ ПЕСЕН "albums" В СХЕМЕ "main"

CREATE TABLE main.albums (
	id serial4 NOT null primary key, -- Идентификатор
	album_name varchar(50) NOT null, -- Название альбома
	description text null, -- Описание альбома
	release_year int4 null check (((release_year >= 1900) AND (release_year <= 9999))), -- Год выхода альбома
	picture bytea null -- Логотип альбома
);
COMMENT ON TABLE main.albums IS 'Альбомы';

-- Column comments

COMMENT ON COLUMN main.albums.id IS 'Идентификатор';
COMMENT ON COLUMN main.albums.album_name IS 'Название альбома';
COMMENT ON COLUMN main.albums.description IS 'Описание альбома';
COMMENT ON COLUMN main.albums.release_year IS 'Год выхода альбома';
COMMENT ON COLUMN main.albums.picture IS 'Логотип альбома';



-- СОЗДАНИЕ СВЯЗНОЙ ТАБЛИЦЫ ИСПОЛНИТЕЛИ-АЛЬБОМЫ "singers_albums" В СХЕМЕ "main"

CREATE TABLE main.singers_albums (
	singer_id int4 references main.singers(id), -- Идентификатор исполнителя
	album_id int4 references main.albums(id), -- Идентификатор альбома
	constraint pk_singers_albums primary key (singer_id, album_id) 
);
COMMENT ON TABLE main.singers_albums IS 'Исполнители-альбомы';

-- Column comments

COMMENT ON COLUMN main.singers_genres.genre_id IS 'Идентификатор исполнителя';
COMMENT ON COLUMN main.singers_genres.singer_id IS 'Идентификатор альбома';



-- СОЗДАНИЕ ТАБЛИЦЫ ПЕСЕН "singles" В СХЕМЕ "main"

CREATE TABLE main.singles (
	id serial4 NOT null primary key, -- Идентификатор
	single_name varchar(100) NOT null, -- Название трека
	description text null, -- Описание трека
	duration int4 null, -- Длительность(мс) трека
	picture bytea null, -- Логотип трека
	album_id int4 references main.albums(id) -- Идентификатор альбома
);
COMMENT ON TABLE main.singles IS 'Треки';

-- Column comments

COMMENT ON COLUMN main.singles.id IS 'Идентификатор';
COMMENT ON COLUMN main.singles.single_name IS 'Название трека';
COMMENT ON COLUMN main.singles.description IS 'Описание трека';
COMMENT ON COLUMN main.singles.duration IS 'Длительность(мс) трека';
COMMENT ON COLUMN main.singles.picture IS 'Логотип трека';
COMMENT ON COLUMN main.singles.album_id IS 'Идентификатор альбома';



-- СОЗДАНИЕ ТАБЛИЦЫ СБОРНИКОВ ПЕСЕН "collections" В СХЕМЕ "main"

CREATE TABLE main.collections (
	id serial4 NOT null primary key, -- Идентификатор
	collection_name varchar(40) NOT null, -- Название сборника
	description text null, -- Описание сборника
	release_year int4 null check (((release_year >= 1900) AND (release_year <= 9999))), -- Год выхода сборника
	picture bytea null -- Логотип сборника
);
COMMENT ON TABLE main.collections IS 'Сборники';

-- Column comments

COMMENT ON COLUMN main.collections.id IS 'Идентификатор';
COMMENT ON COLUMN main.collections.collection_name IS 'Название сборника';
COMMENT ON COLUMN main.collections.description IS 'Описание сборника';
COMMENT ON COLUMN main.collections.release_year IS 'Год выхода сборника';
COMMENT ON COLUMN main.collections.picture IS 'Логотип сборника';



-- СОЗДАНИЕ СВЯЗНОЙ ТАБЛИЦЫ СБОРНИКИ-ТРЕКИ "collections_singles" В СХЕМЕ "main"

CREATE TABLE main.collections_singles (
	collection_id int4 references main.collections(id), -- Идентификатор сборника
	single_id int4 references main.singles(id), -- Идентификатор трека
	constraint pk_collections_singles primary key (collection_id, single_id) 
);
COMMENT ON TABLE main.collections_singles IS 'Сборники-треки';

-- Column comments

COMMENT ON COLUMN main.collections_singles.collection_id IS 'Идентификатор сборника';
COMMENT ON COLUMN main.collections_singles.single_id IS 'Идентификатор трека';
