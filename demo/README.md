# Demo · Sendero

[Ver el video (MP4)](sendero-demo.mp4)

Versión actual: 4 de octubre de 2026, 49 segundos, 1280 × 800, sin audio. La interfaz identifica a la comunidad de la Capilla Nuestra Señora de Lourdes; ninguna persona real aparece en pantalla. Grabación real de acceso de prueba, creación de período y grupo, participante con dos responsables, asistencia y tema, observación, IA local, revisión y recarga. Interfaz en español. Todos los datos son ficticios; el código `demo-ficticia` corresponde únicamente a la demo aislada.

Capturas actualizadas: `grupos.png`, `registro.png`, `ai-plan.png`, `recorrido.png` y `movil.png`. `validacion-v1.json` registra las comprobaciones finales de navegador. `evaluacion-ia.json` conserva los tres casos de inferencia de la versión anterior, no se presenta como una nueva evaluación.

Para una demo aislada con fichas iniciales:

```sh
uv run python -m scripts.demo_server
```

Abre `http://127.0.0.1:5082`; el acceso es el código privado local. Su base `artifacts/demo.sqlite` queda fuera de Git.

Para reproducir el recorrido grabado, usa una ruta nueva de base de datos vacía:

```sh
uv run python -m scripts.demo_server --database artifacts/demo-v1-nueva.sqlite --port 5083 --empty --test-code
```

En otra terminal, con `playwright` y Chromium instalados en ese intérprete, ejecuta `python3 scripts/verify_browser.py`. Esta comprobación llama a Ollama real y regenera imágenes y video WebM. La conversión a MP4 se realiza con FFmpeg. El script requiere una base vacía y Ollama con el modelo predeterminado disponible. No uses el modo `--test-code` con datos reales ni expongas el servidor en internet.

La prueba móvil usa emulación de tamaño y controles táctiles en Chromium. Falta la prueba en un dispositivo físico.
