# Mapa temario → libro

Generado por `python scripts/mapa_secciones.py --md`. **Páginas = página impresa del libro**
(coincide con la del PDF). Cada apartado va de la página en que empieza hasta la página en
que empieza el siguiente (esa última puede ser compartida). Se afina al generar cada tema.

**Cobertura:** los 18 puntos del temario tienen capítulo propio en el libro con el mismo título.
Ningún punto «sin fuente».

**«Leer como imagen»** es una detección automática (página casi sin texto o con cifras
revueltas) y solo orientativa: las señales del T8 tienen texto, pero su forma y color
solo se ven en la imagen. Ante cualquier tabla o señal dudosa, rasterizar.

## T1 · Tema 1. Definiciones

- Archivo: `libro_texto/por_capitulo/tema01_definiciones.txt`
- Páginas del libro: 5-25 (índice del tema en p.5)
- Apartados → páginas:
  - Definiciones relacionadas con los vehículos — pp.6-23
    - Vehículos sin motor — pp.6-8
    - Vehículos a motor — pp.8-21
    - Otro tipo de vehículos con motor — pp.21-23
  - Definiciones relacionadas con las personas — pp.23-25
    - Conductor — pp.23-24
    - Peatón — p.24
    - Titular del vehículo — pp.24-25
    - Conductor habitual — p.25
  - Categorías de los vehículos dependiendo de su uso — p.25
- Notas: ✅ listo (`guia/tema01/definiciones.html`). El libro nombra sin definir el trolebús (p.9) y la bicicleta de pedales con motor (p.21, 23): marcados ⚠️ en la guía, sin rellenar. Tabla M/N/O (p.25) y p.23 comprobadas en imagen.
- Relacionado con: T2 (tipos de permiso según el vehículo), T13 (medidas y cargas)

## T2 · Tema 2. Documentación

- Archivo: `libro_texto/por_capitulo/tema02_documentacion.txt`
- Páginas del libro: 26-41 (índice del tema en p.26)
- Apartados → páginas:
  - Documentos necesarios para conducir — pp.27-28
  - Permiso de conducir — pp.28-32
    - Tipos de permiso de conducir — pp.28-31
    - Permiso de conducir por puntos — p.31
    - Conductores noveles — pp.31-32
    - ¿Cuándo debes renovar tu permiso de conducir tipo B? — p.32
  - Permiso de circulación — pp.32-34
    - ¿Qué vehículos deben tener permiso de circulación? — p.33
    - ¿Qué datos aparecen en el permiso de circulación? — pp.33-34
  - Tarjeta de inspección técnica (ITV) — pp.34-37
    - ¿Qué vehículos deben tener la tarjeta de inspección técnica? — p.34
    - ¿Qué datos aparecen en la tarjeta de inspección técnica? — pp.34-35
    - ¿Cuándo debes pasar la inspección técnica de tu vehículo (ITV)? — pp.35-37
    - Resultados de la inspección técnica — p.37
  - Seguro obligatorio de responsabilidad civil — pp.37-40
    - ¿Qué vehículos deben tener seguro obligatorio de responsabilidad civil? — p.38
    - ¿Qué cubre el seguro obligatorio? — pp.38-39
    - ¿Qué no cubre el seguro obligatorio? — pp.39-40
    - ¿Qué consecuencias tiene no asegurar el vehículo? — p.40
  - Personas responsables — pp.40-41
- Notas: ✅ listo (`guia/tema02/documentacion.html`). Tablas de permisos (p.29-30) e ITV (p.35-36) transcritas desde la imagen: el texto extraído las mezcla.
- Relacionado con: ANEXO (permiso por puntos), T15 (ITV y mantenimiento)

## T3 · Tema 3. El estado del conductor

- Archivo: `libro_texto/por_capitulo/tema03_el_estado_del_conductor.txt`
- Páginas del libro: 42-73 (índice del tema en p.42)
- Apartados → páginas:
  - Estado físico y psicológico del conductor — pp.43-45
  - Factores que influyen en el estado del conductor — pp.45-68
    - Fatiga — pp.45-48
    - Somnolencia — pp.48-52
    - Alcohol — pp.52-58
    - Otras drogas — pp.58-62
    - Enfermedades y medicamentos — pp.62-66
    - Alimentación — p.66
    - Ropa adecuada — pp.66-68
  - Accidentes por distracciones — pp.68-73
    - Fumar en el vehículo — p.70
    - Uso del teléfono móvil — pp.70-72
    - Navegadores GPS — pp.72-73
