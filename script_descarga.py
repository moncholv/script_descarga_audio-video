#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script universal para descargas de video/audio usando yt-dlp y ffmpeg.
Compatible con Windows, MacOS (Intel & Silicon/M1-M2) y Linux (Debian, Ubuntu, Arch).
- Autor: Moncholv
- Colaborador: Eddevios
"""

import os
import platform
import shlex
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from shutil import which

APP_NAME = "Moncho_YT"
APP_VERSION = "1.1.1"
YTDLP_RELEASES_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download"

# Variables globales para las rutas de binarios
YT_DLP_BIN = None
FFMPEG_BIN = None

# Caché de versiones ya consultadas (evita ejecutar `--version` varias veces)
_VERSION_CACHE = {}

# =============== UTILIDADES DE PLATAFORMA ===============


def es_windows():
    return platform.system() == "Windows"


def es_linux():
    return platform.system() == "Linux"


def es_macos():
    return platform.system() == "Darwin"


def nombre_binario(name):
    """Devuelve el nombre del binario empaquetado según la plataforma."""
    if es_windows():
        return "{}.exe".format(name)
    if es_linux():
        return "{}-linux".format(name)
    return name


def get_app_data_dir():
    """Carpeta de datos del usuario, escribible aunque la app esté en /Applications."""
    home = os.path.expanduser("~")
    if es_windows():
        base = os.environ.get("LOCALAPPDATA") or os.path.join(home, "AppData", "Local")
        return os.path.join(base, APP_NAME)
    if es_macos():
        return os.path.join(home, "Library", "Application Support", APP_NAME)
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    return os.path.join(base, APP_NAME)


def get_managed_bin_dir():
    """Carpeta donde se guardan los yt-dlp actualizados (sin tocar el bundle)."""
    return os.path.join(get_app_data_dir(), "bin")


def get_bundle_base():
    """Raíz de recursos: _MEIPASS si está empaquetado, si no la carpeta del script."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_bundled_binary(name):
    """Ruta del binario incluido en binaries/ (o None si no existe)."""
    ruta = os.path.join(get_bundle_base(), "binaries", nombre_binario(name))
    if os.path.isfile(ruta):
        return ruta
    return None


def _ruta_sidecar(binario):
    return binario + ".version"


def _leer_version_conocida(binario):
    """Lee `<binario>.version` sin ejecutar el binario.

    La segunda línea (tamaño) es informativa: PyInstaller adelgaza el binario
    universal al empaquetarlo, así que no sirve para validar el del bundle.
    """
    ruta = _ruta_sidecar(binario)
    try:
        if not os.path.isfile(ruta):
            return None
        with open(ruta, "r", encoding="utf-8") as archivo:
            version = archivo.readline().strip()
        return version or None
    except OSError:
        return None


def _guardar_version_conocida(binario, version):
    try:
        with open(_ruta_sidecar(binario), "w", encoding="utf-8") as archivo:
            archivo.write("{}\n{}\n".format(version, os.path.getsize(binario)))
    except OSError:
        pass


