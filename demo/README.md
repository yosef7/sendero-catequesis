# Demo · Sendero

[Ver el video (MP4)](sendero-demo.mp4)

Duración: 36 segundos. Captura real de la aplicación con generación local mediante Ollama; interfaz en español y textos explicativos en inglés. Sin narración. Todas las fichas, responsables, observaciones y requisitos mostrados son ficticios o ejemplos.

El video muestra: registro de niños, preparación con IA, verificación humana, cambio de etapa, asistencia, observaciones, persistencia al recargar y configuración del recorrido. No se grabaron el inicio de sesión, códigos de acceso ni datos reales de menores.

Las capturas acompañan la demo:

- `registro.png`: listado de niños ficticios.
- `ai-plan.png`: propuesta con el modelo y los datos de progreso.
- `recorrido.png`: historial y formación.
- `movil.png`: vista adaptable al teléfono.
- `evaluacion-ia.json`: tres casos ficticios probados realmente con Ollama. La respuesta del modelo está incluida; estos casos no constituyen una evaluación exhaustiva.

Para generar un entorno de demostración separado del registro habitual:

```sh
uv run python -m scripts.demo_server
```

Abre `http://127.0.0.1:5082`. El código de acceso es el del proyecto local; las cookies de sesión usan el mismo host. La base de demo está en `artifacts/demo.sqlite` y queda fuera de Git. No expongas este servidor en internet.
