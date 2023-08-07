select distinct d.numero_expediente, d.nombreautor, d.desc_unidad, d.usuarioorigen, d.usuariodestino, d.fecha_creacion, d.fechaingresobandeja, d.fecha_acuse_recibo, d.fechadespacho, d.archivado
from (select DISTINCT d.numero_expediente,d.nombreautor, d.desc_unidad, d.usuarioorigen, d.usuariodestino, d.fecha_creacion, d.fechaingresobandeja, d.fecha_acuse_recibo, d.fechadespacho, d.archivado, d.id
from NewTedDetails as d left join NewTedHeaders as h on d.id=h.id where d.copia='f' and h.desc_tipodoc = 'Memorandum') as d 
inner join (
	select distinct d.numero_expediente, max(d.fechaingresobandeja) as MaxDate, min(d.fecha_creacion) as MinCreacion, min(d.id) as MinId
	from NewTedDetails as d left join NewTedHeaders as h on d.id=h.id 
	where d.copia='f' and h.desc_tipodoc = 'Memorandum'
	group by d.numero_expediente
) as tm on d.numero_expediente=tm.numero_expediente and d.fechaingresobandeja=tm.MaxDate and d.fecha_creacion=tm.MinCreacion and d.id=tm.MinId