import configparser, sqlite3
from datetime import datetime
import pandas as pd

from auxiliar import timeLog


def exportTED2CSV():
    config = configparser.ConfigParser()
    config.read('dumpTED.conf')

    dbPath = config['work-paths']['PATH_PREPROC_DB']
    depositPath = config['work-paths']['PATH_DEPOSIT_FILES_REC']

    resultDF=queryEntireTable(dbPath,"NewTedLastUser")
    resultDF.to_excel(depositPath+"/ultimoTED.xlsx",index=False)
    timeLog(f'Archivo "ultimoTED" guardado en {depositPath}')

    resultDF=queryEntireTable(dbPath,"NewTedResoluciones")
    resultDF.to_excel(depositPath+"/Resoluciones.xlsx",index=False)
    timeLog(f'Archivo "Resolucion" guardado en {depositPath}')

def queryEntireTable(dbPath,tableName):
    conn=sqlite3.connect(dbPath)
    sqlqry=f"SELECT * FROM {tableName}"

    resultDF=pd.read_sql_query(sqlqry,conn)

    conn.close()

    updateDate=datetime.now().strftime('%Y-%m-%d')
    resultDF['actualizacion']=updateDate

    return resultDF