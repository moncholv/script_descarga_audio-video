# RLV video & audio download script

Este es un script en Python interactivo que permite descargar audios y vídeos desde YouTube y otras fuentes como SoundCloud y otros muchos, tanto de forma individual como mediante listas de reproducción.
<br>Utiliza las bibliotecas `yt_dlp` y `pytube` y la herramienta de línea de comandos FFmpeg.

## Requisitos

Antes de ejecutar el script, asegúrate de tener lo siguiente instalado:

- Python 3.7 o superior
- [`yt_dlp`](https://github.com/yt-dlp/yt-dlp)
- [`pytube`](https://github.com/pytube/pytube)
- [FFmpeg](https://ffmpeg.org/) (necesario para convertir audios a mp3)

<br>Se pueden instalar ldependencias de Python con pip (lo suyo es hacerlo en un entorno virtual de python):

```bash
pip install yt_dlp pytube
```

El script utiliza FFmpeg para convertir el audio a formato MP3 por lo que necesita estar instalado y accesible desde el PATH del sistema.
En Windows puedes descargarlo desde https://ffmpeg.org/download.html
<br>Una vez descargado, extraemos el zip y añadimos temporalmente el path del binario (sustituyendo la ruta del binario) con:
```
export PATH=$PATH:/c/Users/moncholv/Documents/apps_portables/ffmpeg/bin
```
En mac o linux podemos instalar el paquete ffmpeg directamente.

## Como usar el script
Para usarlo, ejecuta el script desde terminal:
```
python script_descarga.py
```


Verás un menú interactivo con las siguientes opciones:

```
---- moncholv video & audio download script ----
Selecciona una opción:
1. Descargar audio.
2. Descargar audios de lista de reproducción.
3. Descargar vídeo.
4. Descargar vídeos de lista de reproducción.
```

Introduce el número correspondiente y luego proporciona la URL del vídeo o lista de reproducción según tu elección.

## Selección de carpeta de destino
El script permite seleccionar dónde se guardan los archivos descargados:

Puedes introducir una carpeta manualmente cuando se te pida, en caso de no indicar ninguna se descargará en la ruta donde se está ejecutando el script.

O bien, establecer la variable de entorno DESTINO_DESCARGAS para usarla automáticamente (muy útil en Docker).

Si la carpeta no existe, será creada automáticamente.

## Uso con Docker Compose
Puedes ejecutar este script en un contenedor Docker con todas las dependencias incluidas (Python, FFmpeg, yt-dlp, pytube).
```
docker-compose run descargador
```
Esto guardará los archivos descargados en la carpeta local ./descargas.

<br><br>Y hasta aquí que ya me he extendido demasiado...