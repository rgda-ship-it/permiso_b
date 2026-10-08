# Método: crear una guía de estudio web a partir de un PDF

> Plantilla reutilizable, sacada de cómo se construyó la guía de *Materiales Dentales*
> (Phillips 13.ª ed.) en el repo `materiales_dentales`.
> Sirve para cualquier asignatura con **un libro en PDF** y **un temario oficial**.
>
> **Cómo usarlo:** copia este archivo a la carpeta del proyecto nuevo, rellena la
> sección 1 y pásaselo a Claude con el prompt de la fase que toque (sección 13).
> Trabaja **una fase cada vez** y revisa el resultado antes de pasar a la siguiente.

---

## 0. Qué se obtiene al final

Un sitio web estático (HTML + CSS + JS, sin servidor) con un **ciclo de estudio en 4 pasos**,
que aparece como menú numerado en todas las páginas:

| Paso | Sección | Para qué sirve | Carpeta |
|---|---|---|---|
| ① | **Índice** | Leer el contenido completo de cada tema | `index.html` + `bloqueN/*.html` |
| ② | **Guía** | Aprender lo esencial: qué memorizar y qué entender | `esencial/` |
| ③ | **Juegos** | Repasar jugando | `juegos/` |
| ④ | **Examen** | Simulacros con corrección | `simulador/` |

Más una capa interna de **fichas de resumen** en Markdown (`resumen/bloqueN.md`) que
alimenta automáticamente la Guía y los Juegos.

**Regla de diseño del ciclo:** cada paso es una sección separada. No se mezcla lo
esencial dentro del contenido (nada de estrellas, avisos o atajos a la Guía dentro de
los temas). Si se mezclan, el alumno se aburre y se le pasa lo esencial.

```
proyecto/
├── CLAUDE.md                     ← instrucciones permanentes para Claude
├── temario.txt                   ← temario oficial, orden canónico
├── MAPA_TEMARIO_LIBRO.md         ← tema → capítulo → páginas del libro
├── PROGRESO_GUIA.md              ← estado de cada tema
├── libro.pdf
├── libro_texto/
│   ├── paginas/pagina_NNN.txt
│   ├── por_capitulo/capNN_*.txt
│   └── libro_completo.txt
├── scripts/
│   ├── extraer_texto.sh          ← PDF → texto (pdftotext u OCR)
│   ├── extraer_resumen.py        ← HTML de tema → extracto pequeño
│   ├── generar_esencial.py       ← fichas + datos curados → esencial/datos.js
│   ├── verificar_esencial.py     ← mide patrones y contradicciones
│   ├── generar_juegos.py         ← fichas → juegos/fichas.js
│   ├── generar_simulador.py      ← Fase 4 de cada tema → simulador/index.html
│   └── esencial/bloqueN.json     ← datos curados a mano para la Guía
└── guia/
    ├── index.html                ← portada + índice del temario
    ├── css/style.css
    ├── js/main.js
    ├── js/temario-nav.js         ← array del temario, panel lateral, anterior/siguiente
    ├── js/menu.js                ← menú común ① ② ③ ④
    ├── bloque1/ … bloqueN/       ← un HTML por tema (4 fases)
    ├── resumen/bloqueN.md        ← fichas de repaso
    ├── esencial/index.html + datos.js
    ├── juegos/index.html + datos.js + fichas.js
    └── simulador/index.html (+ plantilla.html + preguntas_estilo_examen.json)
```

---

## 1. Datos del proyecto (rellenar antes de empezar)

```text
ASIGNATURA ............ {Permiso de Conducir Clase B (Educación Vial / Legislación de Tráfico)}
LIBRO / EDICIÓN ....... {anual del Permiso B en Lectura Fácil, María Peralta y Laia Vidal (Adaptación), Dirección General de Tráfico / ETRASA, 1ª Edición Corregida Octubre 2024}
PDF ................... {Libro.pdf}
¿PDF CON TEXTO? ....... {sí → pdftotext}
IDIOMA DEL LIBRO ...... {es}
IDIOMA DE LA GUÍA ..... {es}
TEMARIO OFICIAL ....... {Temario.txt}
EXÁMENES ANTERIORES ... {«no hay»}
REPO / RAMA BASE ...... {https://github.com/rgda-ship-it/permiso_b}
DESPLIEGUE ............ {Cloudflare Pages}
PÚBLICO ............... {Estudiantes que preparan la prueba teórica del permiso de conducir clase B a través de materiales adaptados bajo la norma UNE de Lectura Fácil.}
```
---

