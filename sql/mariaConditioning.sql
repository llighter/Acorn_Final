drop table nextGen;

create table nextGen(
	`reldate` DATE NULL DEFAULT NULL,
	`nextGenReldate` DATE NULL DEFAULT NULL,
	`genGap` INT(11) NULL DEFAULT NULL
	
)COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB;


select distinct(relDate) from info_copy order by relDate;


insert into nextGen 
 values 
 (STR_TO_DATE('2009-11-28', '%Y-%m-%d'), STR_TO_DATE('2010-09-07', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2010-09-07', '%Y-%m-%d'), STR_TO_DATE('2009-11-28', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2010-09-07', '%Y-%m-%d'), STR_TO_DATE('2011-11-11', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2010-09-07', '%Y-%m-%d'), STR_TO_DATE('2011-11-11', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2010-09-10', '%Y-%m-%d'), STR_TO_DATE('2011-11-11', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2010-09-10', '%Y-%m-%d'), STR_TO_DATE('2011-11-11', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2011-11-11', '%Y-%m-%d'), STR_TO_DATE('2012-12-07', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2011-11-11', '%Y-%m-%d'), STR_TO_DATE('2012-12-07', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2012-12-07', '%Y-%m-%d'), STR_TO_DATE('2013-10-25', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2012-12-07', '%Y-%m-%d'), STR_TO_DATE('2013-10-25', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2013-10-25', '%Y-%m-%d'), STR_TO_DATE('2014-10-31', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2013-10-25', '%Y-%m-%d'), STR_TO_DATE('2014-10-31', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2014-10-31', '%Y-%m-%d'), STR_TO_DATE('2015-10-23', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2014-10-31', '%Y-%m-%d'), STR_TO_DATE('2015-10-23', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2015-10-23', '%Y-%m-%d'), STR_TO_DATE('2016-05-10', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2015-10-23', '%Y-%m-%d'), STR_TO_DATE('2016-05-10', '%Y-%m-%d'))) ),
 (STR_TO_DATE('2016-05-10', '%Y-%m-%d'), STR_TO_DATE('2016-10-21', '%Y-%m-%d'), abs(DATEDIFF(STR_TO_DATE('2016-05-10', '%Y-%m-%d'), STR_TO_DATE('2016-10-21', '%Y-%m-%d'))) );

create table info01
as select i.*, n.nextGenReldate, n.genGap from info_copy as i
left join nextGen as n 
on i.reldate = n.reldate;








