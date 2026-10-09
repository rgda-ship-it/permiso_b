"""Fase 5: reduce cada página de tema a un extracto pequeño para escribir las fichas.

Uso:  python scripts/extraer_resumen.py [T3 ...]   → scripts/extractos/temaNN.md (todos si no se indica)

El extracto contiene, en este orden: título, descripción, «Mapa del tema», títulos de
apartados (h3/h4) de la Fase 1, tarjetas (⭐ = críticas) con su texto, avisos ⚠️, tablas
completas, resúmenes de «No confundas» con su respuesta, y páginas citadas.
Las fichas (guia/resumen/temaNN.md) se escriben DESDE ESTE EXTRACTO, no desde el libro.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GUIA = RAIZ / "guia"
OUT = RAIZ / "scripts" / "extractos"


def temario():
    """[(id, título, archivo)] desde temario-nav.js (única fuente del orden)."""
    js = (GUIA / "js" / "temario-nav.js").read_text(encoding="utf-8")
    return re.findall(r'id: "([^"]+)", numero: \d+, titulo: "([^"]+)", archivo: "([^"]+)"', js)


class Nodo:
    def __init__(self, tag, attrs, padre):
        self.tag, self.attrs, self.padre, self.hijos = tag, dict(attrs), padre, []

    def texto(self, con_refs=True):
        partes = []
        for h in self.hijos:
            if isinstance(h, str):
                partes.append(h)
            elif h.tag == "span" and "ref" in h.attrs.get("class", "").split():
                if con_refs:
                    partes.append(f" ({h.texto()})")
            elif h.tag in ("script", "style", "svg"):
                continue
            else:
                sep = " " if h.tag in ("li", "p", "br", "td", "th", "div", "h4", "h5") else ""
                partes.append(sep + h.texto(con_refs) + sep)
        return re.sub(r"\s+", " ", "".join(partes)).strip()

    def buscar(self, pred):
        for h in self.hijos:
            if isinstance(h, Nodo):
                if pred(h):
                    yield h
                yield from h.buscar(pred)

    def clase(self, c):
        return c in self.attrs.get("class", "").split()


class Arbol(HTMLParser):
    VACIOS = {"meta", "link", "br", "img", "hr", "input"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = Nodo("doc", [], None)
        self.actual = self.raiz

    def handle_starttag(self, tag, attrs):
        n = Nodo(tag, attrs, self.actual)
        self.actual.hijos.append(n)
        if tag not in self.VACIOS:
            self.actual = n

    def handle_endtag(self, tag):
        n = self.actual
        while n is not self.raiz and n.tag != tag:
            n = n.padre
        if n is not self.raiz:
            self.actual = n.padre

    def handle_data(self, data):
        self.actual.hijos.append(data)


def extracto(tid, titulo, archivo):
    p = Arbol()
    p.feed((GUIA / archivo).read_text(encoding="utf-8"))
    doc = p.raiz
    fase = {s.attrs.get("id"): s for s in doc.buscar(lambda n: n.tag == "section")}
    f1, f3 = fase["fase-1"], fase["fase-3"]
    desc = next(doc.buscar(lambda n: n.tag == "meta" and n.attrs.get("name") == "description")).attrs["content"]
    out = [f"# Extracto {tid} · {titulo}", f"archivo: {archivo}", "", f"> {desc}", ""]

    mapa = next(f1.buscar(lambda n: n.clase("mapa-punto")))
    out.append("## Mapa del tema")
    out += [f"{i}. {li.texto()}" for i, li in enumerate(mapa.buscar(lambda n: n.tag == "li"), 1)]
    out.append("")

    out.append("## Apartados")
    for h in f1.hijos:
        if isinstance(h, Nodo) and h.tag in ("h3", "h4") and h.texto() not in ("Mapa del tema", "Referencias"):
            out.append(("- " if h.tag == "h3" else "  - ") + h.texto())
    out.append("")

    out.append("## Tarjetas (⭐ = crítica)")
    for c in f1.buscar(lambda n: n.clase("concept-card")):
        h4 = next(c.buscar(lambda n: n.tag == "h4"), None)
        cuerpo = c.texto().replace(h4.texto(), "", 1).strip() if h4 else c.texto()
        out.append(f"- {'⭐ ' if c.clase('critica') else ''}**{h4.texto() if h4 else ''}**: {cuerpo}")
    out.append("")

    out.append("## Avisos ⚠️")
    out += [f"- {a.texto()}" for a in f1.buscar(lambda n: n.clase("aviso"))]
    out.append("")

    out.append("## Tablas")
    for t in f1.buscar(lambda n: n.tag == "table"):
        cap = next(t.buscar(lambda n: n.tag == "caption"), None)
        out.append(f"### {cap.texto() if cap else '(sin título)'}")
        for tr in t.buscar(lambda n: n.tag == "tr"):
            celdas = [c.texto() for c in tr.buscar(lambda n: n.tag in ("td", "th"))]
            out.append("| " + " | ".join(celdas) + " |")
        out.append("")

    out.append("## No confundas")
    for d in f3.buscar(lambda n: n.tag == "details" and n.clase("faq-item")):
        s = next(d.buscar(lambda n: n.tag == "summary"))
        primer_p = next(d.buscar(lambda n: n.tag == "p"), None)
        out.append(f"- **{s.texto()}**: {primer_p.texto() if primer_p else ''}")
    out.append("")

    textos = [r.texto() for r in f1.buscar(lambda n: n.clase("ref"))]
    textos += [m for c in f1.buscar(lambda n: n.tag == "caption") for m in re.findall(r"\(p\.([\d\-, ]+)\)", c.texto())]
    paginas = sorted({int(x) for t in textos for x in re.findall(r"\d+", t)})
    out.append("## Páginas citadas")
    out.append(", ".join(map(str, paginas)))
    return "\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pedir = set(sys.argv[1:])
    for tid, titulo, archivo in temario():
        if pedir and tid not in pedir:
            continue
        clave = "anexo" if tid == "ANEXO" else f"tema{int(tid[1:]):02d}"
        txt = extracto(tid, titulo, archivo)
        (OUT / f"{clave}.md").write_text(txt, encoding="utf-8")
        print(f"{clave}.md  {len(txt):6d} caracteres")


if __name__ == "__main__":
    main()
