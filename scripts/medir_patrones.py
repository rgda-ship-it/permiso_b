"""Mide patrones que delatan la respuesta en el examen tipo de cada tema (Fase 4).

Uso:  python scripts/medir_patrones.py [--detalle]   → una línea por tema publicado en guia/
      --detalle lista las preguntas en las que la correcta es la opción más larga.
Avisa si la correcta cae demasiado en la misma letra o si es la opción más larga
o la más corta con demasiada frecuencia (con 3 opciones, el azar da un 33 %).
"""
import re
import sys
from pathlib import Path

GUIA = Path(__file__).resolve().parent.parent / "guia"
total_pos, total_larga, total_corta, total_q = {"a": 0, "b": 0, "c": 0}, 0, 0, 0
for f in sorted(GUIA.glob("tema*/*.html")) + sorted(GUIA.glob("anexo/*.html")):
    s = f.read_text(encoding="utf-8")
    pos, larga, corta, avisos = {"a": 0, "b": 0, "c": 0}, 0, 0, []
    qs = re.findall(r'<ol class="opciones">(.*?)</ol>', s, re.S)
    for q in qs:
        ops = re.findall(r'<button( data-correct="true")?>(.*?)</button>', q)
        if len(ops) != 3 or sum(1 for c, _ in ops if c) != 1:
            avisos.append("pregunta sin 3 opciones o sin una única correcta")
            continue
        i = next(k for k, (c, _) in enumerate(ops) if c)
        pos["abc"[i]] += 1
        largos = [len(re.sub("<[^>]+>", "", t)) for _, t in ops]
        # solo cuenta si es estrictamente la más larga (un empate no delata la respuesta)
        es_larga = largos[i] > max(l for k, l in enumerate(largos) if k != i)
        larga += es_larga
        corta += largos[i] < min(l for k, l in enumerate(largos) if k != i)
        if es_larga and "--detalle" in sys.argv:
            print(f"   · {f.parent.name} q{qs.index(q) + 1}: {[re.sub('<[^>]+>', '', t) for _, t in ops]}")
    n = len(qs)
    if n and max(pos.values()) > n / 2:
        avisos.append("una letra acumula más de la mitad")
    if n and larga / n > 0.5:
        avisos.append("la correcta suele ser la más larga")
    if n and corta / n > 0.5:
        avisos.append("la correcta suele ser la más corta")
    print(f"{f.parent.name}: {n} preguntas · a/b/c {pos['a']}-{pos['b']}-{pos['c']} · "
          f"más larga {larga}/{n} ({100 * larga // max(n, 1)} %) · más corta {corta}/{n} · "
          f"refs {s.count('class=\"ref\"')} · autoev {s.count('class=\"pregunta\"')} · "
          f"no confundir {s.count('class=\"faq-item\"')}" + (f"  ⚠️ {'; '.join(avisos)}" if avisos else ""))
    for k in pos:
        total_pos[k] += pos[k]
    total_larga += larga
    total_corta += corta
    total_q += n
print(f"TOTAL: {total_q} preguntas · a/b/c {total_pos['a']}-{total_pos['b']}-{total_pos['c']} · "
      f"más larga {total_larga}/{total_q} · más corta {total_corta}/{total_q}")
