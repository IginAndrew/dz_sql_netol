SELECT name, years  FROM album  
WHERE years  >= '2018-01-01' and years  < '2019-01-01';

SELECT singl.name, singl.long  FROM singl
group by singl.name, singl.long
having  singl.long  =  (select max(long) from singl);


SELECT singl.name FROM singl
where long > '3:30:00';


SELECT name FROM album  
WHERE years  >= '2018-01-01' and years  <= '2020-12-31';


SELECT distinct name FROM artist  
WHERE name LIKE '%' ;


SELECT name FROM singl 
	WHERE name LIKE '%my%' or name LIKE '%мой%';