## 2. Reglas que no se negocian

1. **Fuente única.** Todo el contenido sale del libro. No se inventa nada ni se rellena con
   conocimiento general. Si el temario pide algo que el libro no trata, se escribe
   `⚠️ No cubierto en {LIBRO}` y se marca el tema como «sin fuente».
2. **Cada afirmación lleva su página**, la **impresa en el libro**, no la del PDF.
   El desfase PDF↔libro **no suele ser constante** (páginas sin numerar al inicio de cada
   sección). Se comprueba en la cabecera o el pie de la página, nunca se calcula con una resta fija.
3. **Sintetizar, no copiar.** Si el libro está en otro idioma, se traduce fielmente
   mientras se sintetiza; nunca se pega texto del original.
4. **Única excepción a «no inventar»:** el bloque `faq-simple` de la Fase 3 (analogía y ejemplo).
   Puede ser formulación propia si no contradice al libro y se presenta como recurso
   pedagógico («Para visualizarlo: …»), sin número de página.
5. **Las capas superiores se alimentan de la de abajo, nunca del libro.** Fichas ← guía;
   Guía esencial, juegos y simulador ← guía y fichas. Una vez validada la guía, no se
   vuelve al PDF.
6. **Despliegue estático.** Todo lo publicado es HTML, CSS y JS que corre en el navegador.
   Python solo se usa sin conexión, en local, para **generar** archivos estáticos.
   Cada página debe abrirse también con doble clic (`file://`), sin servidor.
7. **Los títulos de los temas coinciden exactamente con los del temario oficial.**
8. **Exámenes anteriores:** se usan solo para saber **qué** se pregunta y **cómo**
   (estilo, formato, frecuencia). **Nunca como fuente de contenido.**

---

## 3. Disciplina de tokens (lo que hace viable un libro de 400-600 páginas)

- El PDF se convierte a texto **una sola vez** (fase 1). Después, Claude lee texto, no el PDF.
- Antes de escribir un tema se consulta `MAPA_TEMARIO_LIBRO.md` y se lee **solo** el
  capítulo y las páginas de ese tema. **Nunca lectura exploratoria.**
- En capítulos largos, primero se localiza la sección con `grep` y después se lee ese rango.
- Solo se rasteriza una página del PDF (`pdftoppm -r 150`) cuando hay una figura con datos
  (ejes, curvas) que el texto no describe.
- Si a mitad de un tema se acaba el contexto, se guarda `notas_bloqueX_puntoY.md` con los
  datos clave y se marca en `PROGRESO_GUIA.md` «lectura completa, generación pendiente».
- Para las capas superiores (fichas, Guía): se trabaja desde **extractos** de unos 2-4k
  tokens generados por script, no desde el HTML completo (60-100k tokens por tema). El HTML
  solo se abre con `sed -n` sobre un rango o con búsquedas puntuales.
- **Un tema por sesión**, con sus 4 fases completas. Actualizar `PROGRESO_GUIA.md` al terminar cada uno.

---

## 4. Fase 0 — Preparar el proyecto

1. Crear el repo y la rama base `develop`. Trabajo siempre en `feature/<nombre>` desde `develop`.
2. Guardar el temario en `temario.txt`: bloques y puntos, en el orden oficial, con el
   título exacto. Es la **única fuente de verdad del orden**.
3. Crear `CLAUDE.md` con: qué es el proyecto, la tarea activa, las reglas de la sección 2,
   las rutas de la sección 0 y el flujo de git (sección 11).
4. Crear `PROGRESO_GUIA.md`: una fila por tema con estado (`pendiente` / `listo` /
   `sin fuente`), rango de páginas y notas.

---

## 5. Fase 1 — PDF a texto

**PDF con texto seleccionable** (lo normal en libros recientes):

