# RLV Video & Audio Download Script

Script interactivo en Python para descargar audios y vídeos de YouTube (y otros sitios soportados por yt-dlp). 

## Características

- Elegir entre descargar solo audio (incluye listas) o vídeo (incluye listas)
- Seleccionar de forma interactiva la calidad de vídeo entre los formatos disponibles
- Combinar automáticamente el vídeo elegido con el mejor audio disponible y exportar en MP4
- Elegir la carpeta de destino con detección automática de Descargas (fallback a Escritorio)

## Requisitos

- **Python 3.8 o superior**
- **yt-dlp** (última versión recomendada): `pip install -U yt-dlp`
- **FFmpeg** instalado y en el PATH del sistema (necesario para:
  - Combinar vídeo+audio (merge) en MP4
  - Convertir a MP3 en el modo audio)
- **Conexión a Internet**

### Notas importantes

- El script ya no usa pytube. Puede eliminarse de dependencias para evitar confusión
- Sin FFmpeg, yt-dlp no podrá unir streams ni convertir audio a mp3; el script mostrará advertencia

## Estructura del proyecto

```
script_descarga_audio-video/
├── assets/
│   └── Moncho_YT.icns
├── descargador/
│   ├── build_and_push.sh
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Makefile
│   ├── README.md
│   ├── requirements.txt
│   └── script_descarga.py
├── Docker-Hub/
│   └── docker-compose.yml
├── ejecutable/
│   └── windows/
│       ├── requirements.txt
│       └── script_descarga.py
├── README.md
└── script_descarga.exe
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/moncholv/script_descarga_audio-video.git
cd script_descarga_audio-video/descargador
```

### 2. Instalar dependencias de Python

```bash
pip install -U yt-dlp
```

### 3. Instalar FFmpeg

**Windows:** Descargar binarios, por ejemplo en `C:\ffmpeg\bin`, y añadir esa ruta al PATH del sistema. Verificar con `ffmpeg -version`.

**macOS:** 
```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install ffmpeg
```

## Uso

### Ejecutar el script

Desde la terminal en la carpeta "descargador":

- **Windows:** `python script_descarga.py`
- **macOS/Linux:** `python3 script_descarga.py`

### Flujo interactivo

1. **Elegir opción:**
   - Descargar audio
   - Descargar audios de lista de reproducción
   - Descargar vídeo
   - Descargar vídeos de lista de reproducción

2. **Pegar la URL** (vídeo o playlist)

3. **Elegir carpeta de destino**. Si no se escribe nada, se sugiere automáticamente Descargas; si no existe, fallback a Escritorio. También puede usarse una variable de entorno para fijarla.

4. **En modo vídeo** (3 o 4), se listan las calidades disponibles (resolución, fps, contenedor, e indicación de si traen audio o no). Elegir un número o pulsar Enter para "best".

5. El script descarga y, si es vídeo, combina el itag de vídeo elegido con el mejor audio disponible (m4a) y genera un archivo MP4 final.

6. Al finalizar, el script espera a que se pulse Enter para salir.

## Selección de carpeta de destino

El script determina la carpeta de Descargas del usuario:

- **Windows:** Consulta el registro para obtener la carpeta Descargas; si falla, usa `%UserProfile%\Downloads`; si tampoco existe, usa Escritorio
- **macOS/Linux:** Usa `$HOME/Downloads`; si no existe, usa Escritorio

### Variable de entorno

Se puede establecer la variable de entorno `DESTINO_DESCARGAS` para forzar una carpeta por defecto sin preguntar:

**Windows (PowerShell):**
```powershell
setx DESTINO_DESCARGAS "C:\Users\TU_USUARIO\Downloads\YT"
```

**macOS/Linux (bash/zsh):**
```bash
export DESTINO_DESCARGAS="$HOME/Downloads/YT"
```

Si la carpeta no existe, el script la crea automáticamente.

## Detalles del funcionamiento

### Audio (opciones 1 y 2)
- Usa formato `"bestaudio/best"` y postprocesa a MP3 con FFmpeg
- Requiere FFmpeg en PATH para la conversión

