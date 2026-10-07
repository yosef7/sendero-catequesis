# Sendero · Registro de catequesis

Una herramienta para el equipo de catequesis de la comunidad de la **Capilla Nuestra Señora de Lourdes**, en Valle de Urraca, San Miguelito (Panamá): organiza períodos y grupos, registra participantes y responsables, su formación, los requisitos verificados y cada cambio de etapa. Interfaz en español, adaptable a teléfonos y computadoras, almacenamiento local e IA abierta mediante Ollama.

## Instalar e iniciar el proyecto

Requisitos: Python 3.11 o superior y [uv](https://docs.astral.sh/uv/). Ollama es opcional para el registro y necesario para generar propuestas de IA.

### 1. Abrir el proyecto e instalar las dependencias

Clona el repositorio e instala las dependencias:

```sh
git clone https://github.com/yosef7/sendero-catequesis.git
cd sendero-catequesis
uv sync
```

`uv sync` prepara el entorno virtual y las dependencias; no hace falta activar `.venv` para los comandos siguientes.

### 2. Iniciar Sendero

Desde la carpeta del proyecto:

```sh
uv run python -m sendero
```

Deja esa terminal abierta y visita **http://127.0.0.1:5081**. El primer inicio crea la base local, las etapas de ejemplo y el código privado de acceso. Los siguientes inicios conservan los registros y aplican las migraciones pendientes.

### 3. Consultar el código de acceso

En otra terminal, desde la misma carpeta:

```sh
cat instance/access-code
```

Copia el código en la pantalla de acceso. No compartas el archivo ni incluyas su contenido en capturas públicas.

### 4. Detener y volver a iniciar

Pulsa **Ctrl+C** en la terminal donde corre Sendero. Para volver a abrirlo, ejecuta otra vez `uv run python -m sendero`; los datos permanecen en `instance/`.

Si el puerto 5081 ya está ocupado, detén la instancia anterior o utiliza otro:

```sh
uv run python -m sendero --port 5084
```

En ese caso abre **http://127.0.0.1:5084**. El servidor escucha únicamente en este equipo; esa dirección no permite acceder desde un teléfono distinto.

### Probar con datos ficticios

Para añadir tres fichas de ejemplo a una base vacía:

```sh
uv run python -m sendero --demo
```

`--demo` utiliza la base habitual y solo añade fichas si no hay participantes. Para probar en una base separada, consulta las instrucciones de la [demo aislada](demo/README.md).

La primera vez, revisa **Etapas y requisitos**: los niveles iniciales son ejemplos, no normas de catequesis confirmadas. Puedes cambiar sus nombres, editar requisitos todavía no verificados, añadir requisitos y añadir etapas al final. Los requisitos ya verificados conservan su texto. El avance requiere todos los requisitos de la etapa actual y confirmación humana. Los nombres de los requisitos se conservan en el registro; el modelo solamente recibe sus números y estados.

## Uso diario

1. Accede con el código privado del equipo de catequesis.
2. En **Períodos y grupos**, crea el período con inicio y cierre y añade sus grupos.
3. En **Niños y formación**, registra el participante, fecha de ingreso, etapa, grupo y hasta cinco responsables con vínculo y contacto. Los contactos son opcionales.
4. Abre la ficha y registra asistencia, tema y observaciones. Selecciona la inscripción para asociar la clase a su grupo y período.
5. Consulta las inscripciones e historia en la ficha; filtra el listado por grupo. Una ficha puede conservar inscripciones en varios períodos sin duplicar al participante.
6. Pulsa **Preparar acompañamiento** para obtener un resumen de cantidades, pendientes y acciones sugeridas. El equipo de catequesis puede **Marcar como revisada** una propuesta vigente; la revisión queda en el historial.
7. Verifica los requisitos y confirma el avance cuando corresponda.
8. Descarga un respaldo periódicamente. Archivar una ficha conserva su historia y permite reactivarla.

Consulta los [requisitos y criterios de aceptación](docs/requisitos-v1.md). Las fichas anteriores se conservan sin grupo; usa **Inscribir en otro grupo** para vincularlas a un período con la fecha de inscripción correspondiente. Las migraciones también conservan el responsable original, las clases y propuestas anteriores.

Una clase por niño y fecha; registrar de nuevo esa fecha corrige asistencia/tema y añade otro evento al historial. La fecha de ingreso no cambia desde el formulario de edición. La impresión incluye el recorrido y los datos de contacto: guarda el documento en un lugar privado.

## IA abierta local

Instala [Ollama](https://ollama.com/download), inicia su aplicación y descarga el modelo con `ollama pull qwen2.5-coder:3b`. Ollama debe estar ejecutándose en este equipo. El modelo predeterminado es `qwen2.5-coder:3b`; se eligió porque ya estaba disponible durante el desarrollo. Puedes seleccionar otro modelo local de pesos abiertos:

```sh
OLLAMA_MODEL=llama3:latest uv run python -m sendero
```

En la ficha pulsa **Preparar acompañamiento**. La IA elige y ordena dos o tres acciones de un catálogo revisado y selecciona una pregunta para conversar con el responsable, según los estados de los requisitos y la asistencia. No inventa libremente texto ni requisitos: el esquema restringe los valores y el servidor comprueba que pertenezcan al catálogo. Se guarda localmente con el modelo y el contexto numérico; si cambian los requisitos, las asistencias o la etapa, se marca como desactualizada. Puedes generar una nueva. El adaptador llama a `http://127.0.0.1:11434/api/chat` y transmite únicamente números de requisitos, estados, cantidad de clases y asistencias. No transmite nombres, responsables, contactos, temas ni observaciones. El modelo puede equivocarse: contrasta su texto con la lista de requisitos. La propuesta queda guardada sin modificar requisitos ni etapas. Puedes consultar las cinco propuestas más recientes. Sin Ollama, la aplicación mantiene todas sus funciones de registro y muestra un error claro al solicitar IA.

El resumen de asistencias y requisitos y los números pendientes se calculan a partir del registro; el modelo selecciona y prioriza las acciones y la pregunta. La revisión humana se guarda con fecha, sin modificar formación. El endpoint de resumen también valida el catálogo. La integración sigue el [contrato de salida estructurada de Ollama](https://docs.ollama.com/capabilities/structured-outputs).

La IA abierta interviene en la preparación del seguimiento, sin depender de una API comercial ni enviar los registros a un servicio remoto. La licencia del modelo es independiente de la licencia del proyecto: [Qwen2.5-Coder-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct) utiliza `qwen-research`. Revisa también los términos al cambiar de modelo.

## Modularidad y crecimiento

- `sendero/__init__.py`: fábrica de aplicación, sesión, acceso y protección de solicitudes.
- `sendero/services.py`: validación, requisitos, formación y transiciones atómicas.
- `sendero/db.py` y `schema.sql`: persistencia y versión inicial del esquema.
- `sendero/routes.py`: API HTTP, configuración y respaldo.
- `sendero/ai.py`: adaptador sustituible de inferencia local.
- `sendero/static/`: interfaz, cliente API y estilos.
- `tests/`: comprobaciones de integridad, acceso, historial y minimización del contexto de IA.

Esta versión está pensada para un equipo de confianza con un código de acceso compartido; aún no hay cuentas individuales por catequista. La separación permite ampliar los módulos, pero no demuestra capacidad multiusuario ni carga alta. Para varias parroquias o acceso por internet: incorporar cuentas y roles, despliegue HTTPS, servidor de producción, migraciones incrementales y evaluar PostgreSQL. No exponer el servidor local en la red.

## Datos y respaldo

La base y los secretos viven en `instance/`, excluida de Git. El archivo SQLite no está cifrado: usa una cuenta de equipo privada, bloqueo de pantalla y cifrado del disco. La app no incluye gestión de consentimiento, adjuntos, borrado definitivo ni política de retención; deben definirse antes de usar registros reales de menores. Usa datos ficticios en cualquier demo pública.

**Descargar respaldo** crea una copia consistente SQLite, incluyendo períodos, grupos, inscripciones, responsables, fichas, requisitos, asistencias, propuestas, revisiones e historial. Para restaurar: detén Sendero, conserva la base actual, mueve sus archivos `.sqlite`, `-wal` y `-shm` fuera de `instance/`, copia el respaldo como `instance/sendero.sqlite` y vuelve a iniciar. No reemplaces una base mientras el servidor esté abierto.

## Verificación

```sh
uv run pytest -q
node --check sendero/static/app.js
node --check sendero/static/api.js
node --check sendero/static/plans.js
git diff --check
```

## Reto DEV

Sendero se creó para el [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01) de DEV.

El [artículo en DEV](https://dev.to/arnulfo_07/sendero-helping-noris-prepare-each-childs-next-step-with-local-open-ai-4gl3) explica el proyecto y sus decisiones de diseño. El dom 4 oct, una catequista y la coordinadora de catequesis hicieron la primera prueba: valoraron la facilidad de acceso y el seguimiento, y pidieron que los detalles de la formación se completen solos ([validación](docs/validacion.md#prueba-con-el-equipo-de-catequesis--4-de-octubre)). Confirmar las etapas y los requisitos reales sigue pendiente.

Código asistido por IA. Licencia MIT; Flask y Ollama conservan sus licencias. Consulta [arquitectura y referencias](docs/arquitectura.md).

## Demo

La [demo grabada](demo/README.md) usa datos ficticios.

## Continuidad

Sendero tiene una sola persona mantenedora y un único equipo usuario previsto: el de catequesis de la capilla. La [evaluación de sostenibilidad](docs/sostenibilidad.md) enumera lo que falta para que el proyecto siga siendo útil después del reto y no dependa de una sola persona.
