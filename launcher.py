"""Lanzador legacy para macOS.

La app actual (`script_descarga.py` + `Moncho_YT_app.spec`) ya abre Terminal por
sí misma, así que este archivo no se usa en los builds.

No lo uses como punto de entrada de PyInstaller: en un ejecutable congelado
`sys.executable` es la propia app, y lanzarla con la ruta del script como
argumento la reinicia (los argumentos se ignoran), provocando bucles como el
antiguo fallo de "respondo s y vuelve a preguntar".
"""

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
