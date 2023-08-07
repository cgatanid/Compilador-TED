-- DROP VIEW IF EXISTS ViewTedResoluciones;
-- CREATE VIEW ViewTedResoluciones AS
-- --obtiene los datos de los documentos "resolución" con su número, fecha y materia. excluye los registros de resoluciones hechas pero no firmadas
-- --utiliza un la vista "headMemo" para conseguir el nombre del creador inicial de cada memo
-- SELECT a.numero_expediente,a.numero_documento,a.desc_tipodoc AS tipodocumento,a.fecha_documento_origen AS fecha_creacion,b.nombreautor,b.unidadautor,a.materia
-- FROM NewTedHeaders AS a
-- LEFT JOIN headMemoTED AS b ON b.numero_expediente=a.numero_expediente
-- WHERE a.desc_tipodoc='Resolucion' AND a.numero_documento IS NOT NULL;

SELECT * FROM ViewTedResoluciones;