- Notas: ✅ listo (`guia/tema03/estado-del-conductor.html`). Tablas leídas en imagen: p.59 (drogas) y p.64 (enfermedades); el texto de pdftotext las mezcla. p.69 tiene una errata en el libro («Ditracciones»). Contenido de los «Ver vídeo» no disponible.
- Relacionado con: T14 (fatiga y somnolencia al conducir de noche), T16 (factores de riesgo)

## T4 · Tema 4. Obligaciones de conductores y peatones

- Archivo: `libro_texto/por_capitulo/tema04_obligaciones_de_conductores_y_peatones.txt`
- Páginas del libro: 74-85 (índice del tema en p.74)
- Apartados → páginas:
  - Seguridad en la carretera — pp.75-76
  - Obligaciones de los conductores — pp.76-81
    - Obligaciones generales — pp.76-78
    - Vehículos de dos o tres ruedas — pp.78-80
    - Vehículos especiales — pp.80-81
  - Obligaciones de los peatones — pp.81-85
    - Obligaciones generales — pp.81-84
    - Vehículos de movilidad personal — pp.84-85
  - Animales en carretera — p.85
- Notas: ✅ listo (`guia/tema04/obligaciones-conductores-peatones.html`). Texto limpio; la tabla de p.78 (conducción defensiva / zona de inseguridad) se entiende sin imagen.
- Relacionado con: T9 (por dónde circulan peatones y vehículos), T12 (preferencia de peatones y animales)

## T5 · Tema 5. Dispositivos de seguridad en el vehículo

- Archivo: `libro_texto/por_capitulo/tema05_dispositivos_de_seguridad_en_el_vehiculo.txt`
- Páginas del libro: 86-119 (índice del tema en p.86)
- Apartados → páginas:
  - La importancia del vehículo en los accidentes de tráfico — pp.87-89
  - Elementos de seguridad activa — pp.89-106
    - Sistemas de alumbrado — pp.89-93
    - Los frenos — pp.93-97
    - Las ruedas — pp.97-104
    - Otros elementos de seguridad activa — pp.104-106
  - Elementos de seguridad pasiva — pp.106-119
    - El chasis y la carrocería — p.106
    - El cinturón de seguridad — pp.106-114
    - Los airbags — pp.114-116
    - El reposacabezas — pp.116-117
    - El casco — pp.117-119
- Notas: ✅ listo (`guia/tema05/dispositivos-de-seguridad.html`). Tablas p.96 (fallo de frenos) y p.100 (presión) leídas en imagen: en p.100 el texto extraído ponía «la rueda se reviente» en la columna equivocada (va con presión BAJA). El libro llama al frenado autónomo «AES» (p.93) y «AEB» (p.94): señalado en la guía.
- Relacionado con: T7 (sistemas de alumbrado), T15 (frenos, ruedas y neumáticos)

## T6 · Tema 6. Elementos del vehículo y normas para usarlos

- Archivo: `libro_texto/por_capitulo/tema06_elementos_del_vehiculo_y_normas_para_usa.txt`
- Páginas del libro: 120-138 (índice del tema en p.120)
- Apartados → páginas:
  - Mandos del vehículo — pp.121-125
    - Mandos de los vehículos en general — pp.121-124
    - Mandos de las motocicletas — pp.124-125
  - Visibilidad al conducir — pp.125-129
    - Limpiaparabrisas — pp.126-127
    - Lavaparabrisas — p.127
    - Luneta térmica — p.127
    - Retrovisores — pp.127-129
  - Reglas para conducir de forma cómoda y segura — pp.129-134
    - Reglas para conducir turismos, furgonetas y camiones — pp.130-132
    - Reglas para conducir motocicletas — pp.132-134
  - Sistemas que ayudan a conducir con seguridad — pp.134-138
- Notas: ✅ listo (`guia/tema06/elementos-del-vehiculo.html`). Texto limpio.
- Relacionado con: T5 (seguridad activa), T17 (preparar el viaje)

## T7 · Tema 7. Sistema de luces de los vehículos

