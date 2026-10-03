# Sendero · Registro de catequesis

Una herramienta creada para **Noris Hernández**: registra el ingreso de los niños, su formación, los requisitos verificados y cada cambio de etapa. Interfaz en español, adaptable a teléfonos y computadoras, almacenamiento local e IA abierta mediante Ollama.

## Empezar

Requisitos: Python 3.11 o superior y [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run python -m sendero --demo
```

Abre **http://127.0.0.1:5081**. Consulta el código privado de acceso en `instance/access-code` dentro de este proyecto. No compartas ese archivo. `--demo` añade tres fichas ficticias solamente si el registro está vacío; omite esa opción para comenzar sin niños.

La primera vez, revisa **Etapas y requisitos**: los niveles iniciales son ejemplos, no normas de catequesis confirmadas. Puedes cambiar sus nombres, editar requisitos todavía no verificados, añadir requisitos y añadir etapas al final. Los requisitos ya verificados conservan su texto. El avance requiere todos los requisitos de la etapa actual y confirmación humana. Los nombres de los requisitos se conservan en el registro; el modelo solamente recibe sus números y estados.

## Uso diario

1. Registra el nombre del niño, fecha de ingreso y etapa. Responsable y contacto son opcionales.
2. Abre su ficha y registra clases, asistencias y observaciones.
3. Verifica los requisitos. El historial guarda verificaciones, correcciones y cambios.
4. Confirma el avance cuando corresponda; no se decide mediante IA.
5. Descarga un respaldo periódicamente. Archivar una ficha conserva su historia y permite reactivarla.

Una clase por niño y fecha; registrar de nuevo esa fecha corrige asistencia/tema y añade otro evento al historial. La fecha de ingreso no cambia desde el formulario de edición. La impresión incluye el recorrido y los datos de contacto: guarda el documento en un lugar privado.

## IA abierta local

Instala [Ollama](https://ollama.com/download), inicia su aplicación y descarga el modelo con `ollama pull qwen2.5-coder:3b`. Ollama debe estar ejecutándose en este equipo. El modelo predeterminado es `qwen2.5-coder:3b`; se eligió porque ya estaba disponible durante el desarrollo. Puedes seleccionar otro modelo local de pesos abiertos:

```sh
OLLAMA_MODEL=llama3:latest uv run python -m sendero
```

En la ficha pulsa **Preparar acompañamiento**. La IA elige y ordena dos o tres acciones de un catálogo revisado y selecciona una pregunta para conversar con el responsable, según los estados de los requisitos y la asistencia. No inventa libremente texto ni requisitos: el esquema restringe los valores y el servidor comprueba que pertenezcan al catálogo. Se guarda localmente con el modelo y el contexto numérico; si cambian los requisitos, las asistencias o la etapa, se marca como desactualizada. Puedes generar una nueva. El adaptador llama a `http://127.0.0.1:11434/api/chat` y transmite únicamente números de requisitos, estados, cantidad de clases y asistencias. No transmite nombres, responsables, contactos, temas ni observaciones. El modelo puede equivocarse: contrasta su texto con la lista de requisitos. La propuesta queda guardada sin modificar requisitos ni etapas. Puedes consultar las cinco propuestas más recientes. Sin Ollama, la aplicación mantiene todas sus funciones de registro y muestra un error claro al solicitar IA.

La IA abierta interviene en la preparación del seguimiento, sin depender de una API comercial ni enviar los registros a un servicio remoto. La licencia del modelo es independiente de la licencia del proyecto: [Qwen2.5-Coder-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct) utiliza `qwen-research`. Revisa también los términos al cambiar de modelo.

## Modularidad y crecimiento

- `sendero/__init__.py`: fábrica de aplicación, sesión, acceso y protección de solicitudes.
- `sendero/services.py`: validación, requisitos, formación y transiciones atómicas.
- `sendero/db.py` y `schema.sql`: persistencia y versión inicial del esquema.
- `sendero/routes.py`: API HTTP, configuración y respaldo.
- `sendero/ai.py`: adaptador sustituible de inferencia local.
- `sendero/static/`: interfaz, cliente API y estilos.
- `tests/`: comprobaciones de integridad, acceso, historial y minimización del contexto de IA.

Esta versión está pensada para una catequista en un equipo. La separación permite ampliar los módulos, pero no demuestra capacidad multiusuario ni carga alta. Para varias parroquias o acceso por internet: incorporar cuentas y roles, despliegue HTTPS, servidor de producción, migraciones incrementales y evaluar PostgreSQL. No exponer el servidor local en la red.

## Datos y respaldo

La base y los secretos viven en `instance/`, excluida de Git. El archivo SQLite no está cifrado: usa una cuenta de equipo privada, bloqueo de pantalla y cifrado del disco. La app no incluye gestión de consentimiento, adjuntos, borrado definitivo ni política de retención; deben definirse antes de usar registros reales de menores. Usa datos ficticios en cualquier demo pública.

**Descargar respaldo** crea una copia consistente SQLite, incluyendo fichas, requisitos, asistencias e historial. Para restaurar: detén Sendero, conserva la base actual, mueve sus archivos `.sqlite`, `-wal` y `-shm` fuera de `instance/`, copia el respaldo como `instance/sendero.sqlite` y vuelve a iniciar. No reemplaces una base mientras el servidor esté abierto.

## Verificación

```sh
uv run pytest -q
node --check sendero/static/app.js
node --check sendero/static/api.js
node --check sendero/static/plans.js
git diff --check
```

## Reto DEV

Proyecto nuevo para [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).

Antes de enviar: confirmar niveles con Noris, probar el recorrido con ella, grabar una demo con datos ficticios, publicar el repositorio y redactar el artículo en inglés usando la plantilla oficial. Crear el proyecto local no constituye una entrega al concurso.

Código asistido por IA. Licencia MIT; Flask y Ollama conservan sus licencias. Consulta [arquitectura y referencias](docs/arquitectura.md).

## Material para la presentación

La [demo grabada](demo/README.md) usa datos ficticios. El [artículo preparado](docs/dev-submission.md) y el [estado de entrega](docs/entrega-reto.md) distinguen la preparación de la publicación efectiva.