def _version_de(binario, flag="--version"):
    """Devuelve la versión del binario, o None si no se puede ejecutar.

    Para yt-dlp se apoya en el fichero `<binario>.version` que generan el build
    y el actualizador: así no hay que lanzar el binario (que tarda ~3 s porque
    es un onefile de PyInstaller) en cada arranque.
    """
    if not binario:
        return None
    clave = (binario, flag)
    if clave in _VERSION_CACHE:
        return _VERSION_CACHE[clave]
    version = _leer_version_conocida(binario) if flag == "--version" else None
    if version is None:
        try:
            proc = subprocess.run(
                [binario, flag],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=30,
                universal_newlines=True,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                version = proc.stdout.strip().splitlines()[0].strip()
        except (OSError, subprocess.SubprocessError, ValueError):
            version = None
        if version and flag == "--version":
            # Solo escribimos junto a los binarios que gestiona la app.
            if os.path.dirname(os.path.abspath(binario)) == get_managed_bin_dir():
                _guardar_version_conocida(binario, version)
    _VERSION_CACHE[clave] = version
    return version


# =============== RESOLUCIÓN DE BINARIOS ===============


def _version_key(version):
    """Convierte '2026.10.26' en (2026, 10, 26) para comparar versiones."""
    partes = []
    for parte in version.split(".")[:3]:
        if not parte.isdigit():
            break
        partes.append(int(parte))
    return tuple(partes)


def hay_actualizacion(actual, remota):
    """Devuelve True solo si `remota` es más nueva que `actual`."""
    if not actual or not remota or actual == remota:
        return False
    clave_actual = _version_key(actual)
    clave_remota = _version_key(remota)
    if clave_actual and clave_remota:
        return clave_remota > clave_actual
    # Versiones no numéricas (nightly, builds raras): comparación literal
    return remota != actual


def get_ytdlp_path():
    """
    Elige el yt-dlp que debe usar la app:
    1. Versión actualizada por la propia app (carpeta de datos del usuario).
    2. Binario incluido en el bundle.
    3. yt-dlp del PATH del sistema, solo si ninguno de los anteriores arranca.

    Si hay varios candidatos de la app válidos se usa el de versión más alta
    (y, a igualdad, el actualizado), de modo que una actualización del bundle
    no queda tapada por una copia antigua del usuario. Las versiones se leen de
    los ficheros `.version` para no lanzar el onefile de yt-dlp en cada arranque.
    """
    candidatos = []

    actualizado = os.path.join(get_managed_bin_dir(), nombre_binario("yt-dlp"))
    if os.path.isfile(actualizado):
        candidatos.append(actualizado)

    incluido = find_bundled_binary("yt-dlp")
    if incluido:
        candidatos.append(incluido)

    validos = []
    for indice, candidato in enumerate(candidatos):
        version = _version_de(candidato)
        if version:
            # A igual versión, gana el candidato con menor índice (el actualizado).
            validos.append((_version_key(version), -indice, candidato))

    if validos:
        return max(validos)[2]

    # Fallback: yt-dlp del sistema (se ejecuta solo si los de la app fallan)
    del_sistema = which("yt-dlp")
    if del_sistema:
        if _version_de(del_sistema):
            return del_sistema
        candidatos.append(del_sistema)

    # Ninguno respondió: devolvemos el primero existente para poder informar
    return candidatos[0] if candidatos else None


def get_ffmpeg_path():
    """ffmpeg incluido en el bundle o, si no, el del PATH.

    Se comprueba que arranque de verdad (`-version`): así un ffmpeg empaquetado
    sin sus DLLs/dylibs no se usa y se puede caer al del sistema.
    """
    candidatos = []
    incluido = find_bundled_binary("ffmpeg")
    if incluido:
        candidatos.append(incluido)
    del_sistema = which("ffmpeg")
    if del_sistema:
        candidatos.append(del_sistema)
    for candidato in candidatos:
        if _version_de(candidato, "-version"):
            return candidato
    return candidatos[0] if candidatos else None


def get_ytdlp_version(binario=None):
    return _version_de(binario or YT_DLP_BIN)


def check_dependencies(require_ytdlp=True, require_ffmpeg=True):
    """Configura YT_DLP_BIN y FFMPEG_BIN y muestra información útil."""
    global YT_DLP_BIN, FFMPEG_BIN

    YT_DLP_BIN = get_ytdlp_path()
    FFMPEG_BIN = get_ffmpeg_path()

    if require_ytdlp and not YT_DLP_BIN:
        print("ERROR: 'yt-dlp' no está disponible.")
        print("La app incluye su propio yt-dlp. Si falta, instálalo con:")
        print("  pip install yt-dlp  |  brew install yt-dlp (macOS)")
        sys.exit(1)

    if require_ffmpeg and not FFMPEG_BIN:
        print("ERROR: 'ffmpeg' no está disponible.")
        print("Instálalo según tu sistema (brew install ffmpeg, apt install ffmpeg, etc.)")
        sys.exit(1)

    if YT_DLP_BIN:
        version = get_ytdlp_version(YT_DLP_BIN) or "versión desconocida"
        print("✓ Usando yt-dlp: {} ({})".format(YT_DLP_BIN, version))
    if FFMPEG_BIN:
        print("✓ Usando ffmpeg: {}".format(FFMPEG_BIN))


# =============== ACTUALIZACIÓN REAL DE YT-DLP ===============


def _ssl_context():
    try:
        import certifi  # PyInstaller lo incluye si está instalado
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def _asset_ytdlp():
    """Nombre del asset oficial que corresponde a esta plataforma/arquitectura."""
    if es_macos():
        return "yt-dlp_macos"
    if es_windows():
        return "yt-dlp.exe"
    if es_linux():
        maquina = platform.machine().lower()
        if maquina in ("x86_64", "amd64"):
            return "yt-dlp_linux"
        if maquina in ("aarch64", "arm64"):
            return "yt-dlp_linux_aarch64"
        if maquina.startswith("armv7") or maquina.startswith("armv6"):
            return "yt-dlp_linux_armv7l"
        # Fallback: zipapp oficial (necesita python3 en el sistema)
        return "yt-dlp"
    return "yt-dlp"


def _descargar(url, destino, timeout=120):
    """Descarga url en destino (con .part) mostrando progreso básico."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    parcial = destino + ".part"
    peticion = urllib.request.Request(
        url,
        headers={"User-Agent": "{}/{}".format(APP_NAME, APP_VERSION)},
    )
    try:
        with urllib.request.urlopen(
            peticion, timeout=timeout, context=_ssl_context()
        ) as respuesta, open(parcial, "wb") as salida:
            total = int(respuesta.headers.get("Content-Length") or 0)
            leido = 0
            ultimo_bloque = -1
            while True:
                bloque = respuesta.read(256 * 1024)
                if not bloque:
                    break
                salida.write(bloque)
                leido += len(bloque)
                if total:
                    porcentaje = int(leido * 100 / total)
                    if porcentaje // 10 != ultimo_bloque:
                        ultimo_bloque = porcentaje // 10
                        print(
                            "  ... {}% ({:.1f} MB / {:.1f} MB)".format(
                                porcentaje, leido / 1048576.0, total / 1048576.0
                            ),
                            end="\r",
                            flush=True,
                        )
        os.replace(parcial, destino)
        print()
    finally:
        if os.path.exists(parcial):
            try:
                os.remove(parcial)
            except OSError:
                pass


def _ultima_version_remota(timeout=20):
    """Consulta la última release con una petición HEAD (sin descargar el binario)."""
    peticion = urllib.request.Request(
        "https://github.com/yt-dlp/yt-dlp/releases/latest",
        headers={"User-Agent": "{}/{}".format(APP_NAME, APP_VERSION)},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(
            peticion, timeout=timeout, context=_ssl_context()
        ) as respuesta:
            url_final = respuesta.geturl()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None
    if "/tag/" not in url_final:
        return None
    return url_final.rstrip("/").rsplit("/", 1)[-1] or None


def update_ytdlp(version_remota=None):
    """
    Descarga la última versión oficial de yt-dlp en la carpeta de datos del
    usuario y la deja como preferente. No modifica el bundle (así funciona
    aunque la app esté en /Applications y no requiera permisos de admin).

    `version_remota` permite reutilizar la comprobación hecha por
    `check_update` y no consultar GitHub dos veces.
    """
    global YT_DLP_BIN

    actual = get_ytdlp_version(YT_DLP_BIN or get_ytdlp_path())
    print("\n[Actualización] yt-dlp actual: {}".format(actual or "desconocida"))

    remota = version_remota or _ultima_version_remota()
    if remota and actual and actual == remota:
        print("✓ Ya tienes la última versión de yt-dlp ({}).".format(actual))
        return True

    asset = _asset_ytdlp()
    url = "{}/{}".format(YTDLP_RELEASES_URL, asset)
    destino = os.path.join(get_managed_bin_dir(), nombre_binario("yt-dlp"))
    temporal = destino + ".nuevo"

    print("[Actualización] Descargando la última versión ({})...".format(asset))
    print("[Actualización] Destino: {}".format(destino))
    try:
        _descargar(url, temporal)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as error:
        print("\n✗ No se pudo descargar la actualización: {}".format(error))
        print("  Comprueba tu conexión a Internet y vuelve a intentarlo.")
        return False

    if not es_windows():
        try:
            os.chmod(temporal, 0o755)
        except OSError as error:
            print("⚠️ No se pudo dar permiso de ejecución: {}".format(error))

    # Validar antes de sustituir: si la descarga está corrupta, se conserva
    # el yt-dlp que ya funcionaba.
    nueva = get_ytdlp_version(temporal)
    if not nueva:
        print("\n✗ El archivo descargado no funciona en este equipo.")
        print("  Se conserva el yt-dlp anterior.")
        try:
            os.remove(temporal)
        except OSError:
            pass
        return False

    if actual and actual == nueva:
        print("✓ Ya tienes la última versión de yt-dlp ({}).".format(nueva))
        try:
            os.remove(temporal)
        except OSError:
            pass
        return True

    os.replace(temporal, destino)
    _guardar_version_conocida(destino, nueva)
    YT_DLP_BIN = destino
    print("✓ yt-dlp actualizado a {}.".format(nueva))
    print("  Se usará automáticamente en las próximas ejecuciones.")
    return True


def check_update():
    """Comprueba si hay una versión nueva y solo entonces pregunta.

    Se consulta la última release con una petición HEAD ligera. Si ya está al
    día, si no hay conexión o si la comprobación falla, no se pregunta nada y
    el arranque sigue normalmente.

    No se debe ejecutar `[sys.executable, "-m", "pip", ...]`: en un ejecutable
    PyInstaller `sys.executable` es la propia app, que ignora los argumentos y
    se relanza a sí misma. Eso era lo que hacía que al responder "s" no se
    actualizara nada y volviera a aparecer la misma pregunta en bucle.
    """
    actual = get_ytdlp_version(YT_DLP_BIN or get_ytdlp_path())
    remota = _ultima_version_remota(timeout=5)
    if not hay_actualizacion(actual, remota):
        return

    print(
        "\nHay una nueva versión de yt-dlp disponible: {} → {}".format(
            actual or "desconocida", remota
        )
    )
    try:
        respuesta = input("¿Actualizar ahora? (s/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    if respuesta == "s":
        update_ytdlp(version_remota=remota)
        print("\nPara ffmpeg, si es necesario, actualízalo manualmente según tu sistema.")


# =============== UTILIDADES GENERALES ===============


def print_platform_info():
    print(
        "\n---- {} {} | Plataforma detectada: {} ({}) ----".format(
            APP_NAME, APP_VERSION, platform.system(), platform.machine()
        )
    )


def get_default_download_dir():
    """Carpeta de descargas por defecto según el sistema operativo."""
    # Permite personalizarla sin tocar el código (Docker/scripts)
    personalizada = os.environ.get("DESTINO_DESCARGAS")
    if personalizada:
        personalizada = os.path.expanduser(personalizada)
        try:
            os.makedirs(personalizada, exist_ok=True)
        except OSError:
            pass
        return personalizada

    if es_windows():
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            ) as key:
                return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        except Exception:
            return os.path.join(os.path.expanduser("~"), "Downloads")
    # Para Mac y Linux busca 'Descargas' en español si existe
    ruta_es = os.path.join(os.path.expanduser("~"), "Descargas")
    if os.path.exists(ruta_es):
        return ruta_es
    return os.path.join(os.path.expanduser("~"), "Downloads")


def choose_download_folder(default_dir):
    """Pregunta por carpeta de destino o usa la de por defecto."""
    print("\nCarpeta por defecto de descargas: {}".format(default_dir))
    try:
        ruta = input(
            "¿Quieres descargar en otra carpeta? Ruta (en blanco para usar por defecto): "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        return default_dir
    if not ruta:
        return default_dir
    ruta = os.path.expanduser(ruta)
    try:
        os.makedirs(ruta, exist_ok=True)
    except OSError as error:
        print("⚠️ No se pudo crear la carpeta ({}). Se usará la de por defecto.".format(error))
        return default_dir
    return ruta


def mostrar_menu():
    """Muestra el menú y devuelve la opción elegida."""
    print("\n---- Moncholv video & audio download script ----")
    print("Selecciona una opción:")
    print("1. Descargar video rápido (menor calidad)")
    print("2. Descargar vídeo (elegir calidad)")
    print("3. Descargar vídeos de lista de reproducción")
    print("4. Descargar audio")
    print("5. Descargar audios de lista de reproducción")
    try:
        return input("Escribe el número de la opción y presiona Enter: ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def pedir_url():
    """Pide al usuario una URL de YouTube (video o lista)."""
    try:
        return input("\nIntroduce la URL de YouTube (video o playlist): ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def es_playlist(url):
    """Detecta si una URL de YouTube es una playlist."""
    return "list=" in url or "/playlist?" in url


# =============== LÓGICA DE DESCARGA ===============

# --ignore-config: no depender de configuraciones locales del usuario.
# --no-update: evita que yt-dlp intente autoactualizarse desde dentro del bundle.
# Reintentos: YouTube devuelve 403/errores temporales con frecuencia.
OPCIONES_BASE = [
    "--ignore-config",
    "--no-update",
    "--retries", "10",
    "--fragment-retries", "10",
    "--extractor-retries", "3",
]

FORMATO_VIDEO_RAPIDO = "b[height<=480]/b"


def _ejecutar_ytdlp(argumentos):
    """Ejecuta yt-dlp y devuelve el código de salida, con ayuda ante errores."""
    if not YT_DLP_BIN:
        print("ERROR: yt-dlp no está disponible.")
        return 1
    comando = [YT_DLP_BIN] + OPCIONES_BASE
    # Sin esto, yt-dlp usa el ffmpeg del PATH aunque mostremos el incluido.
    if FFMPEG_BIN:
        comando += ["--ffmpeg-location", FFMPEG_BIN]
    comando += argumentos
    print("\n$ " + " ".join(shlex.quote(parte) for parte in comando))
    try:
        resultado = subprocess.run(comando)
    except OSError as error:
        print("ERROR: no se pudo ejecutar yt-dlp: {}".format(error))
        return 1
    if resultado.returncode != 0:
        print("\n✗ yt-dlp terminó con errores (código {}).".format(resultado.returncode))
        print("  • Un error 'HTTP Error 403: Forbidden' suele significar que yt-dlp")
        print("    está desactualizado. Reinicia la app y responde 's' a la pregunta")
        print("    de actualización (o ejecuta: {} --update).".format(APP_NAME))
        print("  • Si el vídeo pide iniciar sesión o tiene restricción de edad,")
        print("    exporta las cookies del navegador y usa --cookies-from-browser.")
        print("  • Para más detalles ejecuta yt-dlp manualmente con -v.")
    return resultado.returncode


def descargar_video_rapido(url, destino):
    _ejecutar_ytdlp([
        "--format", FORMATO_VIDEO_RAPIDO,
        "--no-playlist",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        url,
    ])


def descargar_video_calidad(url, destino):
    print("\n[Descarga de video personalizada]")
    if es_playlist(url):
        print("ERROR: La descarga de vídeo personalizada solo es aplicable a un video, no a playlists.")
        return
    _ejecutar_ytdlp(["-F", "--no-playlist", url])
    try:
        formato = input("Introduce el código del formato deseado (Ejemplo: 137+140): ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not formato:
        print("No se indicó ningún formato. Cancelado.")
        return
    _ejecutar_ytdlp([
        "-f", formato,
        "--no-playlist",
        "--merge-output-format", "mp4",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        url,
    ])


def descargar_videos_playlist(url, destino):
    print("\n[Descargar videos de playlist (calidad rápida)]")
    if not es_playlist(url):
        print("La URL proporcionada NO es una playlist.")
        return
    _ejecutar_ytdlp([
        "--format", FORMATO_VIDEO_RAPIDO,
        "--yes-playlist",
        "--output", os.path.join(destino, "%(playlist)s/%(title)s.%(ext)s"),
        url,
    ])


def descargar_audio(url, destino):
    print("\n[Descarga de audio (solo un video)]")
    if es_playlist(url):
        print("ERROR: La descarga de audio individual solo es aplicable a un video, no a playlists.")
        return
    _ejecutar_ytdlp([
        "--format", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--no-playlist",
        "--output", os.path.join(destino, "%(title)s.%(ext)s"),
        url,
    ])


def descargar_audios_playlist(url, destino):
    print("\n[Descargar audios de playlist]")
    if not es_playlist(url):
        print("La URL proporcionada NO es una playlist.")
        return
    _ejecutar_ytdlp([
        "--format", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--yes-playlist",
        "--output", os.path.join(destino, "%(playlist)s/%(title)s.%(ext)s"),
        url,
    ])


# ============================================
# MAIN
# ============================================


def _mostrar_version():
    print("{} {}".format(APP_NAME, APP_VERSION))
    ytdlp = get_ytdlp_path()
    if ytdlp:
        print("yt-dlp: {} ({})".format(_version_de(ytdlp) or "desconocida", ytdlp))
    else:
        print("yt-dlp: no encontrado")
    ffmpeg = get_ffmpeg_path()
    print("ffmpeg: {}".format(ffmpeg or "no encontrado"))


def _abrir_en_terminal():
    """Si se lanza como .app sin terminal, abre Terminal y vuelve a ejecutarse."""
    if not (getattr(sys, "frozen", False) and es_macos() and not os.environ.get("TERM")):
        return False
    ruta = sys.executable.replace('"', '\\"')
    cmd = 'tell application "Terminal" to do script "{}"'.format(ruta)
    subprocess.run(["osascript", "-e", cmd])
    subprocess.run(["osascript", "-e", 'tell application "Terminal" to activate'])
    return True


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--version" in argv or "-V" in argv:
        _mostrar_version()
        return
    if "--update" in argv or "--update-ytdlp" in argv:
        # La actualización debe funcionar incluso si aún no hay yt-dlp.
        check_dependencies(require_ytdlp=False, require_ffmpeg=False)
        update_ytdlp()
        return

    if _abrir_en_terminal():
        return

    print_platform_info()
    check_dependencies()
    check_update()
    default_dir = get_default_download_dir()
    download_folder = choose_download_folder(default_dir)
    opcion = mostrar_menu()
    url = pedir_url()

    if not url:
        print("No se introdujo ninguna URL. Saliendo.")
        return

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
        return

    print("\n¡Proceso finalizado!")


if __name__ == "__main__":
    main()
