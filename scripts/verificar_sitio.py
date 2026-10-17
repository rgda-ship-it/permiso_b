"""Verificación del sitio en navegador sin interfaz (Playwright + Chromium).

Uso:  python scripts/verificar_sitio.py        → capturas en capturas/ (no se versiona)

Abre cada página con file:// (sin servidor) a 1280 px y 390 px y comprueba:
errores de JS, scroll horizontal, menú ① ② ③ ④ con el paso actual marcado,
panel lateral, anterior/siguiente, índice «En esta página», examen tipo,
modo oscuro guardado tras recargar y botón ☰ en móvil.

Abre también los temas reales marcados «listo» en temario-nav.js.
Mientras no haya temas listos, prueba las páginas de tema sobre una COPIA del
sitio en una carpeta temporal: copia la plantilla en T2, T3 y T4 y los marca
«listo» solo en esa copia. El sitio real no se toca.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
GUIA = RAIZ / "guia"
CAPTURAS = RAIZ / "capturas"
TAMANOS = {"escritorio": (1280, 900), "movil": (390, 844)}
fallos = []


def comprobar(cond, msg):
    print(("  ok   " if cond else "  FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def preparar_copia():
    tmp = Path(tempfile.mkdtemp(prefix="guia_prueba_")) / "guia"
    shutil.copytree(GUIA, tmp)
    nav = (tmp / "js" / "temario-nav.js").read_text(encoding="utf-8")
    plantilla = (RAIZ / "scripts" / "plantillas" / "tema.html").read_text(encoding="utf-8")
    for tid in ("T2", "T3", "T4"):
        m = re.search(r'id: "%s",.*?archivo: "([^"]+)", estado: "[^"]+"' % tid, nav)
        archivo = m.group(1)
        if not (tmp / archivo).exists():  # si el tema ya existe de verdad, se usa ese
            (tmp / archivo).parent.mkdir(parents=True, exist_ok=True)
            (tmp / archivo).write_text(plantilla.replace("{TN}", tid), encoding="utf-8")
        nav = nav.replace(m.group(0), m.group(0).rsplit('estado: "', 1)[0] + 'estado: "listo"')
    (tmp / "js" / "temario-nav.js").write_text(nav, encoding="utf-8")
    tema = re.search(r'id: "T3",.*?archivo: "([^"]+)"', nav).group(1)
    return tmp, tema


def revisar(page, url, nombre, tam, paso):
    errores = []
    page.on("pageerror", lambda e: errores.append(str(e)))
    page.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    page.goto(url)
    page.wait_for_load_state("load")
    page.wait_for_selector(".ciclo")
    page.screenshot(path=str(CAPTURAS / f"{nombre}_{tam}.png"), full_page=True)
    js_err = [e for e in errores if "fonts.g" not in e]  # sin conexión, la fuente puede fallar
    comprobar(not js_err, f"{nombre} [{tam}] sin errores de JS {js_err or ''}")
    ancho = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    comprobar(ancho[0] <= ancho[1], f"{nombre} [{tam}] sin scroll horizontal ({ancho[0]} ≤ {ancho[1]})")
    actual = page.locator('.ciclo__paso[aria-current="page"]').inner_text()
    comprobar(paso in actual, f"{nombre} [{tam}] menú marca «{paso}» (marca «{actual.strip()}»)")
    comprobar(page.locator(".ciclo__paso").count() == 4, f"{nombre} [{tam}] menú con 4 pasos")


def main():
    CAPTURAS.mkdir(exist_ok=True)
    copia, tema = preparar_copia()
    paginas = [
        ("portada", GUIA / "index.html", "Índice"),
        ("guia", GUIA / "esencial" / "index.html", "Guía"),
        ("juegos", GUIA / "juegos" / "index.html", "Juegos"),
        ("examen", GUIA / "simulador" / "index.html", "Examen"),
        ("tema_prueba", copia / tema, "Índice"),
    ]
    # los 18 temas reales
    nav_js = (GUIA / "js" / "temario-nav.js").read_text(encoding="utf-8")
    for tid, archivo in re.findall(r'id: "([^"]+)",.*?archivo: "([^"]+)", estado: "listo"', nav_js):
        paginas.append((tid.lower(), GUIA / archivo, "Índice"))
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for tam, (w, h) in TAMANOS.items():
            print(f"\n== {tam} ({w} px)")
            for nombre, ruta, paso in paginas:
                ctx = nav.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()
                revisar(page, ruta.as_uri(), nombre, tam, paso)
                ctx.close()

        print("\n== funciones")
        ctx = nav.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.goto((GUIA / "index.html").as_uri())
        page.wait_for_selector("#indice-temario li")
        comprobar(page.locator("#indice-temario li").count() == 18, "portada: 18 temas en el índice")
        listos = (GUIA / "js" / "temario-nav.js").read_text(encoding="utf-8").count('estado: "listo"')
        comprobar(f"{listos} de 18" in page.locator("#progreso").inner_text(), f"portada: progreso «{listos} de 18»")
        comprobar(page.locator("#sidebar-index").count() == 0 and page.locator("#btn-indice").count() == 0,
                  "portada: sin panel lateral ni ☰ (el índice ya está en el centro)")

        # modo oscuro: cambiar, recargar y comprobar que se mantiene
        page.click("#btn-tema")
        tema_antes = page.evaluate("document.documentElement.dataset.theme")
        page.reload()
        page.wait_for_selector(".ciclo")
        comprobar(page.evaluate("document.documentElement.dataset.theme") == tema_antes,
                  f"modo «{tema_antes}» se mantiene al recargar")
        page.screenshot(path=str(CAPTURAS / f"portada_{tema_antes}.png"), full_page=False)

        # página de tema (copia)
        page.goto((copia / tema).as_uri())
        page.wait_for_selector("#page-nav a")
        comprobar(page.locator("#sidebar-index li").count() == 18, "tema: panel lateral con 18 temas")
        comprobar(page.locator('#sidebar-index a[aria-current="page"]').count() == 1, "tema: resaltado en el panel lateral")
        textos = page.locator("#page-nav a").all_inner_texts()
        comprobar(len(textos) == 2 and "Tema 2" in textos[0] and "Tema 4" in textos[1],
                  f"tema: anterior=T2 y siguiente=T4 ({[t.splitlines()[-1] for t in textos]})")
        comprobar(page.locator("#toc a").count() >= 4, f"tema: «En esta página» con {page.locator('#toc a').count()} entradas")
        comprobar(page.locator(".opciones .letra").first.inner_text() == "a)", "tema: opciones con letras a), b), c)")
        page.locator(".quiz-question .opciones button").first.click()
        comprobar("1 respondidas" in page.locator("[data-marcador]").inner_text(), "tema: el marcador cuenta la respuesta")
        comprobar(page.locator(".quiz-question .correcta").count() == 1, "tema: marca la opción correcta")
        comprobar(page.locator(".justificacion").first.is_visible(), "tema: muestra la justificación")
        ctx.close()

        # ② Guía esencial: datos, búsqueda sin tildes, filtros, «Ya me lo sé» y tapar
        ctx = nav.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.goto((GUIA / "esencial" / "index.html").as_uri())
        page.wait_for_selector(".es-tema")
        comprobar(page.locator(".es-tema").count() == 18, "esencial: 18 temas")
        n_mem = page.evaluate("ESENCIAL.temas.reduce(function (s, t) { return s + t.memorizar.length; }, 0)")
        comprobar(page.locator("[data-glosa]").count() == n_mem, f"esencial: glosario con {n_mem} términos")
        page.fill("#es-buscar", "vehiculo")
        comprobar(page.locator("#vista-temas mark").count() > 0, "esencial: «vehiculo» encuentra «vehículo» (sin tildes)")
        page.fill("#es-buscar", "")
        page.select_option("#es-tema", "T10")
        comprobar(page.locator(".es-tema:not([hidden])").count() == 1, "esencial: el filtro deja un solo tema")
        page.select_option("#es-tema", "")
        page.check("#es-solo-rojo")
        comprobar(not page.locator('#es-T3 [data-bloque="dominar"]').is_visible(), "esencial: «Solo 🔴» oculta los 🟠")
        page.uncheck("#es-solo-rojo")
        page.check("#es-tapar")
        comprobar(page.evaluate("document.querySelector('main').classList.contains('tapar')"), "esencial: «Tapar definiciones»")
        page.uncheck("#es-tapar")
        page.locator(".es-tema[open] .es-item input[type=checkbox]").first.check()
        page.reload()
        page.wait_for_selector(".es-tema")
        comprobar(page.locator(".es-item.sabido").count() == 1, "esencial: «Ya me lo sé» se mantiene al recargar")
        ctx.close()

        # ③ Juegos: cada juego se puede jugar hasta el final
        ctx = nav.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        errores_js = []
        page.on("pageerror", lambda e: errores_js.append(str(e)))
        page.goto((GUIA / "juegos" / "index.html").as_uri())
        page.wait_for_selector(".ju-carta")
        comprobar(page.locator(".ju-carta").count() == 6, "juegos: 6 juegos")
        acciones = {"quien": "[data-op]", "mitos": "[data-mr]", "situaciones": "[data-op]",
                    "secuencias": "[data-paso]:not([disabled])"}
        for juego, sel in acciones.items():
            page.click(f'[data-juego="{juego}"]')
            comprobar(not page.locator("#ju-menu").is_visible(), f"juegos: {juego} oculta el menú de juegos")
            for _ in range(80):
                if page.locator("[data-otra]").count():
                    break
                if page.locator("[data-siguiente]").count():
                    page.click("[data-siguiente]")
                else:
                    page.locator(sel).first.click()
            comprobar("Has acertado" in page.locator("#ju-juego").inner_text(), f"juegos: {juego} llega al resultado")
            page.click("[data-volver]")
        page.click('[data-juego="parejas"]')
        for i in range(5):
            if page.locator(f'[data-lado="c"][data-i="{i}"]:not([disabled])').count():
                page.click(f'[data-lado="c"][data-i="{i}"]')
                page.click(f'[data-lado="v"][data-i="{i}"]')
        comprobar("0 errores" in page.locator("#ju-juego").inner_text(), "juegos: parejas unidas sin errores")
        page.click("[data-volver]")
        page.click('[data-juego="pasapalabra"]')
        n = page.locator(".ju-rosco li").count()
        page.click("[data-pasapalabra]")
        page.fill("#ju-palabra", "zzz")
        page.press("#ju-palabra", "Enter")
        comprobar(n >= 20 and page.locator(".ju-rosco li.fallo").count() == 1,
                  f"juegos: pasapalabra con {n} letras corrige la respuesta")
        page.click("[data-rendirse]")
        comprobar("Has acertado 0 de" in page.locator("#ju-juego").inner_text(), "juegos: pasapalabra termina")
        sw = page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        comprobar(sw and not errores_js, f"juegos: sin scroll horizontal ni errores de JS {errores_js or ''}")
        ctx.close()

        # ④ Examen: hacer un examen, corregir, repetir fallos, historial y fin por tiempo
        ctx = nav.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        errores_js = []
        page.on("pageerror", lambda e: errores_js.append(str(e)))
        page.on("dialog", lambda d: d.accept())
        page.clock.install()
        page.goto((GUIA / "simulador" / "index.html").as_uri())
        page.wait_for_selector("#si-temas input")
        n_total = page.evaluate("SIMULADOR.preguntas.length")
        comprobar(n_total >= 18 * 18 and f"({n_total} preguntas)" in page.inner_text("#si-disponibles"),
                  f"examen: {n_total} preguntas disponibles")
        page.click("#si-ninguno")
        comprobar(page.is_disabled("#si-empezar"), "examen: sin temas no se puede empezar")
        page.click("#si-todos")
        page.check('input[name="n"][value="10"]')
        page.check('input[name="reloj"][value="0"]')
        page.click("#si-empezar")
        comprobar(page.locator("#si-mapa button").count() == 10, "examen: 10 preguntas")
        for _ in range(9):
            page.locator("#si-pregunta [data-op]").first.click()
            page.click("#si-siguiente")
        page.keyboard.press("b")
        comprobar("10 respondidas" in page.inner_text("#si-contador"), "examen: cuenta las respondidas (también con el teclado)")
        page.click("#si-terminar")
        res = page.inner_text("#si-resultado")
        bien = int(re.search(r"(\d+) de 10", res).group(1))
        comprobar(page.locator("#si-revision > li").count() == 10, f"examen: corrección con 10 preguntas ({bien} bien)")
        comprobar(page.locator("#si-revision .si-explica .ref").count() == 10, "examen: cada corrección cita la página")
        if bien < 10:
            page.click("#si-repetir")
            comprobar(page.locator("#si-mapa button").count() == 10 - bien, "examen: «Repetir las que no acertaste»")
        page.reload()
        page.wait_for_selector("#si-temas input")
        comprobar(page.locator("#si-historial li").count() >= 1, "examen: el historial se guarda al recargar")
        page.check('input[name="n"][value="10"]')
        page.check('input[name="reloj"][value="1"]')
        page.click("#si-empezar")
        comprobar("10:00" in page.inner_text("#si-reloj"), "examen: cronómetro de 10 minutos")
        page.clock.run_for("10:05")
        comprobar("Se acabó el tiempo" in page.inner_text("#si-resultado"), "examen: corrige solo al acabar el tiempo")
        sw = page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        comprobar(sw and not errores_js, f"examen: sin scroll horizontal ni errores de JS {errores_js or ''}")
        page.screenshot(path=str(CAPTURAS / "examen_resultado_movil.png"), full_page=False)
        ctx.close()

        # móvil: botón ☰ abre y Escape cierra el panel
        ctx = nav.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto((copia / tema).as_uri())
        page.wait_for_selector("#btn-indice")
        comprobar(not page.locator("#sidebar-index").is_visible() or
                  page.evaluate("document.getElementById('sidebar-index').getBoundingClientRect().right <= 0"),
                  "móvil: panel lateral oculto al entrar")
        page.click("#btn-indice")
        page.wait_for_timeout(300)
        comprobar(page.evaluate("document.getElementById('sidebar-index').getBoundingClientRect().left >= 0"),
                  "móvil: ☰ abre el panel lateral")
        page.screenshot(path=str(CAPTURAS / "tema_prueba_movil_indice.png"))
        page.keyboard.press("Escape")
        comprobar(not page.evaluate("document.body.classList.contains('indice-abierto')"), "móvil: Escape cierra el panel")
        ctx.close()
        nav.close()

    shutil.rmtree(copia.parent, ignore_errors=True)
    print(f"\n{'TODO CORRECTO' if not fallos else f'{len(fallos)} FALLOS'} · capturas en {CAPTURAS.relative_to(RAIZ)}/")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
