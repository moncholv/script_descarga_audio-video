#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script universal para descargas de video/audio usando yt-dlp y ffmpeg.
Compatible con Windows, MacOS (Intel & Silicon/M1-M2) y Linux (Debian, Ubuntu, Arch).
- Autor: Moncholv 
- Colaborador: Eddevios
"""

import os
import sys
import platform
import subprocess
from shutil import which

# Variables globales para las rutas de binarios
YT_DLP_BIN = None
FFMPEG_BIN = None

# =============== FUNCIONES UTILITARIAS ===============

def get_ytdlp_path():
    """Busca yt-dlp: primero en la carpeta del ejecutable, luego en PATH"""
    if getattr(sys, 'frozen', False):
        # Ejecutable empaquetado con PyInstaller
        bundle_dir = sys._MEIPASS
        local_ytdlp = os.path.join(bundle_dir, 'yt-dlp')
        if os.path.exists(local_ytdlp):
            return local_ytdlp
    # Busca en PATH del sistema
    return which("yt-dlp")

def get_bundled_binary(name):
    """
    Devuelve la ruta del binario incluido en el bundle.
    Si no está empaquetado, usa el del sistema.
    """
    if getattr(sys, 'frozen', False):
        # Ejecutable empaquetado por PyInstaller
        base_path = sys._MEIPASS
    else:
        # Ejecución normal desde código fuente
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Determina el sufijo según la plataforma
    if platform.system() == "Windows":
        binary_name = f"{name}.exe"
    elif platform.system() == "Linux":
        binary_name = f"{name}-linux" if name in ["yt-dlp", "ffmpeg"] else name
    else:
        binary_name = name  # macOS
    
    binary_path = os.path.join(base_path, 'binaries', binary_name)
    
    # Si existe el binario incluido, úsalo
    if os.path.exists(binary_path):
        return binary_path
    
    # Fallback: usar el del sistema (si existe)
    system_binary = which(name)
    if system_binary:
        return system_binary
    
    return None

def check_dependencies():
    """Verifica que yt-dlp y ffmpeg estén disponibles y configura las rutas globales."""
    global YT_DLP_BIN, FFMPEG_BIN
    
    YT_DLP_BIN = get_ytdlp_path()
    FFMPEG_BIN = which("ffmpeg")
    
    if not YT_DLP_BIN:
        print("ERROR: 'yt-dlp' no está disponible.")
        print("Instálalo con: pip install yt-dlp  o  brew install yt-dlp (Mac)")
        sys.exit(1)
    if not FFMPEG_BIN:
        print("ERROR: 'ffmpeg' no está en el PATH del sistema.")
        print("Instálalo según tu sistema (brew install ffmpeg, apt install ffmpeg, etc.)")
        sys.exit(1)
    
    print(f"✓ Usando yt-dlp: {YT_DLP_BIN}")
    print(f"✓ Usando ffmpeg: {FFMPEG_BIN}")

def check_update():
    """
    Pregunta si se desean actualizar las librerías yt-dlp y ffmpeg (manual).
    """
    r = input("\n¿Deseas comprobar y actualizar yt-dlp? (s/n): ").strip().lower()
    if r == 's':
        subprocess.call([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'])
        print("Para ffmpeg, si es necesario, actualízalo manualmente según tu sistema.")

def print_platform_info():
    """
    Muestra información sobre el sistema operativo en uso.
    """
    plat_name = platform.system()
    print(f"\n---- Plataforma detectada: {plat_name} ({platform.machine()}) ----")

def get_default_download_dir():
    """
    Devuelve la carpeta de descargas por defecto según el sistema operativo.
    """
    if platform.system() == "Windows":
        # Intenta obtener la carpeta Descargas estándar en Windows
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                return winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
        except Exception:
            return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        # Para Mac y Linux busca 'Descargas' en español si existe
        ruta_es = os.path.join(os.path.expanduser("~"), "Descargas")
        if os.path.exists(ruta_es):
            return ruta_es
        return os.path.join(os.path.expanduser("~"), "Downloads")

def choose_download_folder(default_dir):
    """
    Pregunta por carpeta de destino o usa la de por defecto.
    """
    print(f"\nCarpeta por defecto de descargas: {default_dir}")
    r = input("¿Quieres descargar en otra carpeta? Ruta (en blanco para usar por defecto): ").strip()
    if r:
        if not os.path.exists(r):
            os.makedirs(r)  # Crea la carpeta si no existe
        return r
    return default_dir

def mostrar_menu():
    """
    Print el menú y devuelve la opción elegida.
    """
    print("\n---- Moncholv video & audio download script ----")
    print("Selecciona una opción:")
    print("1. Descargar video rápido (menor calidad)")
    print("2. Descargar vídeo (elegir calidad)")
    print("3. Descargar vídeos de lista de reproducción")
    print("4. Descargar audio")
    print("5. Descargar audios de lista de reproducción")
    return input("Escribe el número de la opción y presiona Enter: ").strip()

def pedir_url():
    """Pide al usuario una URL de YouTube (video o lista)."""
    return input("\nIntroduce la URL de YouTube (video o playlist): ").strip()

def es_playlist(url):
    """
    Detecta si una URL de YouTube es una playlist.
    """
    return 'list=' in url or ('/playlist?' in url)

# =============== LÓGICA DE DESCARGA ===============

def descargar_video_rapido(url, destino):
    cmd = [
        YT_DLP_BIN,
        "--format", "mp4[height<=480]/best[height<=480]/best",
        "--no-playlist",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        url
    ]
    subprocess.run(cmd)

def descargar_video_calidad(url, destino):
    print("\n[Descarga de video personalizada]")
    if es_playlist(url):
        print("ERROR: La descarga de vídeo personalizada solo es aplicable a un video, no a playlists.")
        return
    consulta_cmd = [YT_DLP_BIN, "-F", url]
    subprocess.run(consulta_cmd)
    formato = input("Introduce el código del formato deseado (Ejemplo: 137+140): ").strip()
    cmd = [
        YT_DLP_BIN,
        "-f", formato,
        "--no-playlist",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        url
    ]
    subprocess.run(cmd)

def descargar_videos_playlist(url, destino):
    print("\n[Descargar videos de playlist (calidad rápida)]")
    if not es_playlist(url):
        print("La URL proporcionada NO es una playlist.")
        return
    cmd = [
        YT_DLP_BIN,
        "--format", "mp4[height<=480]/best[height<=480]/best",
        "--yes-playlist",
        "--output", os.path.join(destino, "%(playlist)s/%(title)s.%(ext)s"),
        url
    ]
    subprocess.run(cmd)

def descargar_audio(url, destino):
    print("\n[Descarga de audio (solo un video)]")
    if es_playlist(url):
        print("ERROR: La descarga de audio individual solo es aplicable a un video, no a playlists.")
        return
    cmd = [
        YT_DLP_BIN,
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        "--no-playlist",
        url
    ]
    subprocess.run(cmd)

def descargar_audios_playlist(url, destino):
    print("\n[Descargar audios de playlist]")
    if not es_playlist(url):
        print("La URL proporcionada NO es una playlist.")
        return
    cmd = [
        YT_DLP_BIN,
        "--extract-audio",
        "--audio-format", "mp3",
        "--yes-playlist",
        "--output", os.path.join(destino, "%(playlist)s/%(title)s.%(ext)s"),
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        url
    ]
    subprocess.run(cmd)


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    # Si se ejecuta desde una .app en macOS, abre Terminal
    if getattr(sys, 'frozen', False) and platform.system() == "Darwin":
        # Verifica si ya estamos en Terminal
        if not os.environ.get('TERM'):
            # No estamos en terminal, ábrela
            script_path = sys.executable
            cmd = f'''
            tell application "Terminal"
                do script "{script_path}"
                activate
            end tell
            '''
            subprocess.run(['osascript', '-e', cmd])
            sys.exit(0)
    
    # Flujo normal
    print_platform_info()
    check_dependencies()
    check_update()
    default_dir = get_default_download_dir()
    download_folder = choose_download_folder(default_dir)
    opcion = mostrar_menu()
    url = pedir_url()

    if opcion == "1":
        descargar_video_rapido(url, download_folder)
    elif opcion == "2":
        descargar_video_calidad(url, download_folder)
    elif opcion == "3":
        descargar_videos_playlist(url, download_folder)
    elif opcion == "4":
        descargar_audio(url, download_folder)
    elif opcion == "5":
        descargar_audios_playlist(url, download_folder)
    else:
        print("Opción no reconocida. Saliendo.")

    print("\n¡Proceso finalizado!")
