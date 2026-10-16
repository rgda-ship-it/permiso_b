"""Fase 6: genera guia/esencial/datos.js a partir de las fichas y de los datos curados.

Uso:  python scripts/generar_esencial.py

Entradas por tema:
  - guia/resumen/temaNN.md          → mapa, tabla(s) clave, cifras y «No confundir» (automático)
  - scripts/esencial/temaNN.json    → curado a mano:
      {"memorizar": [{"t": término, "d": definición corta, "p": "44", "v": ["fragmento literal", ...]}],
       "dominar":   [{"t": concepto, "d": explicación, "p": "45-48", "cubre": [1, 2], "v": [...]}],
       "mnemo":     [{"r": regla para recordar, "base": "de dónde sale"}],
       "conexiones":[{"id": "T10", "por": "por qué se relaciona"}]}

Garantía de fidelidad: cada fragmento de "v" tiene que aparecer LITERALMENTE en la página
del tema (sin tener en cuenta espacios ni mayúsculas). Si alguno no aparece, el script ABORTA.
Además avisa si la página "p" no coincide con ninguna de las dos referencias (p.XX) que
rodean ese fragmento en la guía (la anterior y la siguiente).
Al final informa de la cobertura: qué líneas del «Mapa del punto» no cubre ningún concepto 🟠.
"""
import json
import re
import sys
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GUIA = RAIZ / "guia"
CURADO = RAIZ / "scripts" / "esencial"
COLORES = {"T1": "#248ec5", "T2": "#009ee3", "T3": "#00b2c3", "T4": "#008784", "T5": "#7fb289",
           "T6": "#a9d19a", "T7": "#d2db5c", "T8": "#dabe3b", "T9": "#f3c05c", "T10": "#f3997a",
           "T11": "#e09197", "T12": "#eb5f84", "T13": "#e5007d", "T14": "#c35b9e", "T15": "#9184be",
           "T16": "#738fb3", "T17": "#476eac", "ANEXO": "#023d83"}


def temario():
    js = (GUIA / "js" / "temario-nav.js").read_text(encoding="utf-8")
    return re.findall(r'id: "([^"]+)", numero: \d+, titulo: "([^"]+)", archivo: "([^"]+)"', js)


def clave(tid):
    return "anexo" if tid == "ANEXO" else f"tema{int(tid[1:]):02d}"


def norm(s):
    s = s.lower().replace("«", '"').replace("»", '"').replace("’", "'")
    return re.sub(r"\s+", "", s)


def paginas(txt):
    out = set()
    for a, b in re.findall(r"(\d+)(?:-(\d+))?", txt):
        out.update(range(int(a), int(b or a) + 1))
    return out


def texto_tema(archivo):
    """(texto normalizado sin refs, texto normalizado con marcadores §p…§ en las refs)."""
    h = (GUIA / archivo).read_text(encoding="utf-8")
    h = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r'<span class="ref"[^>]*>(.*?)</span>', lambda m: f" §{m.group(1)}§ ", h)
    t = unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"\(p\.([\d\-, ]+)\)", lambda m: f" §p.{m.group(1)}§ ", t)  # páginas en títulos de tabla
    con = norm(t)
    sin = re.sub(r"§[^§]*§", "", con)
    return sin, con


def comprobar(fr, p, sin, con, donde, errores, avisos):
    f = norm(fr)
    if f not in sin:
        errores.append(f"{donde}: el fragmento no aparece en la guía → «{fr}»")
        return
    i = con.find(f)
    if i < 0:
        avisos.append(f"{donde}: el fragmento cruza una referencia; no se comprueba la página")
        return
    sig = re.search(r"§([^§]*)§", con[i + len(f):])
    ant = re.findall(r"§([^§]*)§", con[:i])
    cerca = [m for m in (sig.group(1) if sig else None, ant[-1] if ant else None) if m]
    if cerca and p and not any(paginas(p) & paginas(c) for c in cerca):
        avisos.append(f"{donde}: página {p}, pero la guía cita {' / '.join(cerca)} junto a «{fr[:40]}…»")


