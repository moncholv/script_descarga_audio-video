# Binarios necesarios para compilar ejecutables

Esta carpeta contiene los binarios de `yt-dlp` y `ffmpeg` para cada plataforma
que se empaquetan con PyInstaller.

## Actualizar yt-dlp (recomendado)

No los descargues a mano: usa el script, que baja la última release oficial de
macOS, Linux y Windows y verifica las sumas SHA-256.

```bash
./scripts/update_binaries.sh            # última versión
./scripts/update_binaries.sh 2026.10.26 # una versión concreta
```

Versión incluida actualmente: **yt-dlp 2026.10.26**.

Junto a cada binario hay un fichero `.version` (por ejemplo
`yt-dlp.version`) con la versión y el tamaño. La app lo usa para conocer la
versión sin ejecutar el binario en cada arranque. El script los genera; si
descargas un yt-dlp a mano, actualízalos también (primera línea: versión).

Después de actualizar hay que recompilar la app (`make build-app`) para que el
nuevo binario y su `.version` queden dentro del bundle.

## macOS

```bash
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o binaries/yt-dlp
chmod +x binaries/yt-dlp

# ffmpeg (si tienes Homebrew)
cp "$(which ffmpeg)" binaries/ffmpeg
```

`binaries/yt-dlp` es un binario universal (x86_64 + arm64).

## Windows

- **yt-dlp.exe:** https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
- **ffmpeg.exe:** https://github.com/BtbN/FFmpeg-Builds/releases (busca `ffmpeg-master-latest-win64-gpl.zip`)

Colócalos en `binaries/yt-dlp.exe` y `binaries/ffmpeg.exe`.

## Linux

```bash
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux -o binaries/yt-dlp-linux
chmod +x binaries/yt-dlp-linux

# ffmpeg (opción 1: desde el sistema)
sudo apt install ffmpeg
cp "$(which ffmpeg)" binaries/ffmpeg-linux

# ffmpeg (opción 2: estático universal)
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
cp ffmpeg-*-amd64-static/ffmpeg binaries/ffmpeg-linux
chmod +x binaries/ffmpeg-linux
```

## Nota

Los binarios sí se guardan en el repositorio (unos 100 MB) para que las
releases sean reproducibles. Aun así, conviene ejecutar
`./scripts/update_binaries.sh` antes de cada release porque YouTube cambia a
menudo y un yt-dlp antiguo provoca errores `HTTP Error 403: Forbidden`.

La app, además, puede actualizar su propio yt-dlp a la carpeta de datos del
usuario sin permisos de administrador (opción `s` al arrancar o `--update`).
