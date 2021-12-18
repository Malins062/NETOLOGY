-- Альбомы релиза 2018 года
select a.album_name as "Название альбома", a.release_year as "Год релиза", a.description as "Описание" from main.albums a 
where a.release_year = 2018

-- Максимально длинный трек
select s.duration as "Длительность, мс", s.single_name as "Наимнование трека" from main.singles s 
order by s.duration desc 
limit 1

-- Треки, длительность которых не менее 3,5 минут (210 000 мс)
select s.duration as "Длительность, мс", s.single_name as "Наимнование трека" from main.singles s 
where s.duration >= 210000
order by s.duration desc, s.single_name 

-- Сборники релиза 2018-2021 годов включительно
select c.collection_name as "Название альбома", c.release_year as "Год релиза", c.description as "Описание" from main.collections c  
where c.release_year between 2018 and 2021
order by c.release_year, c.collection_name 

-- Исполнители, чье имя состоит из одного слова
select s.singer_name as "Исполнитель", s.nickname as "Псевдоним", s.biography as "Биография" from main.singers s  
where s.singer_name not like '% %'
order by s.singer_name 

-- Название треков со словом "мой" / "my"
select s2.single_name as "Название трека", s2.duration as "Длительность" from main.singles s2 
where s2.single_name ilike '% мой' or s2.single_name ilike  '% мой %' or s2.single_name ilike  'мой %' or
      s2.single_name ilike '% my' or s2.single_name ilike  '% my %' or s2.single_name ilike  'my %' 
order by s2.single_name 