- Archivo: `libro_texto/por_capitulo/tema07_sistema_de_luces_de_los_vehiculos.txt`
- Páginas del libro: 139-153 (índice del tema en p.139)
- Apartados → páginas:
  - Normas generales para usar las luces del vehículo — pp.140-141
  - Luces del vehículo — pp.141-152
    - Luces de posición — pp.142-143
    - Luz de estacionamiento — p.143
    - Luces de gálibo — pp.143-144
    - Luz de largo alcance o luz de carretera — pp.144-145
    - Luz de corto alcance o de cruce — pp.145-147
    - Luces de antiniebla — pp.147-148
    - Catadióptrico — pp.148-149
    - Luz indicadora de dirección — p.149
    - Señal de emergencia — pp.149-151
    - Luz de frenado — p.151
    - Tercera luz de freno — pp.151-152
    - Luz de marcha atrás — p.152
  - Señales acústicas — pp.152-153
- Notas: ✅ listo (`guia/tema07/sistema-de-luces.html`). Las «luces de circulación diurna» aparecen en el esquema de p.141 pero el libro no las explica: no se desarrollan.
- Relacionado con: T5 (sistemas de alumbrado), T14 (conducir de noche y con niebla)

## T8 · Tema 8. Señales de circulación

- Archivo: `libro_texto/por_capitulo/tema08_senales_de_circulacion.txt`
- Páginas del libro: 154-211 (índice del tema en p.154)
- Apartados → páginas:
  - Tipos de señales — pp.155-165
    - Normas generales — pp.155-157
    - Los agentes de tráfico — pp.157-160
    - Señales temporales — pp.160-161
    - Semáforos — pp.161-165
  - Señales verticales — pp.165-200
    - Señales que advierten de peligro — pp.166-172
    - Señales de reglamentación — pp.172-184
    - Señales de indicación — pp.184-200
  - Líneas y marcas en las carreteras — pp.200-211
    - Líneas y marcas blancas — pp.200-209
    - Líneas y marcas de colores — pp.209-211
- Leer como imagen (`scripts/rasterizar.py`): 211
- Notas: ✅ listo (`guia/tema08/senales-de-circulacion.html`). Tablas p.157, 158, 159, 161, 162, 163 y 164 leídas en imagen: el texto extraído emparejaba mal varias filas (p.157 Stop+ceda → Stop; p.158 «aunque baje los brazos» va con brazos horizontales; p.162 amarillo intermitente → ceder el paso). Las señales no se dibujan: el texto del libro no describe formas ni colores.
- Relacionado con: T9 (colores y carriles), T10 (señales de velocidad), T12 (señales de preferencia)

## T9 · Tema 9. La vía

- Archivo: `libro_texto/por_capitulo/tema09_la_via.txt`
- Páginas del libro: 212-242 (índice del tema en p.212)
- Apartados → páginas:
  - La vía para vehículos y peatones — pp.213-223
    - Partes de la vía para vehículos — pp.213-215
    - Otras zonas de la vía — pp.215-222
    - Dirección y sentido — pp.222-223
  - Tipos de vía — pp.223-227
    - Dependiendo de dónde está — pp.223-224
    - Dependiendo de sus características — pp.224-226
    - Colores que indican el estado de la carretera — pp.226-227
  - Los carriles — pp.227-240
    - ¿Por dónde deben circular los vehículos? — pp.227-229
    - Normas para usar los carriles — pp.229-232
    - Carriles reservados — pp.232-235
    - Carriles especiales — pp.235-238
    - El arcén — pp.238-240
  - Circular por autopistas y autovías — pp.240-242
    - Emergencias en la autopista y autovía — pp.241-242
- Relacionado con: T8 (líneas y marcas), T11 (maniobras en carriles), T12 (túneles)

## T10 · Tema 10. Velocidad y distancias

- Archivo: `libro_texto/por_capitulo/tema10_velocidad_y_distancias.txt`
- Páginas del libro: 243-266 (índice del tema en p.243)
- Apartados → páginas:
  - Tipos de velocidad — pp.244-251
    - Velocidad máxima — pp.244-245
    - Velocidad mínima — p.245
    - Velocidad inadecuada — pp.245-246
    - Velocidad adecuada — pp.246-247
    - Situaciones en las que debes conducir a poca velocidad — pp.247-251
  - Velocidad genérica — pp.251-261
    - Límites de velocidad fuera de pueblos y ciudades — pp.251-256
    - Límites de velocidad máxima dentro de pueblos y ciudades — pp.256-258
    - Límites de velocidad mínima dentro y fuera de pueblos y ciudades — pp.258-259
    - ¿Por qué son necesarios los límites de velocidad? — pp.259-261
  - Tipos de distancia — pp.261-266
    - Distancia de reacción — pp.261-262
    - Distancia de frenado — pp.262-263
    - Distancia de detención — pp.263-264
    - Separación lateral — p.264
    - Distancia de seguridad — pp.264-266
