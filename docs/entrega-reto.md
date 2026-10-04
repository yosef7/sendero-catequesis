# Entrega al reto · Estado verificable

Reto: [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01), evento 78.

Ventana en Panamá: jueves 1 de octubre de 2026, 9:00 p. m., hasta lunes 5 de octubre de 2026, 1:59 a. m. Fuente: reglas oficiales, 2 de octubre 02:00 UTC a 5 de octubre 06:59 UTC.

## Estado verificado · 4 de octubre

| Elemento | Estado | Cómo se verificó |
| --- | --- | --- |
| Pruebas | ✅ 26 aprobadas; `node --check` de los tres scripts y `git diff --check` sin errores | Ejecución local del 4 oct |
| Ampliación v1 | ✅ Versionada y enviada el 4 oct a las 9:45 a. m.: `762acc3` (aplicación) y `8678396` (documentación, demo y validación) | `git log` y `git fetch` |
| Repositorio remoto | ⏳ **Privado**; `origin/main` en `8678396`, con 5 commits | `gh repo view` y `git fetch` |
| Artículo DEV 4793109 | ⏳ **Borrador** (`published: false`) con `devchallenge`, `weekendchallenge` y `hf26challenge`; texto igual a [`dev-submission.md`](dev-submission.md) | `get_my_articles` de DevRelay |
| Reto 78 | Abierto hasta el **lun 5 oct, 1:59 a. m. (Panamá)** | `get_challenge_details` de DevRelay |
| Prueba con Noris | ⏳ Sin realizar | — |

> [!WARNING]
> **No incluir el Directorio en el repositorio público.** `docs/DIRECTORIO-PARA-LA-CATEQUESIS-2022.pdf` y su transcripción `.md` reproducen una obra publicada con derechos de autor. Quedaron fuera de los commits del 4 oct y ahora están en `.gitignore`, así que un `git add .` futuro no los publica.

## Bases del reto consultadas el 4 de octubre

Fuente: `full_details` del reto 78 en DevRelay.

- **Enunciado común:** *"Build something with open-source AI at its core"*. Los cinco retos de Hacktoberfest en DEV comparten el enunciado y cambian de tema cada lunes. El tema de este fin de semana es *Build for a Friend*: resolver un problema real de una persona concreta. *"Bonus points if you actually hand it over and tell us what they said."*
- **Requisitos:** proyecto nuevo construido durante la ventana, una entrada por reto, plantilla del anuncio y etiqueta obligatoria `#hf26challenge`.
- **Criterios:** calidad del texto (el de mayor peso), pertinencia con el enunciado y el tema, creatividad, ejecución técnica y, si se entra en una categoría, uso de la tecnología del patrocinador.
- **Premios:** 2450 USD entre 17 ganadores. Premio general de 250 USD con DEV++ y badge; 6 categorías destacadas de 200 USD y 10 categorías de 100 USD. Toda entrega válida recibe un badge de participación. La fecha de anuncio de ganadores sigue sin publicar.
- **Categorías:** Sendero no entra en ninguna, porque no usa tecnologías de patrocinadores. Compite por el premio general.

## Material preparado

- Proyecto nuevo: registro local de formación para Noris.
- IA abierta: inferencia local de pesos abiertos con Ollama, selección y priorización de preparación en un catálogo revisado, guardado del contexto y detección de desactualización.
- Video local actualizado: `demo/sendero-demo.mp4`, 33,24 s, con datos ficticios; incluye períodos, grupos, dos responsables y revisión humana de IA.
- Código: preparado para `yosef7/sendero-catequesis`, licencia MIT. El modelo conserva su licencia `qwen-research`.
- Artículo en inglés: `docs/dev-submission.md`, plantilla oficial, etiquetas `devchallenge`, `weekendchallenge`, `hf26challenge`, asistencia de IA declarada.
- Sin categorías de patrocinadores: no se atribuye uso de herramientas que no participaron en la construcción.
- Sin transcript público: es opcional y no forma parte de esta entrega.

## Publicación

