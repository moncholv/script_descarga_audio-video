import shutil
import sys
import os
import yt_dlp


def verificar_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("⚠️  ADVERTENCIA: FFmpeg no está disponible en el PATH.")
        print("Es necesario para la combinación y conversión de audio/video.")
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
        default_downloads_folder = ""
        if sys.platform == "win32":
            import winreg
            try:
                sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    default_downloads_folder = winreg.QueryValueEx(
                        key, "{374DE290-123F-4565-9164-39C4925E467B}"
                    )[0]
            except Exception:
                default_downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                if not os.path.exists(default_downloads_folder):
                    default_downloads_folder = os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # macOS/Linux
            default_downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(default_downloads_folder):
                default_downloads_folder = os.path.join(os.path.expanduser("~"), "Desktop")

        destino = input(
            f"Introduce la carpeta de destino (o presiona Enter para usar '{default_downloads_folder}'): "
        ).strip() or default_downloads_folder

    try:
        os.makedirs(destino, exist_ok=True)
        print(f"✅ Carpeta preparada: {destino}")
    except Exception as e:
        print(f"❌ Error creando la carpeta: {e}")
        sys.exit(1)
    return destino


def elegir_calidad(url):
    print("\n🔍 Obteniendo calidades disponibles...")
    ydl_opts = {}
    calidades = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            for f in formats:
                if f.get("vcodec") != "none":
                    calidades.append({
                        "itag": f.get("format_id"),
                        "ext": f.get("ext"),
                        "resolucion": f.get("height") or "N/A",
                        "fps": f.get("fps") or "N/A",
                        "tamanio": f.get("filesize"),
                        "nota": f.get("format_note") or "",
                        "acodec": f.get("acodec"),
                    })

        if not calidades:
            print("⚠️ No se encontraron formatos de vídeo disponibles.")
            return "best"

        print("\n📺 Calidades disponibles:")
        for i, c in enumerate(calidades, 1):
            size_str = f"{c['tamanio']/1024/1024:.1f} MB" if c["tamanio"] else "desconocido"
            audio_str = "audio" if c["acodec"] != "none" else "sin audio"
            print(f"{i}. {c['resolucion']}p {c['fps']}fps - {c['nota']} ({size_str}) [{c['ext']}] [{audio_str}] [itag={c['itag']}]")

        seleccion = input("Elige la calidad (número) o Enter para la mejor: ").strip()
        if seleccion and seleccion.isdigit() and 1 <= int(seleccion) <= len(calidades):
            return calidades[int(seleccion) - 1]["itag"]
        else:
            return "best"

    except Exception as e:
        print(f"❌ Error obteniendo calidades: {e}")
        return "best"


def main():
    verificar_ffmpeg()
    mostrar_menu()

    opcion = input("Escribe el número de la opción y presiona Enter: ")
    is_playlist = opcion in {"2", "4"}

    print()
    url = input("Introduce la URL de la lista de reproducción:" if is_playlist else "Introduce la URL del vídeo: ")

    destino = pedir_directorio_destino()
    plantilla_salida = os.path.join(destino, "%(title)s.%(ext)s")

    if opcion in {"1", "2"}:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": plantilla_salida,
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
            ],
            "restrictfilenames": True
        }
    elif opcion in {"3", "4"}:
        video_itag = elegir_calidad(url)
        # Descargar el vídeo seleccionado + mejor audio m4a, y combinar en mp4
        ydl_opts = {
            "format": f"{video_itag}+bestaudio[ext=m4a]/best",
            "outtmpl": plantilla_salida,
            "merge_output_format": "mp4",
            "restrictfilenames": True
        }
    else:
        print("Opción no reconocida")
        sys.exit(1)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([url])
        if error_code != 0:
            print("⚠️ Descarga completada con errores")
    except Exception as e:
        print(f"❌ Error durante la descarga: {e}")

    input("\n✅ Proceso terminado. Pulsa Enter para salir...")


if __name__ == "__main__":
    main()
