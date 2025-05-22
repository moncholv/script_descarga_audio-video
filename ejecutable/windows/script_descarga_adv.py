import shutil
import sys
import os
from pytube import Playlist
import yt_dlp


def asegurar_ffmpeg_en_path():
    if getattr(sys, 'frozen', False):
        ffmpeg_dir = sys._MEIPASS
    else:
        ffmpeg_dir = os.path.dirname(os.path.abspath(__file__))

    ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    if os.path.exists(ffmpeg_path):
        os.environ["PATH"] = f"{ffmpeg_dir};{os.environ['PATH']}"
    else:
        print("❌ ffmpeg.exe no encontrado.")


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


def elegir_calidad_video():
    print("\nElige la calidad del vídeo:")
    print("1. Alta (mejor calidad disponible)")
    print("2. Media")
    print("3. Baja (menor resolución disponible)")
    calidad = input("Introduce el número correspondiente (Enter para usar alta): ").strip()

    if calidad == "2":
        return "bestvideo[height<=720]+bestaudio[ext=mp4]"
    elif calidad == "3":
        return "bestvideo[height<=480]+bestaudio[ext=mp4]"
    else:
        return "bestvideo[ext=mp4]+bestaudio[ext=mp4]"  # por defecto


def elegir_subtitulos():
    subtitulos = input("\n¿Deseas descargar subtítulos? (s/n): ").strip().lower()
    if subtitulos == "s":
        langs = input("Introduce los códigos de idioma separados por coma (ej: en,es,fr): ").strip()
        idiomas = [lang.strip() for lang in langs.split(",") if lang.strip()]
        return {
            "writesubtitles": True,
            "subtitleslangs": idiomas,
            "subtitlesformat": "best"
        }
    return {}


def main():
    asegurar_ffmpeg_en_path()
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
            formato_video = elegir_calidad_video()
            subtitulo_opts = elegir_subtitulos()
            ydl_opts = {
                'format': formato_video,
                'outtmpl': plantilla_salida,
                'merge_output_format': 'mp4',
                **subtitulo_opts
            }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(yt_play)


if __name__ == "__main__":
    main()
