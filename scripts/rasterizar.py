"""Rasteriza páginas del PDF cuando el texto no basta (tablas gráficas, señales).

Uso:  python scripts/rasterizar.py 252 [253 ...]   → libro_img/pagina_NNN.png (150 ppp)
Requiere PyMuPDF (pip install pymupdf). Equivale a «pdftoppm -r 150» del método.
"""
import sys
from pathlib import Path

import pymupdf as fitz

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "libro_img"
OUT.mkdir(exist_ok=True)
doc = fitz.open(RAIZ / "Libro.pdf")
for arg in sys.argv[1:]:
    n = int(arg)
    destino = OUT / f"pagina_{n:03d}.png"
    doc[n - 1].get_pixmap(dpi=150).save(destino)
    print(destino.relative_to(RAIZ))
