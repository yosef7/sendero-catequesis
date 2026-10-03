# Validación de la primera versión

Fecha: 3 de octubre de 2026. Todos los registros utilizados fueron ficticios.

- `uv run pytest -q`: **9 pruebas aprobadas**. Acceso/CSRF, validaciones sin escrituras parciales, historial y avance de etapa, corrección de asistencia, archivado reversible, configuración, respaldo, contexto de IA y hosts/cabeceras.
- El respaldo descargado se abrió con SQLite: `PRAGMA integrity_check` devolvió `ok`, con fichas y eventos presentes.
- Navegador: creación de ficha, verificación, confirmación de avance, asistencia, observación y persistencia después de recargar. Configuración de etapas accesible.
- Capturas de escritorio y móvil revisadas. A 390 píxeles no hubo desbordamiento horizontal en el registro.
- Ollama respondió realmente con `qwen2.5-coder:3b` a un contexto numérico de la ficha ficticia. No se enviaron campos personales. Esta prueba confirma conectividad e inferencia, no calidad garantizada de los resúmenes.
- Sintaxis de los dos módulos JavaScript comprobada con Node.
- Base, código de acceso y artefactos de pruebas excluidos de Git.

Pendiente: confirmación de etapas reales por Noris, prueba de aceptación con ella, prueba de carga, cuentas multiusuario y publicación del repositorio/demo/artículo. El servidor actual es local y no está preparado para exposición en internet.

La revisión visual se completó con el navegador conectado. Un intento independiente de arrancar Chrome terminó por timeout; no se cuenta como una validación aprobada.

## Ampliación para la entrega al reto · 3 de octubre

- `uv run pytest -q`: **18 pruebas aprobadas** tras incorporar las propuestas de acompañamiento. Se añadieron persistencia, detección de contexto cambiado, salida inválida sin escritura, pertenencia al catálogo, aceptación de una respuesta válida y migración desde versión 1 preservando la ficha existente.
- Se probaron tres casos con Ollama real y `qwen2.5-coder:3b`: sin clases, requisitos pendientes y requisitos verificados. Las tres respuestas finales fueron válidas. Las duraciones observadas fueron 41,87 s, 4,78 s y 3,61 s; la primera incluye carga del modelo. El modelo puede priorizar acciones generales; no se demuestra que siempre escoja la mejor prioridad.
- La primera variante de redacción libre devolvió detalles no sustentados; se sustituyó por selección/priorización dentro de un catálogo revisado. Un intento con `llama3:latest` agotó el tiempo de espera; no se cuenta como comparación de calidad ni modelo validado.
- Grabación real de 36,2 s en una base ficticia separada: generación local, verificación, propuesta desactualizada, avance, asistencia, observación y persistencia después de recargar. **Cero errores de JavaScript**. A 390 px no hubo desbordamiento horizontal.
- MP4 H.264 de 1280 × 800, sin audio, con explicaciones en inglés. Capturas limpias del registro, propuesta, recorrido y teléfono.
- No se modificó la documentación pendiente del repositorio Hacktoberfest. Los logs temporales del navegador se mantienen en `artifacts/`, ignorado.

Esto demuestra la ejecución local y el material preparado; el estado de publicación se registra aparte en `docs/entrega-reto.md`. No confirma aceptación por los jueces ni retroalimentación de Noris.