El repositorio [yosef7/sendero-catequesis](https://github.com/yosef7/sendero-catequesis) fue creado **privado** y sus dos commits iniciales se enviaron a `origin/main`: `259c12c` (aplicación) y `84ae89b` (demo y presentación). Después se envió `2c83b35`, que registra el repositorio privado y el borrador de DEV. La visibilidad privada y el MP4 remoto de 901.956 bytes se verificaron mediante GitHub.

El artículo DEV **4793109** está guardado como borrador y se confirmó en la lista de artículos no publicados del usuario `arnulfo_07`, con las tres etiquetas requeridas. La asistencia de IA está declarada en el texto y se envió con el valor predeterminado `some_ai` de DevRelay. No se publicó.

Los enlaces del artículo apuntan al destino previsto; sus enlaces al código y demo apuntan al destino previsto y quedarán accesibles públicamente al cambiar la visibilidad del repositorio. El cambio de visibilidad y la publicación del artículo se verifican antes de marcar la entrega completa.

La elegibilidad personal no se ha certificado: el participante debe cumplir las condiciones oficiales. Los jueces deciden la validez de la entrega. Tampoco se ha documentado aún una prueba con Noris: su reacción no se inventa en el artículo.

## Revisión antes de publicar

Plazo: **antes del lun 5 oct, 1:59 a. m. (Panamá)**. Cada paso depende del anterior.

- [x] Dejar fuera de los commits el PDF del Directorio y su transcripción (ver el aviso de [estado verificado](#estado-verificado--4-de-octubre)). `✅ 4 oct`
- [x] Hacer commit de la ampliación v1 y enviarla a `origin/main`, con `demo/grupos.png` y `demo/validacion-v1.json`, que el artículo enlaza. `✅ 4 oct` (`8678396`)
- [x] Revisar el artículo y el video preparados: cifras contrastadas con `demo/validacion-v1.json`, 26 pruebas aprobadas, video de 33,24 s idéntico al remoto. `✅ 4 oct`
- [ ] Hacer público el repositorio y comprobar que el código, el video y las capturas abren sin iniciar sesión.
- [ ] Publicar el artículo 4793109 con las tres etiquetas.
- [ ] Confirmar desde DEV la URL pública, el estado publicado, la hora y las etiquetas.
- [ ] Anotar la URL publicada en este archivo y en el libro de retos personales del repositorio Hacktoberfest (`docs/06-mlh/stickers-2026.md`), y comprobar después el sticker del Launch Weekend en [hacktoberfest.com/my](https://hacktoberfest.com/my).

## Actualización de la primera versión funcional · 3 de octubre

Actualización del 4 oct: la ampliación se versionó y se envió a `origin/main` (`762acc3` y `8678396`); el remoto sigue privado. Texto original del 3 oct: la ampliación está **local, sin commit ni push**: requisitos, flujo con períodos/grupos, responsables múltiples, asistencia asociada, revisión humana de IA, 26 pruebas, video y capturas actualizados. El remoto sigue privado y conserva la versión inicial. Los enlaces remotos del artículo todavía requieren publicar estos cambios; el MP4 remoto verificado anteriormente no representa esta nueva grabación.

La revisión en Chromium y móvil emulado concluyó; quedan teléfono físico y aceptación de Noris. Se actualiza el borrador DEV existente, no se crea una segunda entrada. El cambio de visibilidad y la publicación del artículo siguen pendientes. El reto 78 sigue abierto y cierra el 5 de octubre a la 1:59 a. m. de Panamá, según los detalles oficiales consultados en DevRelay durante esta ampliación.

El servidor habitual `http://127.0.0.1:5081` ya carga la ampliación; su base se migró a versión 3 después de un respaldo privado, con preservación de los registros verificada. La demo aislada queda en `http://127.0.0.1:5083` con acceso `demo-ficticia`.

DevRelay perdió inicialmente la conexión al actualizar el artículo. Una lectura posterior confirmó que aún conservaba el texto anterior; se repitió entonces la actualización de la misma entrada 4793109 y DEV confirmó el nuevo contenido con `published: false` y `some_ai`.
