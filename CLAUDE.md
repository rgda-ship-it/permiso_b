# Manual Permiso B — guía de estudio web

Guía de estudio estática (HTML + CSS + JS) para la prueba teórica del **permiso de
conducir clase B**, construida a partir de un único libro. El método completo, fase a
fase, está en [METODO_GUIA_DE_ESTUDIO_DESDE_PDF.md](METODO_GUIA_DE_ESTUDIO_DESDE_PDF.md):
**léelo antes de cada fase** y respeta sus reglas (sección 2) y su disciplina de tokens (sección 3).

## Datos del proyecto

```text
ASIGNATURA ............ Permiso de Conducir Clase B (Educación Vial / Legislación de Tráfico)
LIBRO / EDICIÓN ....... Manual del Permiso B en Lectura Fácil. Adaptación: María Peralta y Laia Vidal.
                        Dirección General de Tráfico / ETRASA. 1.ª ed. corregida, octubre 2024
CITA CORTA ............ Manual Permiso B (DGT, LF)
PDF ................... Libro.pdf (476 páginas, con texto → pdftotext)
IDIOMA ................ es (libro y guía)
TEMARIO OFICIAL ....... Temario.txt (17 temas + Anexo puntos)
EXÁMENES ANTERIORES ... no hay
REPO .................. https://github.com/rgda-ship-it/permiso_b · rama base develop
DESPLIEGUE ............ Cloudflare Pages (push a develop → despliegue)
PÚBLICO ............... Estudiantes de la prueba teórica del permiso B con materiales
                        adaptados a Lectura Fácil (norma UNE 153101:2018 EX)
```

## Tarea activa

- [x] Fase 0 — estructura, CLAUDE.md, PROGRESO_GUIA.md
- [x] Fase 1 — PDF a texto
- [ ] Fase 2 — `MAPA_TEMARIO_LIBRO.md`
- [ ] Fase 3 — esqueleto del sitio
- [ ] Fase 4 — temas (piloto primero)
- [ ] Fases 5-8 — fichas, Guía esencial, Juegos, Examen
- [ ] Fase 9 — verificación y cierre

## Reglas (resumen; detalle en el método, sección 2)

1. **Fuente única:** todo sale del libro. Lo que no esté → `⚠️ No cubierto en Manual Permiso B (DGT, LF)` y tema «sin fuente».
2. **Cada afirmación con su página impresa** del libro.
3. **Sintetizar, no copiar** texto literal largo.
4. Única excepción a «no inventar»: el bloque `faq-simple` («Para visualizarlo: …», sin página).
5. Las capas superiores (fichas, Guía, Juegos, Examen) se alimentan de la guía, nunca del PDF.
6. Todo lo publicado es estático y se abre con doble clic (`file://`). Python solo para generar, en local.
7. Los títulos de los temas coinciden exactamente con `Temario.txt`.
8. No hay exámenes anteriores: el estilo de examen se toma del formato habitual DGT
   (3 opciones a/b/c) **solo como formato**, nunca como contenido.

### Particularidades de este libro (Lectura Fácil)

- Lenguaje ya simplificado: frases cortas, una idea por línea, glosarios en recuadro
  (p. ej. «Eje. Barra que atraviesa…»). La guía debe **mantener ese registro sencillo**:
  frases cortas, vocabulario explicado, nada de jerga técnica añadida.
- El libro remite a vídeos («Ver vídeo»): no tenemos su contenido; no se cita ni se resume.
- Muchas señales y tablas son **imágenes**: el texto extraído sale desordenado o vacío
  (p. ej. tabla de velocidades, p. 252). En esos casos se rasteriza la página y se lee la imagen.

## Cómo localizar la página impresa (comprobado en la Fase 1)

- **La página impresa coincide con la del PDF en todo el libro (desfase 0).** Comprobado
  en las 470 páginas numeradas con `libro_texto/indice_paginas.tsv`.
- El número va **al pie**: abajo a la izquierda en páginas pares y a la derecha en impares.
  A veces `pdftotext` lo pega a la última línea de texto («46 ■ Estás incómodo…»).
- La cabecera de cada página lleva el título del tema («Tema 10. Velocidad y distancias»),
  a veces precedida de un icono («STOP», «!»).
- Cada página de `libro_texto/` empieza con `--- PÁGINA PDF N · LIBRO p.N ---`.
- Páginas sin numerar: 1-4 (portada, créditos, índice general, página en blanco) y 475-476 (contraportada).

## Rangos por tema (páginas del libro = PDF)

| Tema | Páginas | Archivo en `libro_texto/por_capitulo/` |
|---|---|---|
| 1. Definiciones | 5-25 | tema01_definiciones.txt |
| 2. Documentación | 26-41 | tema02_documentacion.txt |
| 3. El estado del conductor | 42-73 | tema03_el_estado_del_conductor.txt |
| 4. Obligaciones de conductores y peatones | 74-85 | tema04_… |
| 5. Dispositivos de seguridad en el vehículo | 86-119 | tema05_… |
| 6. Elementos del vehículo y normas para usarlos | 120-138 | tema06_… |
| 7. Sistema de luces de los vehículos | 139-153 | tema07_… |
| 8. Señales de circulación | 154-211 | tema08_… |
| 9. La vía | 212-242 | tema09_… |
| 10. Velocidad y distancias | 243-266 | tema10_… |
| 11. Maniobras | 267-300 | tema11_… |
| 12. Normas de preferencia para circular | 301-318 | tema12_… |
| 13. Transportar personas y cargas | 319-340 | tema13_… |
| 14. Conducir de forma segura | 341-364 | tema14_… |
| 15. Mecánica y mantenimiento del vehículo | 365-387 | tema15_… |
| 16. Accidentes de tráfico | 388-436 | tema16_… |
| 17. Conducción preventiva y eficiente | 437-466 | tema17_… |
| Anexo puntos. El permiso de conducir por puntos | 467-474 | anexo_… |

Cada tema empieza con una página «Índice» propia (la primera de su rango): úsala para el Mapa del punto.

## Rutas

```
Libro.pdf · Temario.txt · MAPA_TEMARIO_LIBRO.md · PROGRESO_GUIA.md
libro_texto/paginas/pagina_NNN.txt · por_capitulo/*.txt · libro_completo.txt · indice_paginas.tsv
libro_img/            ← páginas rasterizadas bajo demanda (no se versiona)
scripts/extraer_texto.py   ← regenera libro_texto/ (requiere pdftotext)
scripts/rasterizar.py N…   ← PNG de páginas concretas (requiere PyMuPDF)
guia/                 ← el sitio (estructura en la sección 0 del método)
```

Estructura del temario: no hay bloques, solo 17 temas + anexo. Convención para el sitio:
**un bloque por tema** (`guia/temaNN/`), y el anexo en `guia/anexo/`. Identificadores: `T1`…`T17`, `ANEXO`.

## Git

- Rama base `develop`; trabajo en `feature/<nombre>`. Commits por hito.
- En Windows, revisar cambios reales con `git diff --ignore-cr-at-eol --stat`; commit solo de archivos propios.
- Si queda `.git/index.lock`, borrarlo.
- Al terminar: merge `--no-ff` a `develop` en local. **El `git push origin develop` lo hace el usuario.**