### Vídeo (opciones 3 y 4)
- La función `elegir_calidad(url)` lista formatos de vídeo disponibles (pueden estar "sin audio" por ser streams DASH)
- El script arma el formato final como: `"{itag_de_video}+bestaudio[ext=m4a]/best"`
- Hace merge con FFmpeg y fuerza contenedor final MP4 (`merge_output_format="mp4"`)

### Notas sobre "sin audio" en calidades altas
- Es lo esperado: YouTube distribuye vídeo y audio por separado en calidades medias/altas
- El script ya añade el mejor audio m4a disponible y hace el merge a MP4

## Ejemplos

### Descargar audio en MP3 de un solo vídeo
Opción 1, pegar URL, aceptar Descargas; se generará un .mp3 con el título del vídeo.

### Descargar vídeo 1080p con audio
Opción 3, pegar URL, aceptar Descargas, elegir una entrada 1080p (aunque figure "sin audio"), el script descargará ese vídeo y el mejor audio y los unirá en MP4.

### Descargar lista de reproducción
- Opción 2 para audio (mp3 por cada elemento)
- Opción 4 para vídeo (merge vídeo+audio por cada elemento)

## Ejecutar por terminal directamente (sin el script)

Comandos orientativos con yt-dlp:

### Ver formatos disponibles (para ver itags)
```bash
yt-dlp -F URL
```

### Descargar mejor vídeo + mejor audio y combinar en MP4
```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" URL
```

### Limitar a 1080p máximo
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" URL
```

### Elegir por itag (ej. vídeo 299 + audio 140)
```bash
yt-dlp -f "299+140" --merge-output-format mp4 -o "%(title)s.%(ext)s" URL
```

### Forzar salida a Descargas
- **Windows:** `-o "C:/Users/%USERNAME%/Downloads/%(title)s.%(ext)s"`
- **macOS/Linux:** `-o "$HOME/Downloads/%(title)s.%(ext)s"`

## Docker (opcional)

Si se desea empaquetar el entorno:

- Incluir Python, yt-dlp y FFmpeg en la imagen
- Montar un volumen local para persistir las descargas (por ejemplo `./descargas`)
- Ejecutar el contenedor indicando la URL y/o usar el modo interactivo si se desea el menú

### Ejemplo (orientativo)
```bash
docker-compose run descargador
```

Guardará los archivos en la carpeta local `./descargas` (si el compose está configurado para montar ese volumen).

## Solución de problemas

### "ffmpeg not found" o "You have requested merging… ffmpeg is not installed"
Instalar FFmpeg y añadir al PATH; verificar con `ffmpeg -version`.

### "Requested format is not available" o HTTP 403 en algunos formatos
Actualizar yt-dlp (`pip install -U yt-dlp`), probar otro formato/itag o usar "best".

### La lista muestra muchas entradas "sin audio"
Es normal; el script ya combina vídeo+audio automáticamente.

### Rutas con espacios o permisos insuficientes
Usar comillas en rutas y verificar permisos de escritura.

### Descargas lentas o bloqueadas
Reintentar más tarde, actualizar yt-dlp, o probar otra red.

## Estructura del script

- `verificar_ffmpeg()`: Advierte si FFmpeg no está en PATH
- `mostrar_menu()`: Menú interactivo de opciones
- `pedir_directorio_destino()`: Sugiere Descargas, fallback a Escritorio, o usa `DESTINO_DESCARGAS` si está definida; crea la carpeta si no existe
- `elegir_calidad(url)`: Lista calidades de vídeo y devuelve itag del vídeo elegido (o "best" si se pulsa Enter)
- `main()`: Orquesta el flujo:
  - Audio: `"bestaudio/best"` + postprocesado a MP3
  - Vídeo: `"{itag}+bestaudio[ext=m4a]/best"` con merge a MP4

## Licencia

Indica la licencia elegida (por ejemplo, MIT) y añade el archivo LICENSE al repositorio.

## Créditos

**Autoría:** moncholv en colaboración con Eddevios (Edu).

Basado en yt-dlp para descarga y FFmpeg para procesamiento.