- Leer como imagen (`scripts/rasterizar.py`): 252, 253, 254, 255, 256, 257
- Relacionado con: T3 (tiempo de reacción), T14 (curvas y clima), T17 (controlar el espacio)

## T11 · Tema 11. Maniobras

- Archivo: `libro_texto/por_capitulo/tema11_maniobras.txt`
- Páginas del libro: 267-300 (índice del tema en p.267)
- Apartados → páginas:
  - Regla de seguridad R.S.M. — pp.268-274
    - Pasos de la regla de seguridad R.S.M. (Retrovisor, Señal y Maniobra) — pp.268-271
    - Regla de seguridad al entrar a una carretera — pp.271-273
    - Precauciones al cambiar de carril — pp.273-274
  - Adelantar a otros vehículos — pp.274-284
    - ¿Por qué lado debes adelantar? — pp.274-277
    - Pasos a seguir para adelantar a otro vehículo — pp.277-281
    - Obligaciones del conductor al que le adelanta otro vehículo — pp.281-282
    - ¿Cuándo está prohibido adelantar? — pp.282-284
  - Cambio de dirección y de sentido — pp.284-290
    - Cambio de dirección — pp.284-287
    - Cambio de sentido — pp.287-290
  - Marcha atrás — pp.290-291
  - Detener el vehículo — pp.291-294
  - Parar y estacionar — pp.294-300
    - Diferencia entre parar y estacionar — p.294
    - ¿Dónde puedes parar y estacionar? — pp.294-297
    - Paradas y estacionamientos peligrosos — pp.297-299
    - ¿Dónde está prohibido parar y estacionar? — pp.299-300
- Relacionado con: T7 (luz indicadora de dirección), T9 (uso de los carriles)

## T12 · Tema 12. Normas de preferencia para circular

- Archivo: `libro_texto/por_capitulo/tema12_normas_de_preferencia_para_circular.txt`
- Páginas del libro: 301-318 (índice del tema en p.301)
- Apartados → páginas:
  - Ceder el paso a otros vehículos — pp.302-311
    - Normas generales — p.302
    - Normas para ceder el paso en lugares concretos — pp.302-305
    - Preferencia de paso para ciclistas, peatones y animales — pp.305-308
    - Preferencia de paso para vehículos en servicio de urgencias — pp.308-311
  - Preferencia de paso en zonas estrechas — pp.311-314
    - Zonas estrechas con señales — p.311
    - Zonas estrechas sin señales — pp.311-314
    - Zonas estrechas en cuesta — p.314
  - Cruzar pasos a nivel y puentes móviles — pp.314-316
  - Cruzar túneles y pasos inferiores — pp.316-318
    - Normas para parar el vehículo dentro de un túnel — pp.316-317
    - Emergencias dentro de un túnel — pp.317-318
- Relacionado con: T8 (señales de preferencia), T11 (incorporaciones)

## T13 · Tema 13. Transportar personas y cargas

- Archivo: `libro_texto/por_capitulo/tema13_transportar_personas_y_cargas.txt`
- Páginas del libro: 319-340 (índice del tema en p.319)
- Apartados → páginas:
  - Normas para transportar personas, animales y cargas — pp.320-327
    - Normas generales — pp.320-321
    - Transportar personas — pp.321-324
    - Transportar cargas — pp.324-327
  - Medidas permitidas para vehículos y cargas — pp.327-335
    - Medidas permitidas para vehículos — pp.327-329
    - Medidas permitidas para cargas — pp.329-333
    - Señalar la carga que sobresale — pp.333-335
    - Operaciones de carga y descarga — p.335
  - Placas y señales de los vehículos — pp.335-340
- Relacionado con: T1 (tipos de vehículos), T7 (señalizar la carga)

## T14 · Tema 14. Conducir de forma segura