```bash
# requiere poppler-utils (pdftotext, pdfinfo)
TOTAL=$(pdfinfo libro.pdf | awk '/Pages:/{print $2}')
mkdir -p libro_texto/paginas libro_texto/por_capitulo
for P in $(seq 1 $TOTAL); do
  { echo "--- PÁGINA PDF $P ---"; pdftotext -f $P -l $P -layout libro.pdf -; } \
    > libro_texto/paginas/pagina_$(printf %03d $P).txt
done
ls -v libro_texto/paginas/*.txt | xargs cat > libro_texto/libro_completo.txt
```

Después se trocea por capítulos con un array de rangos de **páginas PDF**
(`["cap01_titulo"]="18:30"`), localizados buscando la cabecera real de cada capítulo
(`grep -n "CHAPTER 5" libro_texto/libro_completo.txt`).

**PDF escaneado:** igual, pero cada página pasa por `pdftoppm -r 300` y luego por
`tesseract -l spa` (o el idioma que toque). Calidad esperada: cuerpo de texto ~95 %;
fórmulas, tablas y pies de figura, peor. Esas páginas se revisan con la imagen.

**Comprobar:** abrir 3-4 páginas al azar, una con tabla, y anotar en `CLAUDE.md` cómo se
encuentra la página impresa (p. ej. «el número va en la cabecera junto al título del capítulo»).

---

## 6. Fase 2 — Mapa temario → libro

`MAPA_TEMARIO_LIBRO.md`, una sección por tema:

```markdown
## II.4 · Hidrocoloides
- Capítulo: 13 (Auxiliary materials) · archivo: por_capitulo/cap13_auxiliary_materials.txt
- Páginas del libro: 287-295 (PDF 312-320)
- Subapartados del temario → páginas: agar 287-290 · alginato 290-292 · propiedades 292-294
- Relacionado con: II.1 (clasificación), II.2 (yeso)
```

Se arranca grueso, a partir de los títulos de los capítulos, y **se afina con las páginas
exactas cada vez que se genera un tema**. Si un punto del temario no aparece en el libro,
se apunta aquí como «sin fuente» antes de escribir nada.

---

## 7. Fase 3 — Esqueleto del sitio (una sola vez)

- **`css/style.css`**: variables en `:root` (paleta, radios, sombras); tipografías
  *Source Serif 4* (texto) y *DM Sans* (interfaz); modo oscuro con
  `prefers-color-scheme` más un botón 🌓 guardado en localStorage dentro de `try/catch`;
  móvil primero, sin scroll horizontal a 390 px; estilos de impresión.
- **`js/temario-nav.js`**:
  - un array plano `TEMARIO = [{bloque, numero, titulo, archivo, estado}]` en el orden de `temario.txt`;
  - genera el **panel lateral** (índice por bloques, tema actual resaltado y botón ☰ en móvil);
  - la navegación **anterior/siguiente** al pie;
  - el índice «En esta página» (h2/h3 con scroll-spy);
  - el índice general de la portada con el estado de cada tema.
  - El HTML de cada tema solo lleva contenedores vacíos (`<aside id="sidebar-index">`,
    `<nav id="page-nav">`) y `<body data-temario="II.4">`. Así, corregir un título no obliga a tocar 34 archivos.
- **`js/menu.js`**: el menú común ① Índice · ② Guía · ③ Juegos · ④ Examen, con el paso
  actual resaltado. Calcula las rutas desde la propia ubicación del script, de modo que
  funcione igual desplegado que con `file://`. Lo carga `temario-nav.js` en portada y temas,
  y las demás secciones lo incluyen con `<script src="../js/menu.js">`.
- **Portada**: presentación, progreso («N de M temas»), un párrafo «Cómo estudiar con esta
  guía» con los 4 pasos y el índice del temario.

---

## 8. Fase 4 — Los temas, en 4 fases

Un HTML por punto del temario, en `bloqueN/N-slug.html`. **Empezar por un tema piloto**,
revisarlo y solo entonces seguir con el resto, uno por sesión.

### Fase 1 — Resumen de contenido
- Abre con una tarjeta «**Mapa del punto**» (5-8 líneas con el esqueleto del tema).
  Es la semilla de las fichas: no te la saltes.
