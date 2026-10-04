# Primera versión funcional · Requisitos

Fecha: 3 de octubre de 2026. Fuente de alcance: instrucciones del usuario y comportamiento existente de Sendero. Los usuarios previstos son el equipo de catequesis de la Capilla Nuestra Señora de Lourdes (Valle de Urraca, San Miguelito). No se le atribuyen entrevistas ni aceptación de esta versión.

## Flujo y aceptación

| Paso | Comportamiento verificable |
| --- | --- |
| Acceso del equipo | Código privado, sesión y CSRF; API protegida sin sesión. |
| Crear período | Nombre único, inicio y cierre válidos; admite períodos futuros. |
| Crear grupo | Pertenece a un período; nombre único dentro del período. |
| Inscribir participante | Nombre, fecha de ingreso, etapa y grupo; inscripción dentro del período y posterior o igual al ingreso. Una ficha puede tener varias inscripciones. |
| Responsables | Hasta cinco con nombre, vínculo y contacto opcionales. No se aceptan contactos huérfanos sin nombre en el formulario. |
| Asistencia y temas | Presente/ausente, fecha y tema; inscripción propia y fecha dentro de su período y posterior o igual a la inscripción. Una clase por participante y día. Corregir añade un evento. |
| Historial | Ingreso, inscripciones, clases, observaciones, requisitos, avances y revisiones de IA; persiste después de recargar y archivar. |
| IA abierta | Ollama local configurable; resumen de cantidades y pendientes del registro, acciones y pregunta seleccionadas por el modelo de un catálogo validado. Sin nombres, contactos, temas ni observaciones en el prompt. |
| Revisión humana | Marcar una propuesta vigente como revisada guarda fecha y evento. Propuesta desactualizada no puede revisarse; no modifica formación. |
| Respaldo | Copia SQLite consistente con todas las tablas; migraciones preservan fichas y datos anteriores. |
| Computadora y celular | Recorrido con datos ficticios en Chromium, vista de escritorio y tamaños móviles, edición táctil emulada y ausencia de desbordamiento horizontal. |
| Entrega del reto | Repositorio MIT, demo ficticia y artículo en inglés con asistencia de IA declarada; preparación y publicación se registran por separado. |

## Decisiones de esta versión

- Un espacio local para el equipo de catequesis, con un código de acceso compartido. Períodos y grupos organizan la formación; las etapas y sus requisitos son independientes del calendario.
- El grupo se puede omitir en fichas históricas. Para el recorrido nuevo completo se crea el período y grupo antes de inscribir.
- Inicio de inscripción igual al ingreso al crear ficha; inscripciones posteriores tienen su propia fecha. Una misma ficha puede pertenecer a varios grupos, pero solo se registra una clase al día en esta versión.
- Nombres, fechas, vínculo y contacto son los datos mínimos del flujo. No se añadieron identificación oficial, sacramentos, adjuntos ni otras obligaciones no confirmadas.
- Los niveles y requisitos iniciales siguen siendo ejemplos. El documento local de referencia no establece por sí solo requisitos operativos de la parroquia.
- La revisión de una propuesta acredita una acción del equipo de catequesis dentro de la app; no equivale a la aceptación del producto ni certifica la calidad del consejo.

## Límites pendientes

Prueba en teléfono físico y aceptación con el equipo de catequesis; confirmación de etapas; procedimientos de consentimiento y retención antes de registrar datos reales de menores. Acceso multiusuario, uso del teléfono por red y despliegue HTTPS no forman parte del servidor local actual. No se afirma que la demo sea un servicio público alojado.
