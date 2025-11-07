# Binarios necesarios para compilar ejecutables

Esta carpeta debe contener los binarios de `yt-dlp` y `ffmpeg` para cada plataforma antes de compilar los ejecutables con PyInstaller.

## macOS

yt-dlp
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o binaries/yt-dlp
chmod +x binaries/yt-dlp

ffmpeg (si tienes Homebrew)
cp $(which ffmpeg) binaries/ffmpeg


## Windows

Descarga manualmente:
- **yt-dlp.exe:** https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
- **ffmpeg.exe:** https://github.com/BtbN/FFmpeg-Builds/releases (busca `ffmpeg-master-latest-win64-gpl.zip`)

Colócalos en `binaries/yt-dlp.exe` y `binaries/ffmpeg.exe`

## Linux

yt-dlp
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o binaries/yt-dlp-linux
chmod +x binaries/yt-dlp-linux

ffmpeg (opción 1: desde sistema)
sudo apt install ffmpeg # Ubuntu/Debian
cp $(which ffmpeg) binaries/ffmpeg-linux

ffmpeg (opción 2: estático universal)
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
cp ffmpeg-*-amd64-static/ffmpeg binaries/ffmpeg-linux
chmod +x binaries/ffmpeg-linux


## Nota

**Los binarios NO se incluyen en el repositorio** por su gran tamaño (~100-200 MB). Deben descargarse manualmente antes de compilar.

Los ejecutables finales en [Releases](https://github.com/moncholv/script_descarga_audio-video/releases) **SÍ incluyen** estos binarios empaquetados.