def leer_ficha(md):
    def seccion(t):
        m = re.search(r"\*\*" + re.escape(t) + r"[^*]*\*\*\n\n(.*?)(?=\n\*\*|\n---)", md, re.S)
        return m.group(1).strip() if m else ""

    def tabla(bloque):
        filas = [l for l in bloque.splitlines() if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l)]
        celdas = [[c.strip() for c in f.strip().strip("|").split("|")] for f in filas]
        return celdas[0], celdas[1:]

    frase = re.search(r"_\(tema completo:.*?\)_\n\n(.+?)\n", md).group(1).strip()
    mapa = [re.sub(r"^\d+\. ", "", l) for l in re.findall(r"^\d+\. .+$", seccion("Mapa del punto"), re.M)]
    tablas = []
    for titulo, cuerpo in re.findall(r"\*\*Tabla clave — (.+?)\*\*\n\n((?:\|.*\n)+)", md):
        cab, filas = tabla(cuerpo)
        tablas.append({"titulo": titulo, "cab": cab, "filas": filas})
    _, cifras = tabla(seccion("Cifras que caen"))
    trampas = []
    for l in re.findall(r"^- \*\*(.+?):\*\* (.+)$", seccion("No confundir"), re.M):
        trampas.append({"t": l[0], "d": l[1]})
    return {"frase": frase, "mapa": mapa, "tablas": tablas,
            "cifras": [{"c": c[0], "v": c[1], "p": c[2]} for c in cifras], "trampas": trampas}


def main():
    errores, avisos, temas, cobertura = [], [], [], []
    ids = {t for t, _, _ in temario()}
    for tid, titulo, archivo in temario():
        k = clave(tid)
        ficha = leer_ficha((GUIA / "resumen" / f"{k}.md").read_text(encoding="utf-8"))
        f_json = CURADO / f"{k}.json"
        if not f_json.exists():
            avisos.append(f"{k}: sin datos curados (scripts/esencial/{k}.json)")
            continue
        cur = json.loads(f_json.read_text(encoding="utf-8"))
        sin, con = texto_tema(archivo)
        for tipo in ("memorizar", "dominar"):
            for n, it in enumerate(cur.get(tipo, []), 1):
                donde = f"{k} {tipo}[{n}] «{it['t']}»"
                if not it.get("v"):
                    errores.append(f"{donde}: sin fragmentos «v»")
                for fr in it.get("v", []):
                    comprobar(fr, it.get("p", ""), sin, con, donde, errores, avisos)
        n_mem = len(cur.get("memorizar", []))
        if not 5 <= n_mem <= 10:
            avisos.append(f"{k}: {n_mem} definiciones para memorizar (5-10)")
        for c in cur.get("conexiones", []):
            if c["id"] not in ids:
                errores.append(f"{k}: conexión a un tema que no existe: {c['id']}")
        cubiertas = {i for d in cur.get("dominar", []) for i in d.get("cubre", [])}
        faltan = [i for i in range(1, len(ficha["mapa"]) + 1) if i not in cubiertas]
        cobertura.append((k, len(ficha["mapa"]) - len(faltan), len(ficha["mapa"]), faltan))
        temas.append({
            "id": tid, "titulo": titulo, "archivo": archivo, "color": COLORES[tid], **ficha,
            "memorizar": [{"t": i["t"], "d": i["d"], "p": i["p"]} for i in cur.get("memorizar", [])],
            "dominar": [{"t": i["t"], "d": i["d"], "p": i["p"], "cubre": i.get("cubre", [])}
                        for i in cur.get("dominar", [])],
            "mnemo": cur.get("mnemo", []), "conexiones": cur.get("conexiones", []),
        })

    for a in avisos:
        print("  · " + a)
    if errores:
        print(f"\n❌ {len(errores)} errores: no se genera datos.js")
        for e in errores:
            print("  ✗ " + e)
        sys.exit(1)

    destino = GUIA / "esencial" / "datos.js"
    destino.write_text(
        "/* Generado por scripts/generar_esencial.py: no editar a mano. */\n"
        "window.ESENCIAL = " + json.dumps({"temas": temas}, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    print(f"\n✅ {destino.relative_to(RAIZ)} · {len(temas)} temas · "
          f"{sum(len(t['memorizar']) for t in temas)} definiciones · "
          f"{sum(len(t['dominar']) for t in temas)} conceptos")
    tot_c = sum(c for _, c, _, _ in cobertura)
    tot = sum(n for _, _, n, _ in cobertura)
    print(f"Cobertura del Mapa del punto por los conceptos 🟠: {tot_c}/{tot}")
    for k, c, n, faltan in cobertura:
        if faltan:
            print(f"  {k}: faltan las líneas {faltan}")


if __name__ == "__main__":
    main()
