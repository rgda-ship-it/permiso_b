"""Fase 5: comprueba las fichas de guia/resumen/ contra el esquema fijo y contra la guía.

Uso:  python scripts/verificar_fichas.py   → informe por ficha y total de unidades clave

Comprueba en cada ficha:
  - esquema: ancla, título exacto del temario, enlace al tema, frase, «Mapa del punto» (5-8),
    1-2 «Tabla clave» (≤6 filas, ≤4 columnas), «Cifras que caen» (≤8 filas, página nunca vacía),
    «No confundir» (5 líneas) y separador final;
  - fidelidad: cada número de la ficha aparece en el texto de la página del tema
    (sin espacios ni puntos de miles) y cada página citada está dentro del rango del tema.
Unidades clave = líneas del mapa + filas de cifras + líneas de «No confundir».
Sale con código 1 si hay algún error.
"""
import re
import sys
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GUIA = RAIZ / "guia"
RANGOS = {"T1": (5, 25), "T2": (26, 41), "T3": (42, 73), "T4": (74, 85), "T5": (86, 119),
          "T6": (120, 138), "T7": (139, 153), "T8": (154, 211), "T9": (212, 242), "T10": (243, 266),
          "T11": (267, 300), "T12": (301, 318), "T13": (319, 340), "T14": (341, 364),
          "T15": (365, 387), "T16": (388, 436), "T17": (437, 466), "ANEXO": (467, 474)}


def temario():
    js = (GUIA / "js" / "temario-nav.js").read_text(encoding="utf-8")
    return re.findall(r'id: "([^"]+)", numero: \d+, titulo: "([^"]+)", archivo: "([^"]+)"', js)


def texto_html(archivo):
    h = (GUIA / archivo).read_text(encoding="utf-8")
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return unescape(re.sub(r"<[^>]+>", " ", h))


def norm_num(s):
    return s.replace(".", "").replace(" ", "")


def numeros(txt):
    """Números con decimales o miles (0,15 · 3.500 · 10W/40 se separa en 10 y 40)."""
    return set(re.findall(r"\d+(?:[.,]\d+)*", txt))


def seccion(md, titulo):
    m = re.search(r"\*\*" + re.escape(titulo) + r"[^*]*\*\*\n\n(.*?)(?=\n\*\*|\n---)", md, re.S)
    return m.group(1).strip() if m else None


def filas_tabla(bloque):
    return [l for l in bloque.splitlines() if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l)][1:]


def verificar(tid, titulo, archivo, md):
    errores, avisos = [], []
    if f'<a id="{tid}"></a>' not in md:
        errores.append("falta el ancla")
    if f"## {tid} · {titulo}\n" not in md:
        errores.append("el título no coincide con el temario")
    if f"[{archivo}](../{archivo})" not in md:
        errores.append("falta el enlace al tema")
    if not md.rstrip().endswith("---"):
        errores.append("falta el separador final ---")

    mapa = seccion(md, "Mapa del punto")
    lineas_mapa = re.findall(r"^\d+\. .+$", mapa or "", re.M)
    if not 5 <= len(lineas_mapa) <= 8:
        errores.append(f"Mapa del punto con {len(lineas_mapa)} líneas (5-8)")

    tablas = re.findall(r"\*\*Tabla clave — (.+?)\*\*\n\n((?:\|.*\n)+)", md)
    if not 1 <= len(tablas) <= 2:
        errores.append(f"{len(tablas)} tablas clave (1-2)")
    for t, cuerpo in tablas:
        f = filas_tabla(cuerpo)
        cols = cuerpo.splitlines()[0].count("|") - 1
        if len(f) > 6 or cols > 4:
            errores.append(f"tabla «{t}»: {len(f)} filas y {cols} columnas (≤6, ≤4)")
        if not re.search(r"\(p\.\d", t):
            errores.append(f"tabla «{t}» sin página")

    cifras = seccion(md, "Cifras que caen")
    filas_c = filas_tabla(cifras or "")
    if not 1 <= len(filas_c) <= 8:
        errores.append(f"Cifras que caen con {len(filas_c)} filas (1-8)")
    for fila in filas_c:
        celdas = [c.strip() for c in fila.strip("|").split("|")]
        if len(celdas) != 3 or not re.match(r"^\d", celdas[2]):
            errores.append(f"cifra sin página: {fila}")

    nc = seccion(md, "No confundir")
    lineas_nc = re.findall(r"^- \*\*.+$", nc or "", re.M)
    if len(lineas_nc) != 5:
        errores.append(f"No confundir con {len(lineas_nc)} líneas (5)")

    # fidelidad: números y páginas
    html = norm_num(texto_html(archivo))
    cuerpo = md.split("\n", 3)[3]  # sin ancla ni título
    cuerpo = re.sub(r"\(p\.[^)]*\)|\(p\.\d+.*?\)", " ", cuerpo)
    cuerpo = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", cuerpo)
    for fila in filas_c:  # la columna de página no cuenta como dato
        cuerpo = cuerpo.replace(fila, "|".join(fila.split("|")[:-2]) + "|")
    for n in sorted(numeros(cuerpo)):
        if norm_num(n) not in html:
            errores.append(f"el número «{n}» no aparece en la página del tema")
    ini, fin = RANGOS[tid]
    paginas = [int(p) for m in re.findall(r"\(p\.([\d\-, ]+)", md) for p in re.findall(r"\d+", m)]
    paginas += [int(c.strip("|").split("|")[-1].strip().split("-")[0]) for c in filas_c
                if re.match(r"^\d", c.strip("|").split("|")[-1].strip())]
    for p in paginas:
        if not ini <= p <= fin:
            avisos.append(f"página {p} fuera del rango {ini}-{fin} (¿referencia a otro tema?)")
    unidades = len(lineas_mapa) + len(filas_c) + len(lineas_nc)
    return errores, avisos, unidades


def main():
    total, fallos = 0, 0
    for tid, titulo, archivo in temario():
        clave = "anexo" if tid == "ANEXO" else f"tema{int(tid[1:]):02d}"
        f = GUIA / "resumen" / f"{clave}.md"
        if not f.exists():
            print(f"{clave}: (sin ficha)")
            continue
        errores, avisos, u = verificar(tid, titulo, archivo, f.read_text(encoding="utf-8"))
        total += u
        fallos += len(errores)
        print(f"{clave}: {u} unidades clave" + (" ✅" if not errores else f" ❌ {len(errores)} errores"))
        for e in errores:
            print(f"   ✗ {e}")
        for a in avisos:
            print(f"   · {a}")
    print(f"TOTAL: {total} unidades clave · {fallos} errores")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
