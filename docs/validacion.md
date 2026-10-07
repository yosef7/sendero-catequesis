# Validación de la primera versión

Fecha: 3 de octubre de 2026. Todos los registros utilizados fueron ficticios.

- `uv run pytest -q`: **9 pruebas aprobadas**. Acceso/CSRF, validaciones sin escrituras parciales, historial y avance de etapa, corrección de asistencia, archivado reversible, configuración, respaldo, contexto de IA y hosts/cabeceras.
- El respaldo descargado se abrió con SQLite: `PRAGMA integrity_check` devolvió `ok`, con fichas y eventos presentes.
- Navegador: creación de ficha, verificación, confirmación de avance, asistencia, observación y persistencia después de recargar. Configuración de etapas accesible.
- Capturas de escritorio y móvil revisadas. A 390 píxeles no hubo desbordamiento horizontal en el registro.
- Ollama respondió realmente con `qwen2.5-coder:3b` a un contexto numérico de la ficha ficticia. No se enviaron campos personales. Esta prueba confirma conectividad e inferencia, no calidad garantizada de los resúmenes.
- Sintaxis de los dos módulos JavaScript comprobada con Node.
- Base, código de acceso y artefactos de pruebas excluidos de Git.

Pendiente: confirmación de etapas reales por el equipo de catequesis, prueba de aceptación con sus integrantes, prueba de carga, cuentas multiusuario y publicación del repositorio/demo/artículo. El servidor actual es local y no está preparado para exposición en internet.

## Ampliación para la entrega al reto · 3 de octubre

- `uv run pytest -q`: **18 pruebas aprobadas** tras incorporar las propuestas de acompañamiento. Se añadieron persistencia, detección de contexto cambiado, salida inválida sin escritura, pertenencia al catálogo, aceptación de una respuesta válida y migración desde versión 1 preservando la ficha existente.
- Se probaron tres casos con Ollama real y `qwen2.5-coder:3b`: sin clases, requisitos pendientes y requisitos verificados. Las tres respuestas finales fueron válidas. Las duraciones observadas fueron 41,87 s, 4,78 s y 3,61 s; la primera incluye carga del modelo. El modelo puede priorizar acciones generales; no se demuestra que siempre escoja la mejor prioridad.
- La primera variante de redacción libre devolvió detalles no sustentados; se sustituyó por selección/priorización dentro de un catálogo revisado. Un intento con `llama3:latest` agotó el tiempo de espera; no se cuenta como comparación de calidad ni modelo validado.
- Grabación real de 36,2 s en una base ficticia separada: generación local, verificación, propuesta desactualizada, avance, asistencia, observación y persistencia después de recargar. **Cero errores de JavaScript**. A 390 px no hubo desbordamiento horizontal.
- MP4 H.264 de 1280 × 800, sin audio, con explicaciones en inglés. Capturas limpias del registro, propuesta, recorrido y teléfono.
- Los logs temporales del navegador se mantienen en `artifacts/`, excluido de Git.

Esto demuestra la ejecución local y el material preparado; el artículo publicado está en [DEV](https://dev.to/arnulfo_07/sendero-helping-noris-prepare-each-childs-next-step-with-local-open-ai-4gl3). No confirma aceptación por los jueces ni retroalimentación del equipo de catequesis.

## Flujo con períodos, grupos y responsables · 3 de octubre, 2026

- **26 pruebas aprobadas** (`uv run pytest -q`), incluidas migración desde versiones 1 y 2, reinicialización sin duplicados, dos responsables, inscripción y respaldo, reversión de ficha completa ante grupo inválido, pertenencia y fecha de asistencia, revisión humana sin modificar requisitos, rechazo de propuestas desactualizadas y cambios de contexto durante generación.
- Sintaxis de `app.js`, `api.js` y `plans.js`, y `git diff --check`: sin errores.
- Chromium real, 1280 × 800: acceso, período, grupo, participante con dos responsables, clase con tema e inscripción, observación, inferencia real, revisión humana y persistencia al recargar.
- Contexto móvil emulado con pantalla táctil: edición del contacto de un responsable, persistencia comprobada por API, y vistas de ficha, períodos, etapas y listado a 390 y 320 px. Ocho comprobaciones sin desbordamiento horizontal.
- En la repetición se detectó navegación antes de terminar la carga de `/state`; se deshabilitaron los botones durante la carga inicial. La prueba final concluyó con **cero errores de JavaScript**.
- Ollama real (`qwen2.5-coder:3b`): la grabación del 4 oct obtuvo una propuesta válida en **17,79 segundos**, con el modelo sin cargar en memoria; la anterior, del 3 oct, tardó 3,34 s y la primera de esta ampliación 20,37 s. No se generalizan esos tiempos.
- Capturas de grupos, registro, propuesta, historial y vista móvil revisadas; video MP4 1280 × 800 de **49 segundos**, 1.146.968 bytes, sin audio, regrabado el 4 oct con la interfaz de la comunidad. Todos los datos son ficticios y la base de prueba está separada del registro habitual.
- Evidencia resumida versionable: `demo/validacion-v1.json`; script reproducible: `scripts/verify_browser.py` sobre una demo vacía. Logs y bases se mantienen fuera de Git.

Esto verifica escritorio y tamaños móviles en navegador, no un teléfono físico ni la aceptación del equipo de catequesis. Las pruebas usaron una base ficticia separada; nunca la base de uso real.

## Prueba con el equipo de catequesis · 4 de octubre

El **domingo 4 de octubre en la mañana**, el mismo día en que se publicó el artículo, una catequista y la coordinadora de catequesis probaron la versión con períodos, grupos y responsables. Fue la primera prueba con personas del equipo usuario. No hubo fotos ni se guardó registro de la sesión.

| Punto | Resultado |
| --- | --- |
| Qué hicieron | Crearon el período y los registros de participantes |
| Qué valoraron | La **facilidad de acceso** y el **seguimiento** de cada participante |
| Qué pidieron | **Que los detalles de la formación se completen solos**, en lugar de escribirlos ellas |

El pedido de formación automática es la principal línea de trabajo que sale de la prueba. Una opción es ofrecer los temas de cada etapa como una lista para elegir, en lugar de texto libre.

Esta prueba no confirma las etapas y los requisitos reales ni es una aceptación formal del equipo de catequesis.
