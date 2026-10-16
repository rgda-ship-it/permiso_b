"""Fase 7: genera los datos de ③ Juegos.

Uso:  python scripts/generar_juegos.py

Salidas:
  - guia/juegos/fichas.js  → AUTOMÁTICO, sale de capas ya verificadas:
      definiciones 🔴 de scripts/esencial/temaNN.json (Pasapalabra y ¿Quién soy?)
      y «Cifras que caen» de guia/resumen/temaNN.md (Parejas de cifras).
  - guia/juegos/datos.js   → REDACTADO A MANO en scripts/juegos/temaNN.json:
      {"mitos":       [{"f": frase, "r": true si es realidad / false si es mito,
                        "e": explicación, "p": "44", "v": ["fragmento literal", ...]}],
       "situaciones": [{"s": situación, "o": [3 opciones], "c": índice de la correcta,
                        "e": explicación, "p": "44", "v": [...]}],
       "secuencias":  [{"t": título, "pasos": [en orden], "p": "44", "v": [...]}]}

Igual que en la Guía esencial: cada fragmento de "v" tiene que estar LITERAL en la página
del tema (sin espacios ni mayúsculas) o el script ABORTA; avisa si la página no coincide.
Al final mide patrones: mitos frente a realidades, posición de la correcta y si la
correcta es la opción más larga.
"""
import json
import re
import sys
from collections import Counter

from generar_esencial import CURADO, COLORES, GUIA, RAIZ, clave, comprobar, leer_ficha, temario, texto_tema

JUEGOS = RAIZ / "scripts" / "juegos"


def escribir(nombre, var, datos):
    destino = GUIA / "juegos" / nombre
    destino.write_text(
        "/* Generado por scripts/generar_juegos.py: no editar a mano. */\n"
        f"window.{var} = " + json.dumps(datos, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    return destino


def main():
    errores, avisos = [], []
    fichas, curados = [], []
    tot = Counter()
    pos, largas, n_sit = Counter(), 0, 0
    for tid, titulo, archivo in temario():
        k = clave(tid)
        base = {"id": tid, "titulo": titulo, "archivo": archivo, "color": COLORES[tid]}
        ficha = leer_ficha((GUIA / "resumen" / f"{k}.md").read_text(encoding="utf-8"))
        f_es = CURADO / f"{k}.json"
        defs = json.loads(f_es.read_text(encoding="utf-8"))["memorizar"] if f_es.exists() else []
        fichas.append({**base, "defs": [{"t": d["t"], "d": d["d"], "p": d["p"]} for d in defs],
                       "cifras": ficha["cifras"]})

        f_j = JUEGOS / f"{k}.json"
        if not f_j.exists():
            avisos.append(f"{k}: sin datos de juegos (scripts/juegos/{k}.json)")
            continue
        cur = json.loads(f_j.read_text(encoding="utf-8"))
        sin, con = texto_tema(archivo)
        for tipo in ("mitos", "situaciones", "secuencias"):
            for n, it in enumerate(cur.get(tipo, []), 1):
                donde = f"{k} {tipo}[{n}]"
                if not it.get("v"):
                    errores.append(f"{donde}: sin fragmentos «v»")
                for fr in it.get("v", []):
                    comprobar(fr, it.get("p", ""), sin, con, donde, errores, avisos)
            tot[tipo] += len(cur.get(tipo, []))
        for n, m in enumerate(cur.get("mitos", []), 1):
            tot["realidades" if m["r"] else "mitos_f"] += 1
        for n, s in enumerate(cur.get("situaciones", []), 1):
            if len(s["o"]) != 3 or not 0 <= s["c"] < 3:
                errores.append(f"{k} situaciones[{n}]: hacen falta 3 opciones y «c» entre 0 y 2")
                continue
            n_sit += 1
            pos["abc"[s["c"]]] += 1
            lon = [len(o) for o in s["o"]]
            if lon[s["c"]] == max(lon) and lon.count(max(lon)) == 1:
                largas += 1
        for n, s in enumerate(cur.get("secuencias", []), 1):
            if not 3 <= len(s["pasos"]) <= 6:
                errores.append(f"{k} secuencias[{n}]: entre 3 y 6 pasos")
        curados.append({**base, **{t: cur.get(t, []) for t in ("mitos", "situaciones", "secuencias")}})

    for a in avisos:
        print("  · " + a)
    if errores:
        print(f"\n❌ {len(errores)} errores: no se generan los datos")
        for e in errores:
            print("  ✗ " + e)
        sys.exit(1)

    escribir("fichas.js", "FICHAS", {"temas": fichas})
    escribir("datos.js", "JUEGOS", {"temas": curados})
    n_def = sum(len(t["defs"]) for t in fichas)
    n_cif = sum(len(t["cifras"]) for t in fichas)
    print(f"\n✅ guia/juegos/fichas.js · {n_def} definiciones · {n_cif} cifras")
    print(f"✅ guia/juegos/datos.js · {len(curados)} temas · {tot['mitos']} mito/realidad · "
          f"{tot['situaciones']} situaciones · {tot['secuencias']} secuencias")
    print("\nPatrones:")
    if tot["mitos"]:
        print(f"  Mito o realidad: {tot['mitos_f']} mitos / {tot['realidades']} realidades "
              f"({round(100 * tot['realidades'] / tot['mitos'])} % realidades)")
    if n_sit:
        print(f"  Situaciones: correcta en a/b/c = {pos['a']}/{pos['b']}/{pos['c']} · "
              f"la más larga en {largas} de {n_sit} ({round(100 * largas / n_sit)} %)")


if __name__ == "__main__":
    main()
