# Moncholv video & audio download script

Script interactivo en Python para descargar audio y vídeo desde YouTube y muchas otras fuentes (ej. SoundCloud) de forma individual o desde listas de reproducción.
Utiliza las herramientas yt-dlp y ffmpeg.
Requiere Python 3.7 o superior. 
Es multiplataforma: Windows, MacOS (Intel/Silicon/M1/M2/M3) y Linux (Debian, Ubuntu, Arch, SteamOS).

---

## Requisitos

### Antes de ejecutar el script, asegúrate de tener lo siguiente instalado:

- Python 3.7 o superior
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) (gestiona descargas de vídeo/audio/playlists)
- [FFmpeg](https://ffmpeg.org/) (necesario para convertir audios a mp3 y mezclar vídeo/audio)

---

## Estructura del proyecto

```
Moncho_YT/
├── assets/
│   ├── Moncho_YT.icns      # Icono de la aplicación (macOS)
│   ├── Moncho_YT.ico       # Icono de la aplicación (Windows)
│   └── Moncho_YT.png       # Imagen de icono de la aplicación (Windows)
├── binaries/
│   ├── yt-dlp              # Binario yt-dlp macOS
│   ├── ffmpeg              # Binario ffmpeg macOS
│   ├── yt-dlp.exe          # Binario yt-dlp Windows
│   ├── ffmpeg.exe          # Binario ffmpeg Windows
│   ├── yt-dlp-linux        # Binario yt-dlp Linux
│   └── ffmpeg-linux        # Binario ffmpeg Linux
├── build/                  # Archivos temporales de construcción (generado por PyInstaller)
├── dist/                   # Ejecutables finales (generado por PyInstaller)
│   ├── Moncho_YT.exe       # Ejecutable Windows
│   ├── Moncho_YT           # Ejecutable Linux
│   └── Moncho_YT.app/      # Aplicación empaquetada (macOS)
├── docker/
│   └── docker-compose.yml  # Configuración Docker
├── venv/                   # Entorno virtual de Python
├── launcher.py             # Script lanzador (si aplica)
├── Makefile                # Comandos automatizados
├── Moncho_YT_app.spec      # Configuración PyInstaller (macOS)
├── Moncho_YT_windows.spec  # Configuración PyInstaller (Windows)
├── Moncho_YT_linux.spec    # Configuración PyInstaller (Linux)
├── README.md               # Este archivo
├── requirements.txt        # Dependencias Python
└── script_descarga.py      # Script principal
```

---

## Instalación de dependencias

El script utiliza FFmpeg para convertir audio a formato MP3, por lo que debe estar instalado y accesible desde el PATH del sistema.

### Windows:
Descarga FFmpeg desde https://ffmpeg.org/download.html y añade el binario a tu PATH.

Una vez descargado, extraemos el zip y añadimos temporalmente el path del binario (sustituyendo la ruta del binario) con:
```bash
set PATH=%PATH%;C:\ruta\a\ffmpeg\bin
```

### macOS:
```bash
brew install ffmpeg
```

### Linux:

**Debian/Ubuntu:**
```bash
sudo apt install ffmpeg
```

**Fedora:**
```bash
sudo dnf install ffmpeg
```

**Arch:**
```bash
sudo pacman -S ffmpeg
```

---

## Instalación desde código fuente

### Python y yt-dlp

Lo ideal es usar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

O puedes instalar yt-dlp con Homebrew (Mac):

```bash
brew install yt-dlp
```

---

## Cómo usar el script

Desde código fuente:

```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
python3 script_descarga.py
```

O simplemente:

```bash
python script_descarga.py
```

### Menú interactivo:

```
---- Moncholv video & audio download script ----
Selecciona una opción:
1. Descargar video rápido (menor calidad)
2. Descargar vídeo (elegir calidad)
3. Descargar vídeos de lista de reproducción
4. Descargar audio
5. Descargar audios de lista de reproducción
```

Introduce el número de la opción y luego proporciona la URL del vídeo o playlist correspondiente.

---

## Ejecutables precompilados

Si prefieres no instalar Python ni dependencias, puedes usar los ejecutables precompilados disponibles en [Releases](https://github.com/moncholv/script_descarga_audio-video/releases).

### **macOS (Intel y Apple Silicon/M1/M2/M3)**

1. Descarga `Moncho_YT.app.zip` desde Releases
2. Descomprime y mueve `Moncho_YT.app` a tu carpeta **Aplicaciones**
3. **Primera ejecución** (macOS puede bloquearlo por seguridad):
   - **Opción A:** Ve a **Preferencias del Sistema** > **Privacidad y seguridad** > **"Abrir de todos modos"**
   - **Opción B:** Ejecuta en Terminal:
     ```bash
     xattr -cr /Applications/Moncho_YT.app
     open /Applications/Moncho_YT.app
     ```
4. Haz doble clic en `Moncho_YT.app` para ejecutar

**Nota:** El ejecutable incluye `yt-dlp` y `ffmpeg`, no necesitas instalar nada más.

---

### **Windows (64-bit)**

1. Descarga `Moncho_YT-Windows.zip` desde Releases
2. Descomprime el archivo
3. Ejecuta `Moncho_YT.exe`
4. **Si Windows Defender SmartScreen lo bloquea:**
   - Haz clic en **"Más información"**
   - Luego en **"Ejecutar de todas formas"**

**Nota:** El ejecutable incluye `yt-dlp` y `ffmpeg`.

---

### **Linux (Ubuntu, Debian, Fedora, Arch, SteamOS/Steam Deck)**

1. Descarga el ejecutable correspondiente desde Releases:
   - `Moncho_YT-Ubuntu` (Ubuntu/Debian/Mint/Pop!_OS)
   - `Moncho_YT-Fedora` (Fedora/RHEL/CentOS Stream)
   - `Moncho_YT-Arch` (Arch/Manjaro/EndeavourOS)
   - `Moncho_YT-SteamOS` (Steam Deck)

2. Dale permisos de ejecución:
```bash
chmod +x Moncho_YT-Ubuntu
```

3. Ejecuta desde terminal:
```bash
./Moncho_YT-Ubuntu
```

**Nota:** El ejecutable incluye `yt-dlp` y `ffmpeg`. Si tienes problemas, instala `ffmpeg` del sistema:

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Fedora:**
```bash
sudo dnf install ffmpeg
```

**Arch:**
```bash
sudo pacman -S ffmpeg
```

---

## Selección de carpeta de destino

El script permite seleccionar la carpeta de destino. Por defecto ofrece la carpeta de descargas estándar según tu sistema operativo.

Puedes introducir cualquier ruta manualmente cuando se te pida, y será creada si no existe.

También puedes usar la variable de entorno `DESTINO_DESCARGAS` si quieres personalizar la salida automáticamente (útil en Docker o scripts automatizados).

---

## Uso con Docker Compose

Puedes ejecutar este script en un contenedor Docker con todas las dependencias incluidas (Python, FFmpeg, yt-dlp):

```bash
docker-compose run descargador
```

Esto guardará los archivos descargados en la carpeta local `./descargas`.

---

## Compilar tus propios ejecutables

Si deseas compilar los ejecutables tú mismo desde el código fuente:

### Requisitos previos:
```bash
pip install pyinstaller
```

### Descargar binarios necesarios:

Los binarios de `yt-dlp` y `ffmpeg` deben estar en la carpeta `binaries/` antes de compilar.

### **macOS:**

```bash
mkdir -p binaries
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o binaries/yt-dlp
chmod +x binaries/yt-dlp
cp $(which ffmpeg) binaries/ffmpeg  # Si tienes ffmpeg instalado con Homebrew
```

**Compilar:**
```bash
source venv/bin/activate
pyinstaller --clean Moncho_YT_app.spec
```

El ejecutable estará en `dist/Moncho_YT.app`

---

### **Windows:**

**Descargar binarios:**
- `yt-dlp.exe`: https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
- `ffmpeg.exe`: https://github.com/BtbN/FFmpeg-Builds/releases (busca win64-gpl.zip)

Colócalos en `binaries/yt-dlp.exe` y `binaries/ffmpeg.exe`

**Compilar:**
```cmd
venv\Scripts\activate
pyinstaller --clean Moncho_YT_windows.spec
```

El ejecutable estará en `dist\Moncho_YT.exe`

---

### **Linux:**

**Descargar binarios:**

```bash
mkdir -p binaries
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o binaries/yt-dlp-linux
chmod +x binaries/yt-dlp-linux
```

**FFmpeg (descarga según distro):**

**Opción 1: Copiar del sistema**
```bash
# Ubuntu/Debian:
sudo apt install ffmpeg
cp $(which ffmpeg) binaries/ffmpeg-linux

# Arch:
sudo pacman -S ffmpeg
cp $(which ffmpeg) binaries/ffmpeg-linux
```

**Opción 2: Descarga estática universal desde [johnvansickle](https://johnvansickle.com/ffmpeg/)**
```bash
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
cp ffmpeg-*-amd64-static/ffmpeg binaries/ffmpeg-linux
chmod +x binaries/ffmpeg-linux
```

**Compilar en cada distribución:**

Idealmente compila en cada sistema operativo para mejor compatibilidad:

**Ubuntu/Debian:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --clean Moncho_YT_linux.spec
mv dist/Moncho_YT dist/Moncho_YT-ubuntu
```

**Arch/Manjaro:**
```bash
python -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --clean Moncho_YT_linux.spec
mv dist/Moncho_YT dist/Moncho_YT-arch
```

**SteamOS (Steam Deck):**
Usa el mismo proceso que Arch (SteamOS está basado en Arch), o compila directamente en el Steam Deck en modo escritorio.

El ejecutable estará en `dist/Moncho_YT`

---

**Importante:** Los binarios de `yt-dlp` y `ffmpeg` deben estar en la carpeta `binaries/` antes de compilar.

---

## Solución de problemas

### macOS: "La app está dañada y no se puede abrir"
```bash
xattr -cr /Applications/Moncho_YT.app
```

### Windows: SmartScreen bloquea la ejecución
Haz clic en "Más información" > "Ejecutar de todas formas"

### Linux: "Permiso denegado"
```bash
chmod +x Moncho_YT-Ubuntu
```

### Error: "yt-dlp no está disponible"
Instala yt-dlp en tu sistema:
```bash
pip install yt-dlp
```
o
```bash
brew install yt-dlp
```

### Error: "ffmpeg no está disponible"
Instala ffmpeg en tu sistema según tu plataforma (ver sección de instalación arriba)

### Error HTTP 403: Forbidden al descargar playlists
Actualiza yt-dlp:
```bash
pip install -U yt-dlp
```
o
```bash
brew upgrade yt-dlp
```

---

## Cambios principales en esta versión

- Ahora solo usa yt-dlp (pytube eliminado)
- Flujos y lógica separados para playlist y elementos individuales
- Selección automática de carpeta estándar multiplataforma (Windows, MacOS, Linux)
- Actualización automática de yt-dlp opcional
- Añadido soporte para playlist y cabeceras de navegador (user-agent) en las descargas para mayor compatibilidad
- Ejecutables standalone para todas las plataformas con binarios incluidos

---

## Créditos

- 👤 **Autor original**: [Moncholv](https://github.com/moncholv)  
- 🤝 **Colaboraciones y mejoras**: [Eddevios (Edu)](https://github.com/eddevios) | [eddevios.com](https://eddevios.com)

---