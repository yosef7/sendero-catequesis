# Sostenibilidad · Evaluación al 4 de octubre de 2026

Evaluación de la continuidad de Sendero según dos dimensiones: **técnica** (¿otra persona podría mantener el código?) y **proyecto de reto** (¿sigue vivo cuando termina el Weekend Challenge?). Cada punto se marcó con evidencia comprobada el 4 oct, no con intenciones.

## Riesgos principales

1. **Datos de menores sin procedimiento de consentimiento ni retención.** Es el bloqueo para usar Sendero con registros reales. La app no gestiona consentimiento, borrado definitivo ni retención, y la base SQLite no está cifrada. Mientras no exista ese procedimiento, Sendero solo debe usarse con datos ficticios.
2. **Una sola persona lo sabe todo.** Hay un autor (5 commits de José Arnulfo R. H.), una cuenta con acceso al repositorio (`yosef7`) y una base con su código de acceso en un único equipo. Si esa persona no está disponible, el equipo de catequesis no tiene cómo instalar, actualizar ni restaurar Sendero.
3. **La continuidad no depende del reto, sino de la comunidad.** Las rondas siguientes de DEV exigen proyectos nuevos, así que el reto no le da a Sendero una fecha de continuidad. Sin una prueba de aceptación con el equipo de catequesis, nada garantiza que el proyecto se use después del 5 oct.

## Dimensión técnica

| Punto | Estado | Evidencia o siguiente paso |
| --- | --- | --- |
| Personas con commits | ❌ 1 | `git shortlog -sn --all`: 5 commits, un autor. Siguiente paso: buscar una segunda persona de confianza (de la parroquia o de la comunidad técnica) que sepa instalar y respaldar Sendero |
| Acceso administrativo al repositorio | ❌ 1 | Colaboradores: solo `yosef7`. Siguiente paso: invitar a la segunda persona cuando exista |
| Accesos y secretos documentados | ⚠️ Parcial | El README explica dónde viven `instance/access-code` e `instance/secret`, pero no quién más los conoce. Siguiente paso: acordar con el equipo de catequesis dónde se guarda una copia del código de acceso |
| `README.md` | ✅ | Explica qué hace Sendero, cómo instalarlo, iniciarlo, respaldarlo y verificarlo |
| `LICENSE` | ✅ | MIT. El modelo `qwen2.5-coder:3b` conserva su licencia `qwen-research`, que se revisa al cambiar de modelo |
| `CONTRIBUTING.md` | ❌ | No existe. Siguiente paso: crearlo si el repositorio se hace público y se aceptan contribuciones; puede remitir a la sección «Verificación» del README |
| `CODE_OF_CONDUCT.md` | ❌ | No existe. Solo hace falta si se aceptan contribuciones externas |
| Decisiones de arquitectura | ✅ | [`arquitectura.md`](arquitectura.md), [`requisitos-v1.md`](requisitos-v1.md) y [`validacion.md`](validacion.md) registran las decisiones y por qué se restringió la salida de la IA |
| Pruebas automatizadas | ✅ | 26 pruebas aprobadas el 4 oct: acceso, migraciones, transacciones, revisión humana y contexto de IA |
| CI | ❌ | No hay `.github/workflows`. Siguiente paso: un flujo de GitHub Actions que ejecute `uv run pytest -q` y `node --check` en cada push |
| Instalación solo con el README | ⚠️ Parcial | Los pasos están documentados, pero no se han probado en un equipo distinto al del autor. Siguiente paso: instalarlo en la computadora que use la capilla siguiendo solo el README y anotar cada paso tácito que aparezca |
| Dependencias | ✅ | `uv.lock` presente. Una dependencia directa (`flask` 3.1.3) y `pytest` para desarrollo. `pip-audit` el 4 oct: *"No known vulnerabilities found"* |
| Issues y PR abiertos | ✅ | Ninguno |

## Dimensión de proyecto de reto

| Punto | Estado | Evidencia o siguiente paso |
| --- | --- | --- |
| Persona que dijo «yo le sigo» | ⚠️ Implícito | El autor mantiene el proyecto, pero no hay un compromiso escrito para después del 5 oct. Siguiente paso: anotar aquí quién lo mantiene y hasta cuándo |
| Comunidad usuaria real | ✅ | El equipo de catequesis de la Capilla Nuestra Señora de Lourdes, en Valle de Urraca, San Miguelito. El problema existe fuera del reto: llevar el registro de formación de cada niño |
| Aceptación de la comunidad | ❌ | No se ha probado con el equipo de catequesis ni se han confirmado sus etapas. Siguiente paso: sesión con el equipo para revisar etapas y requisitos y recorrer el flujo diario |
| Corre fuera del entorno del reto | ✅ | Funciona sin internet una vez descargados el modelo y las dependencias; no usa servicios de pago ni créditos que venzan |
| Respaldo | ⚠️ Parcial | Existe **Descargar respaldo**, pero es manual y no hay un lugar acordado para guardar las copias. Siguiente paso: acordar con el equipo de catequesis la frecuencia y el destino del respaldo |
| Siguiente paso fijado tras el reto | ❌ | Ninguno con fecha. Siguiente paso: fijar la sesión con el equipo de catequesis y decidir si Sendero pasa a uso real o queda como prototipo documentado |
| Contenido de terceros | ✅ | El PDF del *Directorio para la catequesis* y su transcripción son una obra con derechos de autor. Se conservan en `docs/` solo como consulta local y están excluidos en `.gitignore` |

## Decisión pendiente

Si la comunidad adopta Sendero, el orden es: procedimiento de consentimiento y retención, instalación en la computadora de la capilla con respaldo acordado, y una segunda persona con acceso. Si no se adopta, el README debe indicar que el proyecto es un prototipo archivado y qué se aprendió, para que sirva a otra catequista o a otra parroquia.
