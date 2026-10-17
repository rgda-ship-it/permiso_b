"""Comprueba los enlaces internos de todo el sitio (sin navegador).

Uso:  python scripts/verificar_enlaces.py

Para cada página .html de guia/ revisa href y src relativos: que el archivo exista y,
si llevan #ancla, que en la página de destino haya un id con ese nombre.
También revisa los enlaces que los scripts generan desde los datos («archivo» de cada tema).
Los enlaces externos (http, https, mailto) no se comprueban.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

GUIA = Path(__file__).resolve().parent.parent / "guia"


def ids(f, cache={}):
    if f not in cache:
        cache[f] = set(re.findall(r'\bid="([^"]+)"', f.read_text(encoding="utf-8")))
    return cache[f]


def main():
    fallos, n = [], 0
    paginas = sorted(GUIA.rglob("*.html"))
    for pag in paginas:
        h = pag.read_text(encoding="utf-8")
        h = re.sub(r"<script\b[^>]*>.*?</script>", "", h, flags=re.S)  # los enlaces dentro de JS se revisan aparte
        for attr, url in re.findall(r'\b(href|src)="([^"]+)"', h):
            if re.match(r"^(https?:|mailto:|data:|javascript:)", url):
                continue
            n += 1
            ruta, _, ancla = url.partition("#")
            destino = (pag.parent / unquote(ruta)).resolve() if ruta else pag
            if not destino.exists():
                fallos.append(f"{pag.relative_to(GUIA)}: {attr}=\"{url}\" → no existe")
            elif ancla and destino.suffix == ".html" and ancla not in ids(destino):
                fallos.append(f"{pag.relative_to(GUIA)}: {attr}=\"{url}\" → no hay id «{ancla}»")
    # «archivo» de cada tema en los datos (enlaces que pintan Guía, Juegos y Examen)
    for js in [GUIA / "js" / "temario-nav.js", GUIA / "esencial" / "datos.js", GUIA / "juegos" / "fichas.js",
               GUIA / "juegos" / "datos.js", GUIA / "simulador" / "index.html"]:
        for archivo in set(re.findall(r'"?archivo"?:\s*"([^"]+)"', js.read_text(encoding="utf-8"))):
            n += 1
            if not (GUIA / archivo).exists():
                fallos.append(f"{js.relative_to(GUIA)}: archivo «{archivo}» no existe")
    for f in fallos:
        print("  ✗ " + f)
    print(f"{'✅' if not fallos else '❌'} {len(paginas)} páginas · {n} enlaces internos · {len(fallos)} rotos")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