- Secciones con los títulos exactos del temario (h3), lenguaje claro para pregrado.
- Referencias como tooltip: `<span class="ref" data-tooltip="{LIBRO}, p. XX — frase original">p.XX</span>`.
- Tarjetas destacadas (`.concept-card`, ⭐ las críticas) y avisos ⚠️ para lo que se suele confundir.
- **Diagramas SVG inline** cuando ayuden: curvas, diagramas de fase, esquemas de estructura
  y de procesos. Tablas comparativas en `<table>` con `<caption>`. No se recrean fotos,
  micrografías ni imágenes de equipos: basta con citar la página.
- Al final del tema, una sección «Referencias» con todas las páginas citadas, agrupadas por subtema.

### Fase 2 — Autoevaluación
10-15 preguntas que mezclan opción múltiple, verdadero/falso, completar y asociación, con
respuesta desplegable y su página.

### Fase 3 — Conceptos que se confunden
5-8 `<details class="faq-item">` con pares de conceptos confundibles y su aplicación real.
En los conceptos densos, un `<details class="faq-simple">` anidado con una explicación
sencilla y un ejemplo real (la excepción de la regla 4).

### Fase 4 — Examen tipo
15-20 preguntas de 4 opciones (`.quiz-question`, `data-correct="true"`), con justificación
y página. Si hay exámenes anteriores, se imita su estilo: «señale la FALSA», «A y B son
correctas», «Todas/Ninguna», cifras concretas.

**Al terminar cada tema:** actualizar `PROGRESO_GUIA.md`, afinar `MAPA_TEMARIO_LIBRO.md` y
cambiar `estado: 'listo'` en el array de `temario-nav.js`.

---

## 9. Fases 5-8 — Las capas de repaso (cuando la guía esté completa)

### Fase 5 — Fichas de resumen (`resumen/bloqueN.md`)
- `scripts/extraer_resumen.py` reduce cada HTML a un extracto: h1, descripción, «Mapa del
  punto», títulos de tarjetas ⭐, h3 de la Fase 1, catálogo de tablas, `<summary>` de la
  Fase 3 y páginas citadas. Las fichas se escriben **desde el extracto**.
- **Esquema fijo e idéntico en todos los temas** (es lo que permite generar lo demás por script):

```markdown
<a id="II-4"></a>
## II.4 · Título del tema

_(tema completo: [bloque2/4-slug.html](../bloque2/4-slug.html))_

Una sola frase: de qué va el punto.

**Mapa del punto**

1. **Término** — una línea. (p.287)
…5-8 líneas…

**Tabla clave — título (p.290, Tabla 13-7)**

| … | … |      ← 1-2 tablas, ≤ 6 filas y ≤ 4 columnas

**Cifras que caen**

| Concepto | Valor | Pág. |   ← máx. 8 filas, la página nunca vacía

**No confundir**

- **A frente a B:** una línea que ya resuelve la confusión.   ← 5 líneas

---
```

- Una ficha debe caber en una pantalla o una hoja A4. Prohibido añadir contenido que no esté en la guía.
- **Unidades clave** = líneas del mapa + filas de cifras + líneas de «No confundir». Hay que
  contarlas (en la guía de referencia, 625): es la vara con la que se mide la cobertura del resto.

### Fase 6 — ② Guía «lo esencial» (`esencial/`)
Por tema, en este orden:
1. 🔴 **Memorizar sí o sí**: 5-10 definiciones literales, cortas y exactas, las que se
   preguntan tal cual. Cada una con tema y página.
2. 🟠 **Importante dominar**: mecanismos, comparaciones e indicaciones para entender, no
   recitar. Cada concepto indica qué líneas del «Mapa del punto» cubre.
3. 📋 **Tabla clave**, 🔢 **Cifras clave** y ⚠️ **Trampas de examen**: salen automáticamente de la ficha.
4. 📝 **Así lo preguntan**: preguntas de exámenes anteriores sobre el tema, con la respuesta
   **según la guía** y sin citar la letra de la opción. Si la guía no encaja con ninguna
   opción, «ninguna de las anteriores». Si la guía no trata la pregunta, se marca así y no se
   inventa la respuesta. Una pregunta que toca varios temas aparece en todos ellos, con la misma respuesta.
