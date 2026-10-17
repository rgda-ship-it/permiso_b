# Progreso de la guía

Estados: `pendiente` · `listo` · `sin fuente` · `lectura completa, generación pendiente`

| Id | Tema (título exacto del temario) | Páginas | Estado | Notas |
|---|---|---|---|---|
| T1 | Tema 1. Definiciones | 5-25 | listo | 101 refs · 14 autoev. · 7 no confundir · 18 examen (6-6-6) · trolebús y bici con motor sin definir en el libro (⚠️) |
| T2 | Tema 2. Documentación | 26-41 | listo | tablas p.29-30 y 35-36 en imagen |
| T3 | Tema 3. El estado del conductor | 42-73 | listo | piloto · 128 refs · 14 autoevaluación · 7 no confundir · 18 examen (a/b/c 6-6-6) · tablas p.59 y p.64 en imagen |
| T4 | Tema 4. Obligaciones de conductores y peatones | 74-85 | listo | |
| T5 | Tema 5. Dispositivos de seguridad en el vehículo | 86-119 | listo | tablas p.96 y p.100 en imagen; AES/AEB incoherente en el libro |
| T6 | Tema 6. Elementos del vehículo y normas para usarlos | 120-138 | listo | |
| T7 | Tema 7. Sistema de luces de los vehículos | 139-153 | listo | luz de circulación diurna sin explicar en el libro |
| T8 | Tema 8. Señales de circulación | 154-211 | listo | 7 tablas leídas en imagen (p.157-164); señales en tablas por código |
| T9 | Tema 9. La vía | 212-242 | listo | tablas p.220, 226, 229, 234 en imagen |
| T10 | Tema 10. Velocidad y distancias | 243-266 | listo | tablas p.244, 252-258 en imagen; frase confusa p.262 señalada |
| T11 | Tema 11. Maniobras | 267-300 | listo | tablas p.270, 277, 292 en imagen |
| T12 | Tema 12. Normas de preferencia para circular | 301-318 | listo | |
| T13 | Tema 13. Transportar personas y cargas | 319-340 | listo | tablas p.328, 330 en imagen |
| T14 | Tema 14. Conducir de forma segura | 341-364 | listo | tabla p.345 en imagen |
| T15 | Tema 15. Mecánica y mantenimiento del vehículo | 365-387 | listo | p.373 y 380 en imagen |
| T16 | Tema 16. Accidentes de tráfico | 388-436 | listo | tablas p.390, 408, 410, 425, 427 en imagen |
| T17 | Tema 17. Conducción preventiva y eficiente | 437-466 | listo | p.463 en imagen |
| ANEXO | Anexo puntos. El permiso de conducir por puntos | 467-474 | listo | |

**Resumen:** 18 de 18 temas listos. Fase 4 completa.

## Fase 5 — Fichas de resumen

18 fichas en `guia/resumen/` con el esquema fijo. **342 unidades clave** (mapa + cifras + no confundir). Verificadas con `scripts/verificar_fichas.py`: esquema, números presentes en la guía y páginas dentro del rango.

## Fase 6 — Guía esencial

`guia/esencial/` generado por `scripts/generar_esencial.py` a partir de las fichas y de `scripts/esencial/temaNN.json`.

- 18 temas · **136 definiciones 🔴** (5-8 por tema) · **86 conceptos 🟠** · 36 reglas 🧠 · conexiones 🔗 entre temas.
- Cobertura del «Mapa del punto» por los 🟠: **143/143**.
- Cada definición y concepto lleva fragmentos literales comprobados en la página del tema y su página del libro contrastada con las referencias cercanas: 0 avisos.
- Tablas 📋, cifras 🔢 y trampas ⚠️ salen automáticamente de las fichas.
- Sin «Así lo preguntan» ni prioridad 🔥: no hay exámenes anteriores en el material.
- Verificado con `scripts/verificar_sitio.py` (búsqueda sin tildes, filtro por tema, Solo 🔴, Tapar, «Ya me lo sé» tras recargar; 1280 y 390 px).

## Fase 7 — Juegos

`guia/juegos/` con 6 juegos, filtro por tema, explicación y página del libro después de cada respuesta.

