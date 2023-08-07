import os, configparser

import urllib
import pyodbc
from sqlalchemy import create_engine
import pandas as pd

from auxiliar import timeLog

# load all enviroment variables and config files
from dotenv import load_dotenv
load_dotenv()

config = configparser.ConfigParser()
config.read('dumpTED.conf')

# set database and backups work paths
path = config['work-paths']['PATH_DUMP_FILES']
dbPath = config['work-paths']['PATH_PREPROC_DB']
backupPath = config['work-paths']['PATH_BACKUP_DUMPFILES']

# load work database
engine = create_engine(f'sqlite:///{dbPath}', echo=False)
sqlite_connection = engine.connect()

# load ted dump original path
sharedFiles = os.listdir(path)

def resetJob():

    # load ted dump original files from shared folder
    lista_cabeceras=[s.strip() for s in config['work-lists']['TED_LISTA_CABECERAS'].split(',')]
    lista_detalles=[s.strip() for s in config['work-lists']['TED_LISTA_DETALLES'].split(',')]

    timeLog("Iniciando proceso de actualización del compilado TED. Puedes cancelarlo apretando 'ctrl + c'")
    timeLog("Conectando con base de datos y carpetas de archivos")

    isChanges = 0

    for file in sharedFiles:

        try:
            if file in lista_cabeceras:
                   
                currentHeaders = pd.read_csv(path+'/'+file, sep=';')

                deltaNewHeaders = currentHeaders

                if not (deltaNewHeaders.empty):
                    tipoAgregacion='replace' if '2016' in file else 'append'
                    deltaNewHeaders.to_sql("NewTedHeaders", sqlite_connection, if_exists=tipoAgregacion)
                    currentHeaders.to_pickle(
                        backupPath+'backups/'+file.replace('.txt', '')+'.pkl')
                    timeLog(file.replace('.txt', '')+' fue actualizado')
                    isChanges += 1
                else:
                    timeLog(f'No se detectaron cambios en: {file}')
                

            if file in lista_detalles:
            
                currentDetails = pd.read_csv(path+'/'+file, sep=';',dtype={'numero_expediente':str, 'acuse_recibo':str, 'nombreautor':str, 'nombredestinatario':str, 'desc_cargo':str, 'desc_unidad':str, 'archivado':str, 'nombre_archivo':str, 'cms_id':float, 'id_padre':int, 'usuarioorigen':str, 'usuariodestino':str, 'fecha_creacion':str, 'fechaingresobandeja':str, 'fecha_acuse_recibo':str, 'fechadespacho':str, 'id_expediente':int, 'id':int, 'dias_en_despachar':int, 'dias_en_leer':int, 'copia':str})

                deltaNewDetails = currentDetails

                if not (deltaNewDetails.empty):
                    tipoAgregacion='replace' if '2016' in file else 'append'
                    deltaNewDetails.to_sql("NewTedDetails", sqlite_connection, if_exists=tipoAgregacion)
                    currentDetails.to_pickle(
                        backupPath+'backups/'+file.replace('.txt', '')+'.pkl')
                    timeLog(file.replace('.txt', '')+' fue actualizado')
                    isChanges += 1
                else:
                    timeLog(f'No se detectaron cambios en: {file}')

        except Exception as err:
            timeLog(f'Ha ocurrido un error con {file}. El proceso se ha saltado el archivo. {err}')


    if isChanges > 0:
    
        # Record the new table with last user on each TED
        qrySQL = open('sqlQueries/getLastUserTED-v2.sql', 'r').read()
        lastUserOnTED = pd.read_sql_query(qrySQL, sqlite_connection)
        qrySQL = open('sqlQueries/getAllResoluciones-v2.sql', 'r').read()
        allResoluciones = pd.read_sql_query(qrySQL, sqlite_connection)

        # Save table in the new location
        lastUserOnTED.to_sql("NewTedLastUser", sqlite_connection, if_exists='replace', index=False)
        allResoluciones.to_sql("NewTedResoluciones", sqlite_connection, if_exists='replace', index=False)

        # Update "autorunidad" field
        file = open('./sqlQueries/unidadAutorFix.sql', mode='r', encoding='utf-8').read()
        commandLines = file.split('\n')
        for cmd in commandLines:
            engine.execute(cmd)

        timeLog('La base de datos de transición fue actualizada')

        lastUserOnTED = pd.read_sql_query('select * from NewTedLastUser', sqlite_connection)
        allResoluciones = pd.read_sql_query('select * from NewTedResoluciones', sqlite_connection)

        params = urllib.parse.quote_plus(os.getenv("MSSQL_CONN"))

        # Database settings
        mssql_connection = create_engine(
            'mssql+pyodbc:///?odbc_connect=%s' % params)
        allResoluciones.to_sql(
            "NewTedResoluciones", mssql_connection, if_exists='replace', index=False)
        lastUserOnTED.to_sql("NewTedLastUser", mssql_connection,
                             if_exists='replace', index=False)

        timeLog("La base de datos MS SQL Server ha sido actualizada")

    else:
        timeLog('El proceso terminó sin aplicar cambio alguno')

    timeLog('El proceso se ha completado, se volverá a ejecutar automáticamente mañana a las 05:00 am...')

__name__ = "generalToken"