5. 🧠 **Para recordarlo** (reglas mnemotécnicas sacadas del contenido) y 🔗 **Conexiones** con otros temas.
6. Una etiqueta de prioridad 🔥 según cuántas veces ha caído el tema en los exámenes.

Funciones de la página:
- buscador sin tener en cuenta las tildes, con resaltado;
- glosario A-Z;
- filtro por bloque;
- pestaña «Prioridad por exámenes»;
- casilla «Ya me lo sé» guardada en localStorage dentro de `try/catch`;
- barra de progreso general y por tema;
- modo «Tapar definiciones», que las desenfoca hasta tocar cada una;
- «Solo 🔴»;
- versión para imprimir, con todo desplegado y un tema por página;
- al final, «Siguiente paso: ③ Juegos».

**Cómo se garantiza que no se inventa nada:** los datos curados a mano van en
`scripts/esencial/bloqueN.json` y **cada elemento lleva en `"v"` uno o varios fragmentos
literales de la guía**. `generar_esencial.py` los busca en el HTML del tema (sin espacios ni
mayúsculas) y **aborta** si alguno no aparece. También avisa si la página indicada no
coincide con la que cita la guía junto a ese fragmento.

```json
{"t": "Sinéresis", "d": "El gel exuda líquido por sí mismo…", "p": "292",
 "v": ["el gel exuda líquido por sí mismo, sin que nadie lo seque"]}
```

### Fase 7 — ③ Juegos (`juegos/`)
Juegos de repaso: Pasapalabra, ¿Mito o realidad?, casos clínicos flash, «¿Quién soy?»,
secuencias y parejas de cifras. `generar_juegos.py` saca de las fichas las «Cifras que caen»
(parejas) y los «No confundir» (explicación de cada mito) a `fichas.js`. Lo redactado a mano va en `datos.js`.

### Fase 8 — ④ Examen (`simulador/`)
`generar_simulador.py` recoge:
- todas las preguntas de la Fase 4 de cada tema;
- las de `preguntas_estilo_examen.json`, redactadas desde la guía con el formato de los exámenes reales.

Genera `simulador/index.html` autocontenido a partir de `plantilla.html`. Cada simulacro:
N preguntas al azar, opciones barajadas en cada intento (salvo «Todas», «Ninguna» y las que
se refieren a otra opción), cronómetro, corrección al final con explicación y página, y filtro por bloque.

---

## 10. Fase 9 — Verificación (antes de cada commit)

- **Navegador headless (Playwright):** cada sección en escritorio (1280 px) y móvil
  (390 px), sin errores de JS, sin scroll horizontal y con capturas revisadas a ojo.
  Probar también la interacción: marcar, recargar y comprobar que persiste; buscar; filtrar; imprimir a PDF.
- **Sin patrones que delaten la respuesta** (medirlo con un script, no a ojo):
  - la correcta no puede ser siempre la más larga;
  - la correcta no puede caer siempre en la misma posición;
  - en «Mito o realidad», ni mayoría de mitos ni de realidades;
  - en la Guía, ninguna respuesta cita letras de opción ni se contradice entre temas.
- **Conteos y cobertura:** definiciones por tema (5-10), unidades clave cubiertas (deben ser
  todas), preguntas de examen con respuesta y sin respuesta. Informar de las cifras.

---

## 11. Git y despliegue

- Rama `feature/<nombre>` desde `develop`; commits por bloque o por hito, no por archivo.
- **Commit solo de los archivos propios.** En Windows muchos archivos aparecen modificados
  solo por los fines de línea (CRLF): no se incluyen. Para ver los cambios reales:
  `git diff --ignore-cr-at-eol --stat`.
- Si tras un comando de git queda `.git/index.lock`, se borra.
- Al terminar: merge `--no-ff` a `develop` en local; el `git push origin develop` lo hace el
  usuario. Al hacer push se despliega automáticamente.
- Mensajes de commit claros, con qué se añadió y cómo se regenera.

---

## 12. Lecciones aprendidas

