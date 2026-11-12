import os
import platform
import queue
import subprocess
import sys
import threading
from shutil import which
from tkinter import (
    Tk,
    Frame,
    Label,
    Button,
    Entry,
    StringVar,
    Text,
    Scrollbar,
    END,
    LEFT,
    RIGHT,
    BOTH,
    Y,
    X,
    filedialog,
)
from tkinter.ttk import Combobox, Progressbar

try:
    import yt_dlp
except ImportError:  # pragma: no cover - solo ocurre en instalaciones incompletas
    yt_dlp = None


def get_bundled_binary(name):
    """
    Devuelve la ruta del binario incluido en ./binaries (según plataforma).
    Si no está, intenta usar el del sistema (PATH).
    """
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == "Windows":
        binary_name = f"{name}.exe"
    elif platform.system() == "Linux":
        binary_name = f"{name}-linux" if name in ["yt-dlp", "ffmpeg"] else name
    else:
        binary_name = name  # macOS

    binary_path = os.path.join(base_path, "binaries", binary_name)
    if os.path.exists(binary_path):
        return binary_path

    system_binary = which(name)
    if system_binary:
        return system_binary

    return None


def _binario_funciona(ruta, flag="-version"):
    if not ruta:
        return False
    try:
        return subprocess.run(
            [ruta, flag],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def get_ffmpeg_bin():
    """ffmpeg incluido o del PATH que realmente arranque."""
    for candidato in (get_bundled_binary("ffmpeg"), which("ffmpeg")):
        if _binario_funciona(candidato):
            return candidato
    return None


def verificar_ffmpeg():
    return get_ffmpeg_bin() is not None


def verificar_ytdlp():
    return yt_dlp is not None


def version_ytdlp():
    if yt_dlp is None:
        return None
    return getattr(yt_dlp.version, "__version__", None)


def obtener_carpeta_por_defecto():
    # Descargas del usuario
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")


class MoncholvApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Moncholv Downloader")
        self.geometry("800x500")
        self.resizable(False, False)

        # Estado
        self.opcion_var = StringVar(value="1")  # por defecto: audio de un vídeo
        self.url_var = StringVar()
        self.destino_var = StringVar(value=obtener_carpeta_por_defecto())

        # Cola de mensajes del hilo de descarga hacia la interfaz
        self._cola_log = queue.Queue()

        # Construir UI
        self._crear_ui()
        self._procesar_cola_log()

        # Comprobar ffmpeg (binaries o PATH)
        ffmpeg_bin = get_ffmpeg_bin()
        if ffmpeg_bin:
            self._log(f"✓ FFmpeg encontrado: {ffmpeg_bin}")
        else:
            self._log("⚠️ FFmpeg no está disponible (ni en 'binaries' ni en PATH). Algunas funciones (MP3) pueden fallar.")

        if verificar_ytdlp():
            self._log(f"✓ yt-dlp disponible en el entorno de la app ({version_ytdlp() or 'versión desconocida'}).")
        else:
            self._log("⚠️ yt-dlp no se encontró. La app no podrá descargar vídeos/audio.")

    def _crear_ui(self):
        # Marco superior (título y descripción)
        top_frame = Frame(self, padx=10, pady=10)
        top_frame.pack(fill=X)

        Label(top_frame, text="Moncholv Video & Audio Downloader", font=("Helvetica", 16, "bold")).pack(anchor="w")
        Label(
            top_frame,
            text="Selecciona qué quieres descargar, introduce la URL y elige (o deja) la carpeta Descargas.",
            font=("Helvetica", 10),
        ).pack(anchor="w")

        # Marco de opciones (lado izquierdo)
        options_frame = Frame(self, padx=10, pady=10)
        options_frame.pack(fill=X)

        Label(options_frame, text="Tipo de descarga:", font=("Helvetica", 11, "bold")).pack(anchor="w")

        # Combo para opciones
        combo_frame = Frame(options_frame)
        combo_frame.pack(fill=X, pady=5)

        self.opciones_map = {
            "1. Audio de UN solo vídeo": "1",
            "2. Audios de lista de reproducción (playlist completa)": "2",
            "3. Vídeo de UN solo vídeo": "3",
            "4. Vídeos de lista de reproducción (playlist completa)": "4",
        }

        self.combo_opciones = Combobox(
            combo_frame,
            values=list(self.opciones_map.keys()),
            state="readonly",
            width=60,
        )
        self.combo_opciones.current(0)  # opción 1 por defecto
        self.combo_opciones.pack(side=LEFT)

        self.combo_opciones.bind("<<ComboboxSelected>>", self._on_opcion_cambiada)

        # Campo URL
        url_frame = Frame(self, padx=10, pady=5)
        url_frame.pack(fill=X)

        self.label_url = Label(url_frame, text="URL del vídeo:", font=("Helvetica", 11, "bold"))
        self.label_url.pack(anchor="w")

        self.entry_url = Entry(url_frame, textvariable=self.url_var, width=80)
        self.entry_url.pack(fill=X)

        # Campo carpeta destino
        destino_frame = Frame(self, padx=10, pady=5)
        destino_frame.pack(fill=X)

        Label(destino_frame, text="Carpeta de destino:", font=("Helvetica", 11, "bold")).pack(anchor="w")

        destino_top = Frame(destino_frame)
        destino_top.pack(fill=X)

        self.entry_destino = Entry(destino_top, textvariable=self.destino_var, width=60)
        self.entry_destino.pack(side=LEFT, fill=X, expand=True)

        btn_browse = Button(destino_top, text="Seleccionar carpeta…", command=self._seleccionar_carpeta)
        btn_browse.pack(side=RIGHT, padx=5)

        Label(
            destino_frame,
            text="Si dejas el campo vacío o pulsas Enter, se usará automáticamente la carpeta Descargas.",
            font=("Helvetica", 9),
        ).pack(anchor="w")

        # Botón de descarga
        actions_frame = Frame(self, padx=10, pady=10)
        actions_frame.pack(fill=X)

        btn_download = Button(
            actions_frame,
            text="Iniciar descarga",
            font=("Helvetica", 12, "bold"),
            command=self._iniciar_descarga_thread,
        )
        btn_download.pack()

        # Barra de progreso
        progress_frame = Frame(self, padx=10, pady=5)
        progress_frame.pack(fill=X)

        Label(progress_frame, text="Progreso:", font=("Helvetica", 10)).pack(anchor="w")

        self.progress = Progressbar(progress_frame, orient="horizontal", length=400, mode="indeterminate")
        self.progress.pack(fill=X)

        # Área de log/salida
        log_frame = Frame(self, padx=10, pady=10)
        log_frame.pack(fill=BOTH, expand=True)

        Label(log_frame, text="Salida / Log:", font=("Helvetica", 11, "bold")).pack(anchor="w")

        text_frame = Frame(log_frame)
        text_frame.pack(fill=BOTH, expand=True)

        self.text_log = Text(text_frame, wrap="word")
        self.text_log.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(text_frame, command=self.text_log.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_log["yscrollcommand"] = scrollbar.set

        self._log("Aplicación iniciada. Selecciona una opción, introduce la URL y pulsa 'Iniciar descarga'.\n")

    def _log(self, mensaje: str):
        """Encola el mensaje; la interfaz lo escribe en el hilo principal."""
        self._cola_log.put(mensaje)

    def _procesar_cola_log(self):
        try:
            while True:
                mensaje = self._cola_log.get_nowait()
                self.text_log.insert(END, mensaje + "\n")
                self.text_log.see(END)
        except queue.Empty:
            pass
        self.after(100, self._procesar_cola_log)

    def _on_opcion_cambiada(self, event=None):
        texto = self.combo_opciones.get()
        opcion = self.opciones_map.get(texto, "1")
        self.opcion_var.set(opcion)

        # Actualizar etiqueta de URL según sea vídeo o playlist
        if opcion in {"2", "4"}:
            self.label_url.config(text="URL de la lista de reproducción:")
        else:
            self.label_url.config(text="URL del vídeo:")

    def _seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(initialdir=obtener_carpeta_por_defecto())
        if carpeta:
            self.destino_var.set(carpeta)
            self._log(f"✅ Carpeta seleccionada: {carpeta}")
        else:
            self._log("ℹ️ No se cambió la carpeta de destino.")

    def _iniciar_descarga_thread(self):
        # Usar un hilo para no bloquear la interfaz mientras descarga
        hilo = threading.Thread(target=self._iniciar_descarga, daemon=True)
        hilo.start()

    def _iniciar_descarga(self):
        opcion = self.opcion_var.get()
        url = self.url_var.get().strip()
        destino_input = self.destino_var.get().strip()

        if not url:
            self._log("❌ Debes introducir una URL.")
            return

        if yt_dlp is None:
            self._log("❌ yt-dlp no está instalado en este entorno.")
            return

        # Resolver carpeta destino (Descargas por defecto si está vacío)
        if not destino_input:
            destino = obtener_carpeta_por_defecto()
            self.destino_var.set(destino)
            self._log(f"📁 Usando carpeta Descargas por defecto: {destino}")
        else:
            destino = os.path.expanduser(destino_input)

        try:
            os.makedirs(destino, exist_ok=True)
            self._log(f"✅ Carpeta preparada: {destino}")
        except Exception as e:
            self._log(f"❌ Error creando la carpeta: {e}")
            return

        plantilla_salida = os.path.join(destino, "%(title)s.%(ext)s")

        # Determinar modo (playlist vs vídeo suelto)
        if opcion == "2":
            self._log("🔊 Modo: audios de LISTA DE REPRODUCCIÓN (playlist completa).")
        elif opcion == "4":
            self._log("🎬 Modo: vídeos de LISTA DE REPRODUCCIÓN (playlist completa).")
        elif opcion == "1":
            self._log("🔊 Modo: audio de UN solo vídeo.")
        elif opcion == "3":
            self._log("🎬 Modo: vídeo de UN solo vídeo.")
        else:
            self._log("❌ Opción no reconocida.")
            return

        self._log("⏳ Descarga en progreso, espera un momento...\n")
        self.progress.start(10)  # mueve la barra cada 10 ms

        ffmpeg_bin = get_ffmpeg_bin()

        # Configuración de yt-dlp según tipo
        ydl_opts = {
            "outtmpl": plantilla_salida,
            "noplaylist": opcion in {"1", "3"},
            "retries": 10,
            "fragment_retries": 10,
            "extractor_retries": 3,
            "quiet": True,
            "no_warnings": False,
            "logger": _YdlLogger(self._log),
        }
        if ffmpeg_bin:
            ydl_opts["ffmpeg_location"] = ffmpeg_bin

        if opcion in {"1", "2"}:
            # Audio
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "0",
                    }],
                }
            )
            self._log("🎧 Descargando audio en formato MP3...")
        else:
            # Vídeo
            ydl_opts.update(
                {
                    "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
                    "merge_output_format": "mp4",
                }
            )
            self._log("📽️ Descargando vídeo en formato MP4...")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([url])
        except Exception as e:
            self._log(f"❌ Error durante la descarga: {e}")
        else:
            if error_code == 0:
                self._log("✅ Descarga completada correctamente.")
            else:
                self._log(f"⚠️ Hubo errores durante la descarga (código: {error_code}).")
        finally:
            self.progress.stop()


class _YdlLogger:
    """Redirige los mensajes de yt-dlp a la interfaz sin romper el hilo."""

    def __init__(self, log):
        self._log = log

    def debug(self, msg):
        if msg.startswith("[debug]"):
            return
        self._log(msg)

    def info(self, msg):
        self._log(msg)

    def warning(self, msg):
        self._log("⚠️ " + msg)

    def error(self, msg):
        self._log("❌ " + msg)


def main():
    app = MoncholvApp()
    app.mainloop()


if __name__ == "__main__":
    main()
