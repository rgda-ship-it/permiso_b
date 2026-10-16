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