- Archivo: `libro_texto/por_capitulo/tema14_conducir_de_forma_segura.txt`
- Páginas del libro: 341-364 (índice del tema en p.341)
- Apartados → páginas:
  - La carretera — pp.342-347
    - Las curvas — pp.342-346
    - Zona de la carretera en obras — pp.346-347
  - Conducir por la noche — pp.347-353
  - El clima — pp.353-364
    - Conducir con lluvia — pp.353-356
    - Conducir con nieve — pp.356-358
    - Conducir con hielo — pp.358-360
    - Conducir con niebla — pp.360-361
    - Conducir con nubes de polvo o de humo — p.361
    - Conducir con mucho viento — pp.361-363
    - Conducir con calor — pp.363-364
- Relacionado con: T3 (estado del conductor), T7 (luces), T10 (velocidad y distancias)

## T15 · Tema 15. Mecánica y mantenimiento del vehículo

- Archivo: `libro_texto/por_capitulo/tema15_mecanica_y_mantenimiento_del_vehiculo.txt`
- Páginas del libro: 365-387 (índice del tema en p.365)
- Apartados → páginas:
  - Sistemas del vehículo — pp.366-386
    - Sistema de alimentación — pp.366-368
    - Sistema eléctrico — pp.368-371
    - Sistema de lubricación — pp.371-376
    - Sistema de refrigeración — pp.376-379
    - Sistema de transmisión — pp.379-380
    - Sistema de dirección — pp.380-382
    - Sistema de suspensión — pp.382-385
    - Sistema de frenado — pp.385-386
  - Revisión de ruedas y neumáticos — pp.386-387
- Relacionado con: T5 (frenos y ruedas), T17 (comprobaciones antes del viaje)

## T16 · Tema 16. Accidentes de tráfico

- Archivo: `libro_texto/por_capitulo/tema16_accidentes_de_trafico.txt`
- Páginas del libro: 388-436 (índice del tema en p.388)
- Apartados → páginas:
  - Evitar accidentes de tráfico — pp.389-395
    - Factores de riesgo — pp.389-392
    - Consecuencias de los accidentes de tráfico para la sociedad — pp.392-395
  - Personas con más riesgo de sufrir accidentes de tráfico — pp.395-412
    - Peatones — pp.396-403
    - Conductores — pp.403-412
  - Actuar en caso de accidente — pp.412-424
    - Pasos a seguir — pp.412-415
    - Regla PAS — pp.415-424
  - Primeros auxilios — pp.424-436
    - Constantes vitales — pp.424-428
    - Conocer el estado de los heridos — pp.428-436
    - Trasladar a los heridos — p.436
- Leer como imagen (`scripts/rasterizar.py`): 404
- Relacionado con: T3 (factores del conductor), T5 (seguridad pasiva), T9 (emergencias en autopista)

## T17 · Tema 17. Conducción preventiva y eficiente

- Archivo: `libro_texto/por_capitulo/tema17_conduccion_preventiva_y_eficiente.txt`
- Páginas del libro: 437-466 (índice del tema en p.437)
- Apartados → páginas:
  - Preparar el viaje — pp.438-440
    - Comprobaciones de seguridad — pp.438-439
    - Elegir la ruta — pp.439-440
  - Conducción preventiva — pp.440-449
    - ¿Qué es? — pp.440-441
    - Visión — p.441
    - Anticipación — pp.441-446
    - Controlar el espacio — pp.446-449
  - Conducción eficiente — pp.449-466
    - ¿Qué es? — pp.449-450
    - La contaminación — pp.450-452
    - Técnicas para conducir de forma eficiente — pp.452-455
    - ¿Qué hace que se consuma más combustible? — pp.455-463
    - Distintivos ambientales — pp.463-466
- Relacionado con: T10 (distancias), T15 (mantenimiento)

## ANEXO · Anexo puntos. El permiso de conducir por puntos

- Archivo: `libro_texto/por_capitulo/anexo_el_permiso_de_conducir_por_puntos.txt`
- Páginas del libro: 467-474 (índice del tema en p.467)
- Apartados → páginas:
  - ¿Cuántos puntos tiene cada conductor? — pp.468-469
  - Perder puntos — pp.469-470
  - ¿Qué faltas quitan puntos del permiso de conducir? — pp.470-474
- Leer como imagen (`scripts/rasterizar.py`): 470
- Relacionado con: T2 (permiso de conducir por puntos)

