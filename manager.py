import schedule
import time

import configparser

from pytimedinput import timedInput

# get modules
from dumpModule import backupJob
from resetModule import resetJob
# from exportTED import exportTED2CSV

def job():
    backupJob()
    # exportTED2CSV()   

def main():

    config = configparser.ConfigParser()
    config.read('dumpTED.conf')

    print(("Iniciando proceso de compilación TED"))
    userText, timedOut = timedInput("Escriba 'reset' para iniciar compilación desde 0. O espere 5 segundos para compilación regular...")
    if(timedOut):
        print("Iniciando proceso de compilación regular...")

        # from mssqlUpdater run backupJob
        job()

        execTime=config['default']['DUMP_EXEC_TIME']

        schedule.every().day.at(execTime).do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
        
    else:
        if userText =='reset':
            print("Iniciando compilacion desde 0...")
            resetJob()
        else:
            print(f"El comando: '{userText}' no es una instrucción válida")

if __name__ == "__main__":
    main()