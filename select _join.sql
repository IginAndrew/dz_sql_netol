SELECT count(artist.zhanr_id), zhanr.name  FROM artist
JOIN zhanr ON artist.zhanr_id  = zhanr.id 
group by zhanr.name
;


SELECT count(singl.id) FROM singl
JOIN album ON singl.album_id  = album.id 
WHERE album.years  > '2018-10-10' and album.years  < '2021-01-01';


SELECT avg(singl.long), album.name FROM singl
JOIN album ON singl.album_id  = album.id 
group by album.name
ORDER BY album.name 
;

select distinct artist.name  from artist
where artist.name not in (select distinct artist.name  from artist 
join album on album.artist_id = artist.id 
where album.id  in (select album.id  from album where album.years = '2020-10-10'))
;

SELECT distinct  sbornik.name  FROM sbornik  
JOIN singl ON sbornik.id = singl.sbornik_id 
JOIN album ON album.id  = singl.album_id 
JOIN artist ON album.artist_id = artist.id 
WHERE artist.name  = 'Цой'
;

SELECT album.name, artist.name FROM album 
JOIN artist ON album.artist_id = artist.id
GROUP BY album.name, artist.name
having  artist.name =  
(select artist.name from artist 
 GROUP BY artist.name
 HAVING COUNT(artist.name) > 1) 
;


SELECT singl.name, singl.sbornik_id  FROM singl 
WHERE  singl.sbornik_id is null  
;

SELECT artist.name FROM artist
JOIN album ON artist.id  = album.artist_id 
JOIN singl ON album.id  = singl.album_id 
WHERE singl.long = (select min(singl.long) from singl);

SELECT album.name, album_id  FROM album
JOIN singl ON album.id  = singl.album_id 
group by album.name, album_id  
HAVING COUNT(album_id) = (SELECT min(singl.album_id) FROM singl)
ORDER BY album_id asc
;