| Juego | Origen | Cantidad |
|---|---|---|
| Pasapalabra | definiciones 🔴 de la Guía (términos de hasta 3 palabras) | 23 letras con «Todos los temas» |
| ¿Quién soy? | definiciones 🔴 de la Guía | 136 |
| Parejas de cifras | «Cifras que caen» de las fichas | 109 |
| ¿Mito o realidad? | `scripts/juegos/temaNN.json` | 112 (56 mitos / 56 realidades) |
| Situaciones al volante | `scripts/juegos/temaNN.json` | 61 (correcta en a/b/c = 19/25/17; nunca la más larga) |
| Secuencias | `scripts/juegos/temaNN.json` | 17 |

- Todo lo redactado lleva fragmentos literales comprobados en la página del tema: 0 errores, 0 avisos. Prueba de mutación: cambiar «izquierda» por «derecha» detiene el generador.
- En pantalla las opciones se barajan en cada partida.
- Verificado con `scripts/verificar_sitio.py`: cada juego llega al resultado a 390 px, sin errores de JS ni scroll horizontal.

## Fase 8 — Examen

`guia/simulador/index.html`, generado por `scripts/generar_simulador.py` desde `scripts/plantillas/simulador.html` (las preguntas van dentro: funciona sin servidor).

- **324 preguntas** (las 18 del «Examen tipo» de cada tema). 0 de estilo examen: no hay exámenes anteriores en el material; el script acepta `scripts/simulador/preguntas_estilo_examen.json` si se redactan.
- Correcta en a/b/c = 108/108/108 tal como están escritas; la más larga en 79 de 324 (24 %, por debajo del 33 % del azar). En pantalla las opciones se barajan en cada intento: 0 opciones fijas («todas/ninguna de las anteriores»).
- Simulacro: 10, 20, 30 o todas; temas a elegir; cronómetro de 1 minuto por pregunta o sin tiempo; una pregunta por pantalla con mapa para saltar y teclas a/b/c y flechas.
- Corrección: nota, fallos y sin responder, desglose por tema, revisión con la explicación, la página del libro y el enlace al tema, «Ver solo los fallos», «Repetir las que no acertaste» e historial de los 10 últimos (en el navegador).
- No dice «apto / no apto»: el libro no da el número de preguntas ni de fallos del examen oficial.
- Verificado con `scripts/verificar_sitio.py` (examen completo, corrección, repetir, historial tras recargar y fin por tiempo con reloj simulado; 390 px).

## Fase 9 — Verificación y cierre

| Comprobación | Resultado |
|---|---|
| Navegador (`verificar_sitio.py`): portada, Guía, Juegos, Examen y los 18 temas, a 1280 y 390 px | 230 comprobaciones, 0 fallos: sin errores de JS ni scroll horizontal |
| Interacción | buscar, filtrar, marcar y recargar (persiste), tapar, jugar cada juego hasta el final, examen completo, repetir fallos, historial y fin por tiempo |
| Imprimir a PDF | Guía esencial: 59 páginas con los 18 temas (se abren todos), sin el menú |
| Enlaces internos (`verificar_enlaces.py`) | 22 páginas, 119 enlaces, 0 rotos |
| Fichas (`verificar_fichas.py`) | 342 unidades clave, 0 errores |
| Guía esencial | 136 definiciones (5-8 por tema), 86 conceptos, Mapa del punto cubierto 143/143 |
| Examen tipo | 324 preguntas, todas con 3 opciones y una correcta; a/b/c 108/108/108; la más larga 79 (24 %) y la más corta 74 (23 %); ningún tema pasa de 7/18 |
| Autoevaluación | 252 preguntas, todas con respuesta |
| Mito o realidad | 56 mitos / 56 realidades |
| Respuestas que citan letras de opción | 0 |
| Contradicciones entre temas | explicadas en la guía: tiempo de reacción (T3/T10), temperatura (T3/T14/T17), luz de peligro naranja o amarilla (T11/T13), puntos por alcohol (T3/Anexo), AES/AEB (T5) y, nueva, color del chaleco (T11/T16) |

Cambios de esta fase:
- T12: la correcta era la opción más corta en 10 de 18 preguntas (patrón al revés). Se ajustó la longitud de 6 preguntas, sin cambiar su contenido: ahora 6 de 18. `medir_patrones.py` mide también «la más corta».
- T16: nota sobre el color del chaleco (el libro dice «amarillos» en p.293 y «amarillo, naranja o rojo» en p.417).
- Nuevo `scripts/verificar_enlaces.py`; `verificar_sitio.py` abre los 18 temas reales.

Pendiente (opcional): preguntas «estilo examen» extra (no hay exámenes anteriores) y modo «apto / no apto» del Examen (el libro no da el criterio oficial).

