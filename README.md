Escáner de Red - Herramienta de Escaneo con Nmap

Este es un script de Python que utiliza la biblioteca nmap para realizar diferentes tipos de escaneos a dispositivos en una red. Permite escanear puertos abiertos, identificar servicios, detectar posibles vulnerabilidades y obtener información sobre el sistema operativo de los hosts en la red.
Requisitos

Para ejecutar este script, necesitas tener instalado Python y la biblioteca nmap en tu sistema. Además, el script realiza pings para verificar la disponibilidad de los hosts antes de proceder con el escaneo.
Instalación de dependencias

    Instalar Python: Si aún no tienes Python, puedes descargarlo desde aquí.

    Instalar la biblioteca python-nmap: Puedes instalar la biblioteca python-nmap usando pip con el siguiente comando:

    pip install python-nmap

    Esta biblioteca se utiliza para interactuar con Nmap desde Python.

    Instalar Nmap: Debes tener Nmap instalado en tu sistema. Puedes descargarlo desde su sitio web oficial: Nmap Download.

Uso

    Clona o descarga el repositorio en tu máquina local.

    Abre una terminal o consola de comandos y navega hasta la carpeta donde se encuentra el archivo escaneo_red.py (o el nombre del archivo que hayas dado al script).

    Ejecuta el script con el siguiente comando:

    python escaneo_red.py

    Menú de Opciones: Al ejecutar el script, verás un menú con las siguientes opciones de escaneo:
        1. Escaneo Normal (básico): Escaneo básico de puertos (1-1024).
        2. Escaneo Silencioso (básico + SYN): Realiza un escaneo SYN (sin conexión) de puertos (1-1024).
        3. Escaneo Completo (Detallado): Escaneo completo que incluye la versión de los servicios.
        4. Escaneo Completo Silencioso (SYN + Detallado): Combinación de un escaneo SYN con detalles de los servicios.
        5. Escaneo Completo SYN (SYN ++ Detallado): Escaneo más profundo que incluye detección de sistema operativo y vulnerabilidades.
        6. Salir: Sale del programa.

    Proceso de escaneo: Después de seleccionar una opción y proporcionar la IP o nombre de host del objetivo, el script realizará un ping para verificar si el host está activo. Luego, se ejecutará el escaneo basado en la opción seleccionada.

    Resultados: Al finalizar el escaneo, el script mostrará los resultados, que incluyen:
        Estado del host (activo o inactivo).
        Puertos abiertos, servicios y versiones detectadas.
        Información sobre el sistema operativo (si es detectado).
        Vulnerabilidades conocidas (si son encontradas).

Notas Importantes

    Precaución: Asegúrate de tener permiso explícito para escanear las redes y dispositivos. Realizar escaneos no autorizados puede ser ilegal en muchos lugares.
    El script está diseñado para ser ejecutado en sistemas Windows, Linux y macOS.
