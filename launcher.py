import os
import sys
import subprocess
from pathlib import Path

def main():
    # Base tanto en modo empaquetado (onefile) como en ejecución normal
    base = Path(getattr(sys, "_MEIPASS", os.path.dirname(sys.argv[0])))

    # Ubicación del script principal dentro del bundle
    script_path = base / "script_descarga.py"
    if not script_path.exists():
        # Fallback si ejecutas sin empaquetar
        script_path = Path.cwd() / "script_descarga.py"

    # Abre Terminal, ejecuta el script y espera una tecla para cerrar
    cmd = f'/bin/zsh -lc "{sys.executable} \\"{script_path}\\"; echo; read -n 1 -s -r -p \\"Pulsa una tecla para cerrar...\\""'
    subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "{cmd}"'])
    subprocess.run(['osascript', '-e', 'tell application "Terminal" to activate'])

if __name__ == "__main__":
    main()
