from datetime import datetime

def timeLog(logMessage):
    logedMessage=datetime.now().strftime("%d-%m-%Y %H:%M:%S") + \
        " : " + logMessage
    print(logedMessage)