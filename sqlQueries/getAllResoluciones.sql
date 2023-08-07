select r.numero_expediente,r.desc_tipodoc,r.numero_documento,r.fecha_documento_origen,r.materia, u.nombreautor ,o.desc_unidad
from (SELECT numero_expediente, desc_tipodoc, numero_documento,fecha_documento_origen,materia FROM NewTedHeaders WHERE desc_tipodoc='Resolucion') as r 
left join (
select numero_expediente, nombreautor,min(min_fecha_creacion) from autorMemos group by numero_expediente
) as u on r.numero_expediente=u.numero_expediente
left join (
select DISTINCT nombredestinatario, desc_unidad from NewTedDetails
) as o on u.nombreautor = o.nombredestinatario