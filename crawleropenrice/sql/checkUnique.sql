select * from
(
SELECT count(*) as num FROM `crawlingList` group by url
) table2
group by table2.num
