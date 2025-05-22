# Si no quieres añadir al PATH de forma permanente la ruta, tendrás que hacer un export 
# a la ruta donde tengas el binario para poder ejecutar en cada sesión:
# export PATH=$PATH:/c/Users/moncholv/Documents/apps_portables/ffmpeg/bin

from pytube import Playlist
import yt_dlp


def mostrar_menu():
    print("---- moncholv video & audio download script ----")
    print("Selecciona una opción:")
    print("1. Descargar audio.")
    print("2. Descargar audios de lista de reproducción.")
    print("3. Descargar vídeo.")
    print("4. Descargar vídeos de lista de reproducción.")
    print()


def main():
    while True:
        mostrar_menu()
        opcion = input("Escribe el número de la opción y presiona Enter: ")

        is_playlist = opcion == "2" or opcion == "4"
        print()
        url = input("Introduzca la url de la lista de reproducción:" if is_playlist else "Introduzca la url del vídeo: ")

        match opcion:
            case "1" | "3":
                yt_play = url
            case "2" | "4":
                yt_play = Playlist(url)
            case _:
                print("Opción no reconocida")
                exit()

        match opcion:
            case "1" | "2":
                ydl_opts = {'format': 'mp3/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]}
            case "3" | "4":
                ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(yt_play)
        break


if __name__ == "__main__":
    main()
