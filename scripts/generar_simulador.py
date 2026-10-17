"""Fase 8: genera ④ Examen (guia/simulador/index.html, autocontenido).

Uso:  python scripts/generar_simulador.py

Recoge:
  - las preguntas del «Examen tipo» (fase 4) de cada página de tema;
  - si existe, scripts/simulador/preguntas_estilo_examen.json, redactadas desde la guía:
      [{"tema": "T3", "q": enunciado, "o": [3 opciones], "c": índice correcta,
        "e": explicación, "p": "44", "v": ["fragmento literal", ...]}]
    (cada fragmento de "v" tiene que estar LITERAL en la página del tema o el script ABORTA).

Rellena scripts/plantillas/simulador.html (marca /*PREGUNTAS*/) y escribe guia/simulador/index.html.
Marca «fija» la opción que no se puede barajar («todas/ninguna de las anteriores», «a y b»…).
Comprueba 3 opciones y una sola correcta, y mide la posición de la correcta y si es la más larga.
"""
import json
import re
import sys
from collections import Counter
from html import unescape

from generar_esencial import COLORES, GUIA, RAIZ, comprobar, temario, texto_tema

PLANTILLA = RAIZ / "scripts" / "plantillas" / "simulador.html"
EXTRA = RAIZ / "scripts" / "simulador" / "preguntas_estilo_examen.json"
FIJA = re.compile(r"\b(todas|ninguna|ambas) (de )?las (anteriores|opciones)|\b[abc]\) y [abc]\)|\b[abc] y [abc]\b", re.I)


def texto(h):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", h))).strip()


def preguntas_tema(tid, archivo, errores):
    html = (GUIA / archivo).read_text(encoding="utf-8")
    out = []
    for n, bloque in enumerate(html.split('<div class="quiz-question">')[1:], 1):
        donde = f"{tid} pregunta {n}"
        enun = re.search(r"<p>\s*\d+\.\s*(.*?)</p>", bloque, re.S)
        ops = re.findall(r"<button( data-correct=\"true\")?>(.*?)</button>", bloque, re.S)
        just = re.search(r'<div class="justificacion">(.*?)</div>', bloque, re.S)
        if not (enun and just) or len(ops) != 3 or sum(1 for c, _ in ops if c) != 1:
            errores.append(f"{donde}: hace falta enunciado, justificación, 3 opciones y una sola correcta")
            continue
        e = just.group(1).strip()
        paginas = re.findall(r'data-tooltip="[^"]*p\. ([\d\-, ]+)"', e)
        if not paginas:
            errores.append(f"{donde}: la justificación no cita página")
        out.append({"tema": tid, "q": texto(enun.group(1)), "o": [texto(t) for _, t in ops],
                    "c": next(k for k, (c, _) in enumerate(ops) if c),
                    "e": texto(re.sub(r'<span class="ref".*?</span>', "", e, flags=re.S)),
                    "p": ", ".join(paginas)})
    return out


def main():
    errores, avisos = [], []
    temas, preguntas = [], []
    archivos = {}
    for tid, titulo, archivo in temario():
        temas.append({"id": tid, "titulo": titulo, "archivo": archivo, "color": COLORES[tid]})
        archivos[tid] = archivo
        preguntas += preguntas_tema(tid, archivo, errores)
    n_tema = len(preguntas)

    if EXTRA.exists():
        for n, it in enumerate(json.loads(EXTRA.read_text(encoding="utf-8")), 1):
            donde = f"estilo examen [{n}]"
            if it.get("tema") not in archivos or len(it.get("o", [])) != 3 or not 0 <= it.get("c", -1) < 3:
                errores.append(f"{donde}: tema desconocido, o no tiene 3 opciones y «c» entre 0 y 2")
                continue
            if not it.get("v"):
                errores.append(f"{donde}: sin fragmentos «v»")
            sin, con = texto_tema(archivos[it["tema"]])
            for fr in it.get("v", []):
                comprobar(fr, it.get("p", ""), sin, con, donde, errores, avisos)
            preguntas.append({k: it[k] for k in ("tema", "q", "o", "c", "e", "p")})

    pos, largas = Counter(), 0
    for i, q in enumerate(preguntas):
        q["id"] = i
        fijas = [k for k, o in enumerate(q["o"]) if FIJA.search(o)]
        if fijas:
            q["fija"] = fijas
        pos["abc"[q["c"]]] += 1
        lon = [len(o) for o in q["o"]]
        largas += lon[q["c"]] > max(l for k, l in enumerate(lon) if k != q["c"])

    for a in avisos:
        print("  · " + a)
    if errores:
        print(f"\n❌ {len(errores)} errores: no se genera el examen")
        for e in errores:
            print("  ✗ " + e)
        sys.exit(1)

    datos = json.dumps({"temas": temas, "preguntas": preguntas}, ensure_ascii=False, separators=(",", ":"))
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    if "/*PREGUNTAS*/" not in plantilla:
        sys.exit("La plantilla no tiene la marca /*PREGUNTAS*/")
    destino = GUIA / "simulador" / "index.html"
    destino.write_text(plantilla.replace("/*PREGUNTAS*/", datos.replace("</", "<\\/")), encoding="utf-8")
    n = len(preguntas)
    print(f"✅ {destino.relative_to(RAIZ)} · {n} preguntas ({n_tema} de los temas, {n - n_tema} estilo examen)")
    print(f"Patrones: correcta en a/b/c = {pos['a']}/{pos['b']}/{pos['c']} · la más larga en {largas} de {n} "
          f"({round(100 * largas / max(n, 1))} %) · opciones fijas: {sum(1 for q in preguntas if 'fija' in q)}")
    print("En pantalla las opciones se barajan en cada intento (salvo las fijas).")


if __name__ == "__main__":
    main()
