-- 1. Количество исполнителей в каждом жанре
select g.genre_name as "Название жанра", coalesce(k.cnt, 0) as "Количество исполнителей"  from main.genres g  
left outer join 
	(select s.genre_id as id, count(s.singer_id) as cnt from main.singers_genres s
	group by s.genre_id) as k
on g.id = k.id
order by 2 desc, g.genre_name 

-- 2. Количество треков вошедших в альбомы 2019-2020 гг.
select count(s.id) as "Количество треков" from main.singles s 
where s.album_id in (select a.id from main.albums a where a.release_year between 2019 and 2020)

-- 3. Средняя продолжительность треков по каждому альбому
select a.album_name as "Назване альбома", 
	to_char((coalesce(avg(s.duration / 1000), 0)|| ' second')::interval,'MI:SS') as "Средняя длительность трека" 
	from main.singles s 
right outer join main.albums a on s.album_id = a.id 
group by a.album_name 
order by 2 desc

-- 4. Все исполнители, которые не выпустили альбомы в 2020 году
select s.singer_name as "Исполнитель" from main.singers s
where s.id not in (
	select sa.singer_id from main.singers_albums sa 
	join main.albums b on sa.album_id = b.id 
	where b.release_year = 2021)
order by 1

-- 5. Названия сборников, в которых присутствует конкретный исполнитель
select c.collection_name as "Название сборника" from main.collections c 
join main.collections_singles cs on c.id = cs.collection_id 
join main.singles s on cs.single_id = s.id 
join main.albums a2 on s.album_id = a2.id 
join main.singers_albums sa on a2.id = sa.album_id 
join main.singers_albums sa2 on sa.singer_id = sa2.singer_id 
join main.singers s2 on sa2.singer_id = s2.id 
where s2.singer_name ilike '%Лепс%'
group by 1

-- 6. Название альбомов, в которых присутствуют исполнители более 1 жанра
select a.album_name as "Название альбома", s.singer_name as "Исполнитель", count(sg.genre_id) as "Кол-во жанров"  from main.albums a 
join main.singers_albums sa on a.id = sa.album_id 
join main.singers s on sa.singer_id = s.id 
join main.singers_genres sg on s.id = sg.singer_id 
group by a.album_name, s.singer_name 
having count(sg.singer_id) > 1
order by s.singer_name, a.album_name 

-- 7. Наименование треков, которые не входят в сборники
select distinct s.single_name as "Наименование трека" from main.singles s 
left join main.collections_singles cs on s.id = cs.single_id 
where cs.single_id is null
order by 1

-- 8. Исполнителя(-ей), написавшего самый короткий по продолжительности трек
select s.singer_name as "Исполнитель", s3.single_name as "Трек",
	to_char((coalesce((s3.duration / 1000), 0)|| ' second')::interval,'MI:SS') as "Длительность трека" 
	from main.singers s 
join main.singers_albums sa on s.id = sa.singer_id 
join main.albums s2 on sa.album_id = s2.id 
join main.singles s3 on s2.id = s3.album_id 
where s3.duration in (select min(s4.duration) from main.singles s4)
order by 1, 2

-- 9. Название альбомов, содержащих наименьшее количество треков
select a.album_name "Название альбома", count(s.id) as "Кол-во треков" from main.albums a 
left join main.singles s on a.id = s.album_id 
group by 1
having count(s.id) =
	(select min(cnt) from (select s2.album_id as id, count(s2.id) as cnt from main.singles s2
		group by s2.album_id) c)
order by 1
