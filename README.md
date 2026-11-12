# Moncholv video & audio download script (v1.1.1)

Script interactivo en Python para descargar audio y vídeo desde YouTube y muchas otras fuentes (ej. SoundCloud) de forma individual o desde listas de reproducción.
Utiliza las herramientas yt-dlp y ffmpeg.
Requiere Python 3.10 o superior si lo ejecutas desde el código fuente (los ejecutables ya incluyen todo).
Es multiplataforma: Windows, MacOS (Intel/Silicon/M1/M2/M3) y Linux (Debian, Ubuntu, Arch, SteamOS).

> **Importante:** YouTube cambia a menudo y un `yt-dlp` antiguo provoca `HTTP Error 403: Forbidden`.
> Esta versión incluye yt-dlp **2026.10.26** y puede actualizarlo sola (opción `s` al arrancar o `--update`).


---

## Requisitos

### Ejecutables precompilados

No necesitas instalar nada: el `.app` / `.exe` / AppImage ya incluye `yt-dlp` y `ffmpeg`.

### Desde código fuente

- Python 3.10 o superior
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) (gestiona descargas de vídeo/audio/playlists)
- [FFmpeg](https://ffmpeg.org/) (necesario para convertir audios a mp3 y mezclar vídeo/audio)

El script usa el `yt-dlp` más moderno entre el actualizado por la app y el
incluido en `binaries/`; si ninguno arranca, cae al del `PATH`. Para FFmpeg usa
el incluido en `binaries/` (si arranca correctamente) o el del `PATH`.


---

## Estructura del proyecto

```
Moncho_YT/
├── assets/
│   ├── Moncho_YT.icns      # Icono de la aplicación (macOS)
│   ├── Moncho_YT.ico       # Icono de la aplicación (Windows)
│   └── Moncho_YT.png       # Imagen de icono de la aplicación (Windows)
├── binaries/
│   ├── yt-dlp              # Binario yt-dlp macOS (universal, 2026.10.26)
│   ├── ffmpeg              # Binario ffmpeg macOS
│   ├── yt-dlp.exe          # Binario yt-dlp Windows
│   ├── ffmpeg.exe          # Binario ffmpeg Windows
│   ├── yt-dlp-linux        # Binario yt-dlp Linux x86_64
│   └── ffmpeg-linux        # Binario ffmpeg Linux
├── scripts/
│   └── update_binaries.sh  # Descarga y verifica el yt-dlp más reciente
├── build/                  # Archivos temporales de construcción (generado por PyInstaller)
├── dist/                   # Ejecutables finales (generado por PyInstaller)
│   ├── Moncho_YT.exe       # Ejecutable Windows
│   ├── Moncho_YT           # Ejecutable Linux
│   └── Moncho_YT.app/      # Aplicación empaquetada (macOS)
├── docker/
│   └── docker-compose.yml  # Configuración Docker
├── venv/                   # Entorno virtual de Python
├── launcher.py             # Script lanzador (si aplica)
├── gui_moncholv.py         # Interfaz gráfica opcional (Tkinter)
├── Makefile                # Comandos automatizados
├── Moncho_YT_app.spec      # Configuración PyInstaller (macOS, terminal)
├── Moncho_YT.spec          # Configuración PyInstaller (macOS, GUI)
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

## Actualizar yt-dlp

YouTube cambia con frecuencia, así que un yt-dlp antiguo acaba devolviendo
`HTTP Error 403: Forbidden` o "Requested format is not available".

La app ya no intenta actualizar con `pip` (eso no funcionaba en los ejecutables):
descarga el binario oficial de la plataforma y lo guarda en una carpeta del
usuario, sin permisos de administrador:

| Plataforma | Carpeta del yt-dlp actualizado |
| --- | --- |
| macOS | `~/Library/Application Support/Moncho_YT/bin/yt-dlp` |
| Windows | `%LOCALAPPDATA%\Moncho_YT\bin\yt-dlp.exe` |
| Linux | `~/.local/share/Moncho_YT/bin/yt-dlp-linux` |

Se usa el binario de versión más alta (normalmente el actualizado, porque el
incluido en la app se queda atrás con el tiempo). Al arrancar se consulta la
última release y **solo se pregunta si hay una versión nueva**; si ya estás al
día (o no hay conexión), no aparece ninguna pregunta. Formas de actualizar:

```bash
# 1) Al arrancar solo pregunta si hay una versión nueva; responde "s" para instalarla
# 2) Sin preguntas:
python3 script_descarga.py --update
# 3) En el .app de macOS:
/Applications/Moncho_YT.app/Contents/MacOS/Moncho_YT --update
```

Para ver qué versión se está usando:

```bash
python3 script_descarga.py --version
```

Si actualizas los binarios del repositorio antes de compilar, usa:

```bash
./scripts/update_binaries.sh   # o: make binaries
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

### Opciones de línea de comandos

```bash
python3 script_descarga.py            # menú interactivo
python3 script_descarga.py --version  # versión de la app y de yt-dlp/ffmpeg
python3 script_descarga.py --update   # actualiza yt-dlp y sale
```

En macOS también funcionan dentro del bundle:

```bash
/Applications/Moncho_YT.app/Contents/MacOS/Moncho_YT --version
/Applications/Moncho_YT.app/Contents/MacOS/Moncho_YT --update
```

---

## Ejecutables precompilados

Si prefieres no instalar Python ni dependencias, puedes usar los ejecutables precompilados disponibles en [Releases](https://github.com/moncholv/script_descarga_audio-video/releases).

### **macOS (Intel y Apple Silicon/M1/M2/M3)**

1. Descarga `Moncho_YT-v1.1.1-macOS.zip` (o el `.zip` de la release) desde Releases
2. Descomprime y mueve `Moncho_YT.app` a tu carpeta **Aplicaciones**
3. **Primera ejecución** (macOS puede bloquearlo por seguridad):
   - **Opción A:** Ve a **Preferencias del Sistema** > **Privacidad y seguridad** > **"Abrir de todos modos"**
   - **Opción B:** Ejecuta en Terminal:
     ```bash
     xattr -cr /Applications/Moncho_YT.app
     open /Applications/Moncho_YT.app
     ```
4. Haz doble clic en `Moncho_YT.app` para ejecutar

**Nota:** El ejecutable incluye `yt-dlp` (2026.10.26) y `ffmpeg`, no necesitas instalar nada más. Solo pregunta cuando hay una versión nueva de yt-dlp; si quieres forzar la comprobación, ejecuta `... --update`. Se guarda en tu carpeta de usuario sin tocar la app.

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

#### **Instalación rápida (AppImage)**

1. **Descarga el AppImage** correspondiente desde [Releases](https://github.com/moncholv/script_descarga_audio-video/releases):
   - `Moncho_YT-x86_64.AppImage` (Compatible con todas las distribuciones)

2. **yt-dlp incluido:** el AppImage ya trae un `yt-dlp` (Linux x86_64). Si quieres
   usar el del sistema en su lugar, instala uno de estos métodos. La app usa el
   de versión más moderna entre el actualizado y el incluido (el del `PATH` solo
   como último recurso):

   **Opción A - Usando pip (Recomendado):**
```bash
pip install yt-dlp
```

o
```bash
python3 -m pip install -U yt-dlp
```

**Opción B - Descarga directa (Siempre actualizado):**
```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

**Opción C - Usando el gestor de paquetes de tu distribución:**

**Ubuntu/Debian:**
```bash
sudo add-apt-repository ppa:tomtomtom/yt-dlp
sudo apt update
sudo apt install yt-dlp
```

**Fedora:**
```bash
sudo dnf install yt-dlp
```

**Arch/Manjaro:**
```bash
sudo pacman -S yt-dlp
```

**Cualquier distro (usando Snap):**
```bash
sudo snap install yt-dlp
```

3. **Dale permisos de ejecución al AppImage:**
```bash
chmod +x Moncho_YT-x86_64.AppImage
```

4. **Ejecuta desde terminal:**
```bash
./Moncho_YT-x86_64.AppImage
```

**Nota importante:** El AppImage incluye `yt-dlp`, así que funciona sin instalar nada.
Aun así, conviene actualizarlo con `--update` cuando YouTube cambie; el binario
actualizado se guarda en `~/.local/share/Moncho_YT/bin/` y no requiere `sudo`.

**Opcional - FFmpeg:** Si experimentas problemas con la conversión de audio, también puedes instalar ffmpeg:

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
pip install -r requirements.txt pyinstaller
```

### Descargar binarios necesarios:

Los binarios de `yt-dlp` y `ffmpeg` deben estar en la carpeta `binaries/` antes de compilar.
La forma recomendada (descarga macOS + Linux + Windows y verifica SHA-256):

```bash
./scripts/update_binaries.sh   # o: make binaries
```

### **macOS:**

```bash
cp "$(which ffmpeg)" binaries/ffmpeg  # Si tienes ffmpeg instalado con Homebrew
```

**Compilar:**
```bash
source venv/bin/activate
pyinstaller --clean --noconfirm Moncho_YT_app.spec
# o simplemente: make build-app
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
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux -o binaries/yt-dlp-linux
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

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Incluyen una prueba de regresión para el antiguo bucle de actualización:
en un ejecutable PyInstaller, `sys.executable -m pip ...` relanzaba la app
entera y volvía a pedir la actualización.

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

Si usas el código fuente, instala yt-dlp en el entorno:
```bash
pip install -U yt-dlp
```
o
```bash
brew install yt-dlp
```

En los ejecutables precompilados el binario va incluido; si aparece este error,
la descarga o el empaquetado se corrompió: vuelve a descargar la app o ejecuta
`make build-app` desde el repositorio.

### Error: "ffmpeg no está disponible"
Instala ffmpeg en tu sistema según tu plataforma (ver sección de instalación arriba)

### Error HTTP 403: Forbidden (o "Requested format is not available")

Es el síntoma típico de un `yt-dlp` desactualizado: YouTube invalida las URLs
de descarga y devuelve 403. Actualiza el binario que usa la app:

```bash
# Desde el código fuente
python3 script_descarga.py --update

# En la app de macOS
/Applications/Moncho_YT.app/Contents/MacOS/Moncho_YT --update
```

También puedes responder `s` cuando la app detecte una versión nueva. El nuevo binario se
guarda en tu carpeta de usuario (ver [Actualizar yt-dlp](#actualizar-yt-dlp)),
así que no hace falta reinstalar la app ni usar `sudo`.

Si el error continúa:
- Comprueba la versión con `python3 script_descarga.py --version`.
- Para vídeos con restricción de edad o que piden iniciar sesión, exporta las
  cookies del navegador y añade `--cookies-from-browser chrome` (o `safari`,
  `firefox`) a la llamada de yt-dlp.
- Prueba otro vídeo para descartar que el problema sea solo de ese contenido.

### Linux AppImage: usar un yt-dlp del sistema (opcional)

El AppImage ya incluye `yt-dlp`. Si prefieres usar el del sistema (por ejemplo,
para compartirlo con otras herramientas), instálalo con uno de estos comandos;
la app lo usará solo si no hay uno actualizado por `--update` ni uno incluido:

**Forma rápida (pip):**
```bash
pip install yt-dlp
```

**Forma con permisos de administrador (wget):**
```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

**Ubuntu/Debian (con PPA):**
```bash
sudo add-apt-repository ppa:tomtomtom/yt-dlp
sudo apt update
sudo apt install yt-dlp
```

---

## Cambios principales en esta versión (1.1.1)

- **yt-dlp actualizado a 2026.10.26** (macOS universal, Linux x86_64 y Windows):
  soluciona el `HTTP Error 403: Forbidden` al descargar audio/vídeo.
- **Actualización real de yt-dlp**: la app descarga el binario oficial en la
  carpeta de datos del usuario y lo prefiere sobre el del bundle. Ya no usa
  `pip` (que no funcionaba en los ejecutables) y no necesita `sudo`.
- Nuevos comandos `--update` y `--version`.
- Al arrancar solo pregunta si hay una actualización nueva; si ya estás al día
  no interrumpe (la comprobación HEAD falla en silencio si no hay conexión).
- La versión de yt-dlp se lee de un fichero `binaries/yt-dlp.version`, así el
  arranque no tiene que ejecutar el binario onefile (~3 s) cada vez.
- Corregido el bucle al responder `s`: antes se relanzaba la app con `-m pip`
  (los argumentos se ignoraban) y volvía a preguntar; ahora descarga el binario
  oficial, lo valida y sigue con el menú. Hay pruebas de regresión en `tests/`.
- Eliminado el `--user-agent` fijo de Chrome 114 en las playlists y añadidos
  reintentos (`--retries`, `--fragment-retries`, `--extractor-retries`).
- Resolución de binarios unificada: se valida que cada yt-dlp/ffmpeg se ejecute y
  se usa el de versión más moderna entre el actualizado y el incluido.
- FFmpeg incluido se usa de verdad también al descargar (antes solo se detectaba).
- `DESTINO_DESCARGAS` funciona como carpeta por defecto (documentado y probado).
- GUI arreglada: sin `pytube` (dependencia inexistente y rota), usa `yt-dlp`
  para playlists y pasa la ruta de FFmpeg incluido.
- Specs de PyInstaller actualizados para PyInstaller 6 (sin `cipher`/`zipfiles`).
- Script `scripts/update_binaries.sh` + `make binaries` para actualizar los
  binarios del repositorio verificando sus sumas SHA-256.
- README y solución de problemas actualizados.

### Versiones anteriores

- Ahora solo usa yt-dlp (pytube eliminado)
- Flujos y lógica separados para playlist y elementos individuales
- Selección automática de carpeta estándar multiplataforma (Windows, MacOS, Linux)
- Ejecutables standalone para todas las plataformas con binarios incluidos

---

## Créditos

- 👤 **Autor original**: [Moncholv](https://github.com/moncholv)  
- 🤝 **Colaboraciones y mejoras**: [Eddevios (Edu)](https://github.com/eddevios) | [eddevios.com](https://eddevios.com)

---
