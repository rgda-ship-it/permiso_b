"""Fase 2: localiza la página del libro donde empieza cada apartado del índice de cada tema.

Uso:  python scripts/mapa_secciones.py  → imprime, por tema, «página  apartado».
Los apartados se copian de la página «Índice» de cada tema. Busca la primera línea,
después de la página de índice y dentro del rango del tema, que empiece por el título
(sin tener en cuenta tildes, mayúsculas ni espacios). «A|B»: A es el título del índice
y B la variante con que aparece en el cuerpo (títulos partidos en dos líneas o redactados
distinto); vale cualquiera de las dos.
Salida con «?» = no encontrado: revisar a mano.
"""
import re
import unicodedata
from pathlib import Path

PAG = Path(__file__).resolve().parent.parent / "libro_texto" / "paginas"

# id: (primera página = índice del tema, última página, [apartados; «-» = subapartado])
TEMAS = {
    "T1": (5, 25, ["Definiciones relacionadas|con los vehículos", "-Vehículos sin motor", "-Vehículos a motor",
                   "-Otro tipo de vehículos con motor|Otros tipos de vehículos a motor",
                   "Definiciones relacionadas|con las personas", "-Conductor", "-Peatón",
                   "-Titular del vehículo", "-Conductor habitual", "Categorías de los vehículos"]),
    "T2": (26, 41, ["Documentos necesarios para conducir", "Permiso de conducir", "-Tipos de permiso de conducir",
                    "-Permiso de conducir por puntos", "-Conductores noveles",
                    "-¿Cuándo debes renovar tu permiso", "Permiso de circulación",
                    "-¿Qué vehículos deben tener permiso de circulación|¿Qué vehículos deben tener", "-¿Qué datos aparecen en el permiso|¿Qué datos aparecen",
                    "Tarjeta de inspección técnica", "-¿Qué vehículos deben tener|la tarjeta",
                    "-¿Qué datos aparecen en la tarjeta", "-¿Cuándo debes pasar la inspección|¿Cuándo debes pasar",
                    "-Resultados de la inspección", "Seguro obligatorio de responsabilidad civil",
                    "-¿Qué vehículos deben tener seguro", "-¿Qué cubre el seguro", "-¿Qué no cubre el seguro",
                    "-¿Qué consecuencias tiene no asegurar", "Personas responsables"]),
    "T3": (42, 73, ["Estado físico y psicológico", "Factores que influyen en el estado|Factores que influyen", "-Fatiga|Estar cansado (fatiga)",
                    "-Somnolencia", "-Alcohol", "-Otras drogas", "-Enfermedades y medicamentos",
                    "-Alimentación", "-Ropa adecuada", "Accidentes por distracciones",
                    "-Fumar en el vehículo", "-Uso del teléfono móvil|Usar el teléfono móvil", "-Navegadores GPS"]),
    "T4": (74, 85, ["Seguridad en la carretera", "Obligaciones de los conductores", "-Obligaciones generales",
                    "-Vehículos de dos o tres ruedas", "-Vehículos especiales", "Obligaciones de los peatones",
                    "-Obligaciones generales", "-Vehículos de movilidad personal", "Animales en carretera|Animales en la carretera"]),
    "T5": (86, 119, ["La importancia del vehículo", "Elementos de seguridad activa", "-Sistemas de alumbrado",
                     "-Los frenos", "-Las ruedas", "-Otros elementos de seguridad activa",
                     "Elementos de seguridad pasiva", "-El chasis y la carrocería", "-El cinturón de seguridad",
                     "-Los airbags", "-El reposacabezas", "-El casco"]),
    "T6": (120, 138, ["Mandos del vehículo", "-Mandos de los vehículos en general", "-Mandos de las motocicletas",
                      "Visibilidad al conducir", "-Limpiaparabrisas", "-Lavaparabrisas", "-Luneta térmica",
                      "-Retrovisores", "Reglas para conducir de forma cómoda", "-Reglas para conducir turismos",
                      "-Reglas para conducir motocicletas", "Sistemas que ayudan a conducir"]),
    "T7": (139, 153, ["Normas generales|para usar las luces", "Luces del vehículo", "-Luces de posición",
                      "-Luz de estacionamiento", "-Luces de gálibo", "-Luz de largo alcance",
                      "-Luz de corto alcance", "-Luces de antiniebla|Luces antiniebla", "-Catadióptrico",
                      "-Luz indicadora de dirección", "-Señal de emergencia", "-Luz de frenado",
                      "-Tercera luz de freno", "-Luz de marcha atrás", "Señales acústicas"]),
    "T8": (154, 211, ["Tipos de señales", "-Normas generales", "-Los agentes de tráfico|Agentes de tráfico",
                      "-Señales temporales", "-Semáforos", "Señales verticales",
                      "-Señales que advierten de peligro|Señales que avisan de peligro", "-Señales de reglamentación", "-Señales de indicación",
                      "Líneas y marcas en las carreteras", "-Líneas y marcas blancas",
                      "-Líneas y marcas de colores"]),
    "T9": (212, 242, ["La vía para vehículos y peatones", "-Partes de la vía", "-Otras zonas de la vía",
                      "-Dirección y sentido", "Tipos de vía", "-Dependiendo de dónde está",
                      "-Dependiendo de sus características|Dependiendo$", "-Colores que indican", "Los carriles",
                      "-¿Por dónde deben circular", "-Normas para usar los carriles", "-Carriles reservados",
                      "-Carriles especiales|Supuestos especiales", "-El arcén", "Circular por autopistas y autovías",
                      "-Emergencias en la autopista"]),
    "T10": (243, 266, ["Tipos de velocidad", "-Velocidad máxima", "-Velocidad mínima", "-Velocidad inadecuada",
                       "-Velocidad adecuada", "-Situaciones en las que debes conducir", "Velocidad genérica",
                       "-Límites de velocidad|fuera de pueblos", "-Límites de velocidad máxima|dentro",
                       "-Límites de velocidad mínima", "-¿Por qué son necesarios", "Tipos de distancia",
                       "-Distancia de reacción", "-Distancia de frenado", "-Distancia de detención",
                       "-Separación lateral", "-Distancia de seguridad"]),
    "T11": (267, 300, ["Regla de seguridad R.S.M", "-Pasos de la regla", "-Regla de seguridad al entrar",
                       "-Precauciones al cambiar de carril", "Adelantar a otros vehículos",
                       "-¿Por qué lado debes adelantar|¿Por qué lado adelantan", "-Pasos a seguir para adelantar",
                       "-Obligaciones del conductor|al que le adelanta", "-¿Cuándo está prohibido adelantar",
                       "Cambio de dirección y de sentido", "-Cambio de dirección", "-Cambio de sentido",
                       "Marcha atrás", "Detener el vehículo", "Parar y estacionar",
                       "-Diferencia entre parar y estacionar", "-¿Dónde puedes parar",
                       "-Paradas y estacionamientos peligrosos", "-¿Dónde está prohibido parar"]),
    "T12": (301, 318, ["Ceder el paso a otros vehículos", "-Normas generales", "-Normas para ceder el paso|en lugares",
                       "-Preferencia de paso para ciclistas", "-Preferencia de paso para vehículos|en servicio",
                       "Preferencia de paso en zonas estrechas", "-Zonas estrechas con señales",
                       "-Zonas estrechas sin señales", "-Zonas estrechas en cuesta",
                       "Cruzar pasos a nivel", "Cruzar túneles", "-Normas para parar el vehículo|dentro",
                       "-Emergencias dentro de un túnel"]),
    "T13": (319, 340, ["Normas para transportar personas", "-Normas generales", "-Transportar personas",
                       "-Transportar cargas", "Medidas permitidas para vehículos y cargas",
                       "-Medidas permitidas para vehículos", "-Medidas permitidas para cargas",
                       "-Señalar la carga que sobresale", "-Operaciones de carga y descarga",
                       "Placas y señales de los vehículos"]),
    "T14": (341, 364, ["La carretera", "-Las curvas", "-Zona de la carretera en obras", "Conducir por la noche",
                       "El clima", "-Conducir con lluvia", "-Conducir con nieve", "-Conducir con hielo",
                       "-Conducir con niebla", "-Conducir con nubes de polvo", "-Conducir con mucho viento",
                       "-Conducir con calor"]),
    "T15": (365, 387, ["Sistemas del vehículo", "-Sistema de alimentación$", "-Sistema eléctrico$",
                       "-Sistema de lubricación$", "-Sistema de refrigeración$", "-Sistema de transmisión$",
                       "-Sistema de dirección$", "-Sistema de suspensión$", "-Sistema de frenado$",
                       "Revisión de ruedas y neumáticos"]),
    "T16": (388, 436, ["Evitar accidentes de tráfico", "-Factores de riesgo", "-Consecuencias de los accidentes",
                       "Personas con más riesgo", "-Peatones|Los peatones$", "-Conductores", "Actuar en caso de accidente",
                       "-Pasos a seguir", "-Regla PAS", "Primeros auxilios", "-Constantes vitales",
                       "-Conocer el estado de los heridos", "-Trasladar a los heridos"]),
    "T17": (437, 466, ["Preparar el viaje", "-Comprobaciones de seguridad", "-Elegir la ruta",
                       "Conducción preventiva", "-¿Qué es?", "-Visión", "-Anticipación", "-Controlar el espacio",
                       "Conducción eficiente", "-¿Qué es?", "-La contaminación", "-Técnicas para conducir",
                       "-¿Qué hace que se consuma", "-Distintivos ambientales"]),
    "ANEXO": (467, 474, ["¿Cuántos puntos tiene", "Perder puntos", "¿Qué faltas quitan puntos"]),
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def lineas(p):
    # las líneas con viñeta «■» son listas, nunca títulos de apartado
    return [norm(l) for l in (PAG / f"pagina_{p:03d}.txt").read_text(encoding="utf-8").splitlines()[1:]
            if not l.lstrip().startswith("■")]


def titulo_completo(pag_indice, clave, usadas):
    """Título tal como figura en la página «Índice» del tema (une las líneas partidas)."""
    crudas = [l.strip().lstrip("■").strip()
              for l in (PAG / f"pagina_{pag_indice:03d}.txt").read_text(encoding="utf-8").splitlines()[1:]]
    crudas = [l for l in crudas if l]
    for i, l in enumerate(crudas):
        if i not in usadas and norm(l).startswith(norm(clave)):
            usadas.add(i)  # dos apartados pueden empezar igual: cada línea del índice, una vez
            partes = [l]
            for sig in crudas[i + 1:]:
                if sig[0].islower() or sig[0] == "(":
                    partes.append(sig)
                else:
                    break
            return " ".join(partes)
    return clave


def pagina_dudosa(p):
    """Página que probablemente hay que leer como imagen: casi sin texto o con cifras revueltas."""
    cuerpo = [l for l in (PAG / f"pagina_{p:03d}.txt").read_text(encoding="utf-8").splitlines()[2:]
              if l.strip() and not re.fullmatch(r"\s*\d{1,3}\s*", l)]
    texto = " ".join(cuerpo)
    return len(texto.replace(" ", "")) < 120 or bool(re.search(r"\d{5,}|\d[a-záéíóú]+\d", texto))


def localizar(tid):
    ini, fin, aps = TEMAS[tid]
    desde, res, usadas = ini + 1, [], set()
    for ap in aps:
        sub = ap.startswith("-")
        # «$» al final = la línea entera debe ser el título (evita esquemas que los enumeran)
        alternativas = [(norm(a), a.endswith("$")) for a in ap.lstrip("-").split("|")]
        encontrada = None
        for p in range(desde, fin + 1):
            if any((l == a) if exacta else l.startswith(a)
                   for l in lineas(p) for a, exacta in alternativas if a):
                encontrada = p
                break
        if encontrada:
            desde = encontrada  # los apartados van en orden
        res.append((sub, titulo_completo(ini, ap.lstrip("-").split("|")[0].rstrip("$"), usadas), encontrada))
    return res


def rangos(res, fin):
    """Añade la página final de cada apartado: hasta donde empieza el siguiente del mismo nivel o superior."""
    # subapartado: acaba donde empieza el siguiente elemento; apartado: donde empieza el siguiente apartado
    out = []
    for i, (sub, tit, p) in enumerate(res):
        siguientes = [q for s, _, q in res[i + 1:] if q and (sub or not s)]
        hasta = siguientes[0] if siguientes else fin
        out.append((sub, tit, p, max(p or 0, hasta)))
    return out


def fmt(a, b):
    return f"p.{a}" if a == b else f"pp.{a}-{b}"


def markdown():
    temario = [l.strip(" *\t") for l in (PAG.parent.parent / "Temario.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    archivos = {f.name.split("_")[0]: f.name for f in (PAG.parent / "por_capitulo").glob("*.txt")}
    md = ["# Mapa temario → libro", "",
          "Generado por `python scripts/mapa_secciones.py --md`. **Páginas = página impresa del libro**",
          "(coincide con la del PDF). Cada apartado va de la página en que empieza hasta la página en",
          "que empieza el siguiente (esa última puede ser compartida). Se afina al generar cada tema.", "",
          "**Cobertura:** los 18 puntos del temario tienen capítulo propio en el libro con el mismo título.",
          "Ningún punto «sin fuente».", "",
          "**«Leer como imagen»** es una detección automática (página casi sin texto o con cifras",
          "revueltas) y solo orientativa: las señales del T8 tienen texto, pero su forma y color",
          "solo se ven en la imagen. Ante cualquier tabla o señal dudosa, rasterizar.", ""]
    for (tid, (ini, fin, _)), titulo in zip(TEMAS.items(), temario):
        clave = "anexo" if tid == "ANEXO" else f"tema{int(tid[1:]):02d}"
        md += [f"## {tid} · {titulo}", "",
               f"- Archivo: `libro_texto/por_capitulo/{archivos[clave]}`",
               f"- Páginas del libro: {ini}-{fin} (índice del tema en p.{ini})",
               "- Apartados → páginas:"]
        for sub, tit, p, hasta in rangos(localizar(tid), fin):
            donde = fmt(p, hasta) if p else "⚠️ no localizado"
            md.append(f"{'    ' if sub else '  '}- {tit} — {donde}")
        dudosas = [p for p in range(ini + 1, fin + 1) if pagina_dudosa(p)]
        if dudosas:
            md.append(f"- Leer como imagen (`scripts/rasterizar.py`): {', '.join(map(str, dudosas))}")
        if tid in NOTAS:
            md.append(f"- Notas: {NOTAS[tid]}")
        if tid in RELACIONES:
            md.append(f"- Relacionado con: {RELACIONES[tid]}")
        md.append("")
    return "\n".join(md)


# Notas que se añaden al generar cada tema (Fase 4)
NOTAS = {
    "T7": "✅ listo (`guia/tema07/sistema-de-luces.html`). Las «luces de circulación diurna» aparecen en "
          "el esquema de p.141 pero el libro no las explica: no se desarrollan.",
    "T6": "✅ listo (`guia/tema06/elementos-del-vehiculo.html`). Texto limpio.",
    "T5": "✅ listo (`guia/tema05/dispositivos-de-seguridad.html`). Tablas p.96 (fallo de frenos) y p.100 "
          "(presión) leídas en imagen: en p.100 el texto extraído ponía «la rueda se reviente» en la "
          "columna equivocada (va con presión BAJA). El libro llama al frenado autónomo «AES» (p.93) y "
          "«AEB» (p.94): señalado en la guía.",
    "T4": "✅ listo (`guia/tema04/obligaciones-conductores-peatones.html`). Texto limpio; la tabla "
          "de p.78 (conducción defensiva / zona de inseguridad) se entiende sin imagen.",
    "T2": "✅ listo (`guia/tema02/documentacion.html`). Tablas de permisos (p.29-30) e ITV (p.35-36) "
          "transcritas desde la imagen: el texto extraído las mezcla.",
    "T1": "✅ listo (`guia/tema01/definiciones.html`). El libro nombra sin definir el trolebús (p.9) y "
          "la bicicleta de pedales con motor (p.21, 23): marcados ⚠️ en la guía, sin rellenar. "
          "Tabla M/N/O (p.25) y p.23 comprobadas en imagen.",
    "T3": "✅ listo (`guia/tema03/estado-del-conductor.html`). Tablas leídas en imagen: p.59 (drogas) "
          "y p.64 (enfermedades); el texto de pdftotext las mezcla. p.69 tiene una errata en el libro "
          "(«Ditracciones»). Contenido de los «Ver vídeo» no disponible.",
}


# Relaciones entre temas, orientativas, deducidas de los títulos de los apartados (afinar al generar cada tema)
RELACIONES = {
    "T1": "T2 (tipos de permiso según el vehículo), T13 (medidas y cargas)",
    "T2": "ANEXO (permiso por puntos), T15 (ITV y mantenimiento)",
    "T3": "T14 (fatiga y somnolencia al conducir de noche), T16 (factores de riesgo)",
    "T4": "T9 (por dónde circulan peatones y vehículos), T12 (preferencia de peatones y animales)",
    "T5": "T7 (sistemas de alumbrado), T15 (frenos, ruedas y neumáticos)",
    "T6": "T5 (seguridad activa), T17 (preparar el viaje)",
    "T7": "T5 (sistemas de alumbrado), T14 (conducir de noche y con niebla)",
    "T8": "T9 (colores y carriles), T10 (señales de velocidad), T12 (señales de preferencia)",
    "T9": "T8 (líneas y marcas), T11 (maniobras en carriles), T12 (túneles)",
    "T10": "T3 (tiempo de reacción), T14 (curvas y clima), T17 (controlar el espacio)",
    "T11": "T7 (luz indicadora de dirección), T9 (uso de los carriles)",
    "T12": "T8 (señales de preferencia), T11 (incorporaciones)",
    "T13": "T1 (tipos de vehículos), T7 (señalizar la carga)",
    "T14": "T3 (estado del conductor), T7 (luces), T10 (velocidad y distancias)",
    "T15": "T5 (frenos y ruedas), T17 (comprobaciones antes del viaje)",
    "T16": "T3 (factores del conductor), T5 (seguridad pasiva), T9 (emergencias en autopista)",
    "T17": "T10 (distancias), T15 (mantenimiento)",
    "ANEXO": "T2 (permiso de conducir por puntos)",
}


def main():
    import sys
    if "--md" in sys.argv:
        destino = PAG.parent.parent / "MAPA_TEMARIO_LIBRO.md"
        destino.write_text(markdown() + "\n", encoding="utf-8")
        print(destino.name, "generado")
        return
    for tid in TEMAS:
        print(f"== {tid}")
        for sub, tit, p in localizar(tid):
            print(f"  {p or '?':>4}  {'  ' if sub else ''}{tit}")


if __name__ == "__main__":
    main()
