import ast
import contextlib
import io
import pathlib
import sys
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "script_descarga.py").read_text(encoding="utf-8")

sys.path.insert(0, str(ROOT))
import script_descarga  # noqa: E402


class VersionTests(unittest.TestCase):
    def test_version_key_orders_dates(self):
        clave = script_descarga._version_key
        self.assertGreater(clave("2026.10.26"), clave("2026.3.17"))
        self.assertGreater(clave("2025.10.22"), clave("2025.9.30"))
        self.assertEqual(clave("2026.10.26"), (2026, 10, 26))

    def test_app_version_has_three_parts(self):
        self.assertRegex(script_descarga.APP_VERSION, r"^\d+\.\d+\.\d+$")

    def test_hay_actualizacion(self):
        hay = script_descarga.hay_actualizacion
        self.assertFalse(hay("2026.10.26", "2026.10.26"))
        self.assertFalse(hay("2026.10.26", "2026.3.17"))
        self.assertFalse(hay(None, "2026.10.26"))
        self.assertFalse(hay("2026.10.26", None))
        self.assertTrue(hay("2026.10.26", "2026.11.01"))
        self.assertTrue(hay("2026.3.17", "2026.10.26"))


class UpdateCheckTests(unittest.TestCase):
    def _ejecutar(self, actual, remota, respuesta="n"):
        with mock.patch.object(script_descarga, "YT_DLP_BIN", None), \
             mock.patch.object(script_descarga, "get_ytdlp_path", return_value="/fake/yt-dlp"), \
             mock.patch.object(script_descarga, "get_ytdlp_version", return_value=actual), \
             mock.patch.object(script_descarga, "_ultima_version_remota", return_value=remota), \
             mock.patch("builtins.input", return_value=respuesta) as entrada, \
             mock.patch.object(script_descarga, "update_ytdlp") as actualizar, \
             contextlib.redirect_stdout(io.StringIO()):
            script_descarga.check_update()
        return entrada, actualizar

    def test_no_pregunta_si_ya_esta_actualizado(self):
        entrada, actualizar = self._ejecutar("2026.10.26", "2026.10.26")
        entrada.assert_not_called()
        actualizar.assert_not_called()

    def test_no_pregunta_si_la_remota_es_mas_vieja(self):
        entrada, actualizar = self._ejecutar("2026.10.26", "2026.3.17")
        entrada.assert_not_called()
        actualizar.assert_not_called()

    def test_no_pregunta_si_no_hay_conexion(self):
        entrada, actualizar = self._ejecutar("2026.10.26", None)
        entrada.assert_not_called()
        actualizar.assert_not_called()

    def test_pregunta_y_actualiza_si_hay_version_nueva(self):
        entrada, actualizar = self._ejecutar("2026.10.26", "2026.11.01", respuesta="s")
        entrada.assert_called_once()
        actualizar.assert_called_once_with(version_remota="2026.11.01")

    def test_pregunta_pero_no_actualiza_si_dice_no(self):
        entrada, actualizar = self._ejecutar("2026.10.26", "2026.11.01", respuesta="n")
        entrada.assert_called_once()
        actualizar.assert_not_called()


class UpdateRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arbol = ast.parse(SOURCE)

    def _funcion(self, nombre):
        for nodo in self.arbol.body:
            if isinstance(nodo, ast.FunctionDef) and nodo.name == nombre:
                return nodo
        self.fail("No se encontró la función {}".format(nombre))

    def _cuerpo_sin_docstring(self, nombre):
        funcion = self._funcion(nombre)
        nodos = [
            nodo
            for nodo in funcion.body
            if not (
                isinstance(nodo, ast.Expr)
                and isinstance(nodo.value, ast.Constant)
                and isinstance(nodo.value.value, str)
            )
        ]
        return "\n".join(ast.unparse(nodo) for nodo in nodos)

    def test_update_never_relaunches_the_app_with_pip(self):
        """El bug original: `sys.executable -m pip` relanzaba la app empaquetada."""
        for nodo in ast.walk(self.arbol):
            if not isinstance(nodo, ast.Call):
                continue
            llamada = ast.unparse(nodo)
            if "sys.executable" in llamada:
                self.assertNotIn("pip", llamada, llamada)

    def test_check_update_uses_the_real_updater(self):
        cuerpo = self._cuerpo_sin_docstring("check_update")
        self.assertIn("update_ytdlp(", cuerpo)
        self.assertNotIn("sys.executable", cuerpo)

    def test_updater_downloads_and_validates_official_binary(self):
        self.assertIn("YTDLP_RELEASES_URL", SOURCE)
        self.assertIn("_descargar(", SOURCE)
        # Se valida antes de sustituir el binario que ya funcionaba
        self.assertIn("get_ytdlp_version(temporal)", SOURCE)
        self.assertIn("os.replace(temporal, destino)", SOURCE)


if __name__ == "__main__":
    unittest.main()
