#!/usr/bin/env bash
#
# Descarga las últimas versiones oficiales de yt-dlp para macOS, Linux y
# Windows en binaries/ y verifica sus sumas SHA-256.
#
# Uso:
#   ./scripts/update_binaries.sh              # última release
#   ./scripts/update_binaries.sh 2026.10.26   # una release concreta

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TAG="${1:-latest}"
if [ "$TAG" = "latest" ]; then
  BASE="https://github.com/yt-dlp/yt-dlp/releases/latest/download"
else
  BASE="https://github.com/yt-dlp/yt-dlp/releases/download/${TAG}"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> Descargando yt-dlp (${TAG})"
curl -fL --retry 3 --retry-delay 2 -o "$TMP/yt-dlp_macos" "$BASE/yt-dlp_macos"
curl -fL --retry 3 --retry-delay 2 -o "$TMP/yt-dlp_linux" "$BASE/yt-dlp_linux"
curl -fL --retry 3 --retry-delay 2 -o "$TMP/yt-dlp.exe" "$BASE/yt-dlp.exe"
curl -fL --retry 3 --retry-delay 2 -o "$TMP/SHA2-256SUMS" "$BASE/SHA2-256SUMS"

echo "==> Verificando sumas SHA-256"
(
  cd "$TMP"
  grep -E ' (yt-dlp_macos|yt-dlp_linux|yt-dlp\.exe)$' SHA2-256SUMS > sums.txt
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c sums.txt
  else
    shasum -a 256 -c sums.txt
  fi
)

echo "==> Instalando en binaries/"
install -m 755 "$TMP/yt-dlp_macos" binaries/yt-dlp
install -m 755 "$TMP/yt-dlp_linux" binaries/yt-dlp-linux
install -m 644 "$TMP/yt-dlp.exe" binaries/yt-dlp.exe

VERSION="$(./binaries/yt-dlp --version)"
# Ficheros que usa la app para conocer la versión sin lanzar el onefile.
# Formato: versión + tamaño del binario (para detectar sustituciones).
SIZE_MAC="$(wc -c < binaries/yt-dlp | tr -d ' ')"
SIZE_LINUX="$(wc -c < binaries/yt-dlp-linux | tr -d ' ')"
SIZE_WIN="$(wc -c < binaries/yt-dlp.exe | tr -d ' ')"
printf '%s\n%s\n' "$VERSION" "$SIZE_MAC" > binaries/yt-dlp.version
printf '%s\n%s\n' "$VERSION" "$SIZE_LINUX" > binaries/yt-dlp-linux.version
printf '%s\n%s\n' "$VERSION" "$SIZE_WIN" > binaries/yt-dlp.exe.version

echo "==> Versión: ${VERSION}"
echo "==> Listo. Recuerda recompilar la app para incluir el nuevo binario."