- **Piloto primero.** Un tema completo, revisado, antes de generar el resto. Lo mismo para cada capa nueva.
- **Lista de tareas visible** durante todo el trabajo, con la verificación como último paso.
- **El esquema fijo de las fichas es lo que permite automatizar.** Sin él, cada capa se escribe a mano.
- **Separar capas y no mezclar secciones**: el contenido no lleva atajos a lo esencial y la Guía no repite el contenido.
- **Verificar contra la guía por script**, con fragmentos literales y no de memoria. Un
  cambio de una palabra («algas pardas» → «algas rojas») tiene que hacer fallar la generación.
- **Las páginas también se verifican**: el script compara la página escrita con la que cita
  la guía junto al fragmento. Así salieron varios errores de una página.
- **El desfase PDF↔libro no es constante**: comprobarlo siempre en la página.
- **Los temas que el libro no cubre se marcan «sin fuente»** y no se rellenan.
- **Las respuestas sin letra de opción** evitan que el alumno memorice «la c».
- **Respuestas de examen ambiguas o no tratadas por la guía**: decirlo, no inventarlo.

---

## 13. Prompts listos para copiar (uno por fase)

> En todos: «Lee primero `CLAUDE.md` y este archivo (`METODO_GUIA_DE_ESTUDIO_DESDE_PDF.md`).
> Usa una lista de tareas. Respeta las reglas de la sección 2 y la disciplina de tokens de la sección 3».

**Fase 0-1 — Arranque y texto**
```text
Proyecto nuevo de guía de estudio. Datos: [pega la sección 1 rellenada].
1) Crea la estructura de carpetas, CLAUDE.md, PROGRESO_GUIA.md y temario.txt.
2) Convierte el PDF a texto por página y por capítulo (sección 5). Comprueba 4 páginas,
   una con tabla, y anota en CLAUDE.md cómo localizar la página impresa del libro.
Enséñame el resultado antes de seguir.
```

**Fase 2 — Mapa**
```text
Construye MAPA_TEMARIO_LIBRO.md (sección 6): cada punto de temario.txt → capítulo,
archivo de texto y rango de páginas del libro. Marca como «sin fuente» lo que no esté
en el libro. No leas capítulos enteros: usa grep sobre títulos y cabeceras.
```

**Fase 3 — Esqueleto**
```text
Crea el esqueleto del sitio (sección 7): style.css, temario-nav.js con el array del
temario, menu.js con el ciclo ① Índice ② Guía ③ Juegos ④ Examen y la portada.
Pruébalo en Playwright a 1280 y 390 px.
```

**Fase 4 — Un tema (repetir por tema)**
```text
Genera el tema {II.4 · Título} con sus 4 fases (sección 8). Lee solo las páginas que
indica MAPA_TEMARIO_LIBRO.md. Cita la página impresa en cada afirmación. Al terminar,
actualiza PROGRESO_GUIA.md, el mapa y el estado en temario-nav.js.
[Primera vez: «Es el piloto: enséñamelo antes de seguir»].
```

**Fase 5 — Fichas**
```text
Crea scripts/extraer_resumen.py y escribe las fichas de resumen/bloqueN.md desde los
extractos, con el esquema fijo de la sección 9. Empieza por un bloque piloto. Cuenta las
unidades clave totales e infórmame.
```

**Fase 6 — Guía esencial**
```text
Crea la sección ② Guía (sección 9, fase 6): esencial/index.html, generar_esencial.py y
scripts/esencial/bloqueN.json con fragmentos «v» verificados. Exámenes anteriores en
{ruta}: solo para saber qué se pregunta. Empieza por un tema piloto y enséñamelo.
Después, todos, con un informe de cobertura sobre las unidades clave.
```

**Fase 7-8 — Juegos y examen**
```text
Crea juegos/ y simulador/ con sus scripts generadores (sección 9, fases 7 y 8). Mide
con un script que no haya patrones en las respuestas (sección 10).
```

**Cierre**
```text
Verifica todo (sección 10), haz commit solo de mis archivos en la rama feature y merge
--no-ff a develop en local (sección 11). Dime qué tengo que hacer yo para publicar.
```
