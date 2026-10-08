"""Fase 1: PDF -> texto por página, por tema y completo.

Uso (desde la raíz del proyecto):  python scripts/extraer_texto.py
Requiere pdftotext (xpdf o poppler) en el PATH.

Genera:
  libro_texto/paginas/pagina_NNN.txt   (NNN = página del PDF)
  libro_texto/por_capitulo/temaNN_slug.txt
  libro_texto/libro_completo.txt
  libro_texto/indice_paginas.tsv       (pdf, página impresa, tema de la cabecera)
"""
import re
import subprocess
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "Libro.pdf"
OUT = RAIZ / "libro_texto"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")[:40]


def main():
    (OUT / "paginas").mkdir(parents=True, exist_ok=True)
    (OUT / "por_capitulo").mkdir(parents=True, exist_ok=True)
    texto = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(PDF), "-"],
        capture_output=True, check=True).stdout.decode("utf-8")
    paginas = texto.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()

    filas, completo, temas = [], [], {}
    for n, pag in enumerate(paginas, start=1):
        lineas = [l for l in pag.splitlines() if l.strip()]
        # número impreso: al principio o al final de la última línea (pie de página)
        # (a veces va pegado al texto: «46 ■ …» o «… carretera.   187»)
        impresa = ""
        if lineas:
            m = re.match(r"\s*(\d{1,3})(?:\s|$)", lineas[-1]) or re.search(r"\s(\d{1,3})\s*$", lineas[-1])
            impresa = m.group(1) if m else ""
        # tema: cabecera «Tema N. Título» o «Anexo …» en las primeras líneas
        cab = ""
        # (a veces precedida de un icono: «STOP   Tema 8. …»; se ignora el índice general)
        es_indice_general = any("ÍNDICE GENERAL" in l for l in lineas[:2])
        for l in ([] if es_indice_general else lineas[:2]):
            m = re.search(r"(Tema \d+\.[^\n]*|Anexo[^\n]*)", l)
            if m:
                cab = re.sub(r"\s+", " ", m.group(1)).strip()
                break
        bloque = f"--- PÁGINA PDF {n} · LIBRO p.{impresa or '?'} ---\n{pag}"
        (OUT / "paginas" / f"pagina_{n:03d}.txt").write_text(bloque, encoding="utf-8")
        completo.append(bloque)
        filas.append(f"{n}\t{impresa}\t{cab}")
        if cab:
            temas.setdefault(cab, []).append(bloque)

    (OUT / "libro_completo.txt").write_text("\n".join(completo), encoding="utf-8")
    (OUT / "indice_paginas.tsv").write_text(
        "pdf\timpresa\tcabecera\n" + "\n".join(filas) + "\n", encoding="utf-8")

    for f in (OUT / "por_capitulo").glob("*.txt"):
        f.unlink()
    for cab, bloques in temas.items():
        m = re.match(r"Tema (\d+)", cab)
        pref = f"tema{int(m.group(1)):02d}" if m else "anexo"
        (OUT / "por_capitulo" / f"{pref}_{slug(cab.split('.', 1)[-1])}.txt").write_text(
            "\n".join(bloques), encoding="utf-8")
    print(f"{len(paginas)} páginas · {len(temas)} cabeceras distintas")
    for cab, b in temas.items():
        print(f"  {len(b):4d}  {cab}")


if __name__ == "__main__":
    main()
