# Compilador-TED


El proyecto está compuesto por varios archivos de Python que trabajan en conjunto para realizar una tarea específica: la compilación de datos TED (Trabajadores del Estado con Despacho) y la generación de copias de seguridad (backups) de esos datos.

El archivo principal del proyecto es "manager.py". Este archivo es el punto de entrada del programa y contiene la función principal "main()". Veamos paso a paso cómo funciona el proyecto:

manager.py:

Este archivo importa las bibliotecas necesarias y otros archivos del proyecto.
Lee la configuración del archivo "dumpTED.conf", que contiene algunas variables de configuración importantes.
La función "main()" inicia el proceso de compilación de datos TED.
dumpTED.conf:

Este archivo de configuración contiene variables como la hora de ejecución del programa, rutas de archivos y listas de archivos a considerar para la compilación.
auxiliar.py:

Este archivo contiene funciones útiles, como "timeLog(logMessage)", que se utiliza para registrar mensajes de tiempo en los registros.
dumpModule.py:

Contiene la función "backupJob()", que es responsable de realizar la compilación y respaldo de los datos TED.
Esta función realiza una comparación entre los datos antiguos y los datos nuevos para detectar cambios en los archivos TED.
Los archivos TED incluyen "cabeceraexpedientesXXXX.txt" y "detalleexpedientesXXXX_v3.txt" (donde XXXX representa el año).
resetModule.py:

Este archivo contiene la función "resetJob()", que es similar a "backupJob()", pero se utiliza para una compilación desde cero.
Si se le pasa el texto "reset" al programa, se ejecutará la compilación desde cero.
exportTED.py:

Este archivo tiene la función "exportTED2CSV()", que se utiliza para exportar los datos compilados en formato CSV.
Se generan dos archivos CSV, uno para los datos de cabecera y otro para los detalles de las transacciones TED.
Otras funcionalidades:

El proyecto utiliza la biblioteca "schedule" para programar tareas y ejecutar la función "backupJob()" diariamente a una hora específica.
El proyecto utiliza la biblioteca "pytimedinput" para recibir una entrada del usuario y, en función de esta entrada, ejecutar "resetJob()" para una compilación desde cero o iniciar la compilación regular.
En resumen, el primer proyecto "dumpTED" está diseñado para realizar compilaciones regulares de datos TED y realizar copias de seguridad. La compilación consiste en detectar cambios en los archivos TED y actualizar la base de datos SQLite utilizada para almacenar los datos compilados. También ofrece la opción de realizar una compilación desde cero si el usuario lo solicita.

Es importante mencionar que este análisis se basa en la revisión de los archivos proporcionados. Si hay más funcionalidades en otros archivos que no se han mostrado aquí, es posible que haya más detalles en el funcionamiento del proyecto.
