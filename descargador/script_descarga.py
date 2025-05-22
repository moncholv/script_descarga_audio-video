import shutil
import sys
import os
from pytube import Playlist
import yt_dlp


def verificar_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("⚠️  ADVERTENCIA: FFmpeg no está disponible en el PATH.")
        print("Es necesario para la conversión de audio a mp3.")
        print("Asegúrate de que ffmpeg esté instalado y en tu PATH.\n")


def mostrar_menu():
    print("---- moncholv video & audio download script ----")
    print("Selecciona una opción:")
    print("1. Descargar audio.")
    print("2. Descargar audios de lista de reproducción.")
    print("3. Descargar vídeo.")
    print("4. Descargar vídeos de lista de reproducción.")
    print()


def pedir_directorio_destino():
    destino = os.getenv("DESTINO_DESCARGAS")
    if destino:
        print(f"📁 Usando carpeta de destino desde variable de entorno: {destino}")
    else:
        destino = input("Introduce la carpeta de destino (o presiona Enter para usar la carpeta actual): ").strip()
        if destino == "":
            destino = os.getcwd()
    try:
        os.makedirs(destino, exist_ok=True)
        print(f"✅ Carpeta preparada: {destino}")
    except Exception as e:
        print(f"❌ Error creando la carpeta: {e}")
        sys.exit(1)
    return destino


def main():
    verificar_ffmpeg()
    mostrar_menu()

    opcion = input("Escribe el número de la opción y presiona Enter: ")
    is_playlist = opcion in {"2", "4"}

    print()
    url = input("Introduce la URL de la lista de reproducción:" if is_playlist else "Introduce la URL del vídeo: ")

    destino = pedir_directorio_destino()
    plantilla_salida = os.path.join(destino, '%(title)s.%(ext)s')

    match opcion:
        case "1" | "3":
            yt_play = url
        case "2" | "4":
            yt_play = Playlist(url)
        case _:
            print("Opción no reconocida")
            sys.exit(1)

    match opcion:
        case "1" | "2":
            ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'outtmpl': plantilla_salida,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'
                }]
            }
        case "3" | "4":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]',
                'outtmpl': plantilla_salida,
                'merge_output_format': 'mp4'
            }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(yt_play)


if __name__ == "__main__":
    main()
