# RLV video & audio download script

Este es un script en Python interactivo que permite descargar audios y vídeos desde YouTube y otras fuentes como SoundCloud y otros muchos, tanto de forma individual como mediante listas de reproducción.
<br>Utiliza las bibliotecas `yt_dlp` y `pytube` y la herramienta de línea de comandos FFmpeg.

## Requisitos

Antes de ejecutar el script, asegúrate de tener lo siguiente instalado:

- Python 3.7 o superior
- [`yt_dlp`](https://github.com/yt-dlp/yt-dlp)
- [`pytube`](https://github.com/pytube/pytube)
- [FFmpeg](https://ffmpeg.org/) (necesario para convertir audios a mp3)

<br>Se pueden instalacr los paquetes de Python con pip (lo suyo es hacerlo en un entorno virtual de python):

```bash
pip install yt_dlp pytube
```

Debes tener FFmpeg instalado y accesible desde el PATH del sistema.
En Windows puedes añadir temporalmente el path del binario (sustituyendo la ruta del binario) con:
```
export PATH=$PATH:/c/Users/moncholv/Documents/apps_portables/ffmpeg/bin
```


Para usarlo, ejecuta el script desde terminal:
```
python download_yt.py
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
<br>Descargará el audio o vídeo en la ruta desde la que estás ejecutando el script.