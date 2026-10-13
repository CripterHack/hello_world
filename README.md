# HELLO WORLD · 2015

![HELLO WORLD synthetic calendar art](hello-world.svg)

**Arte generado con fechas históricas. No representa trabajo realizado en 2015.**

El diseño comienza exactamente el **domingo 8 de febrero de 2015**, con **98 commits vacíos** en fechas distintas hasta el **miércoles 2 de diciembre de 2015**, a las **12:00 UTC**. Las letras ocupan cinco filas, de domingo a jueves; el dibujo cabe completamente en 2015. El SVG es una representación, no una captura del perfil.

## Estado

- Diseño de 2015, SVG, manifiesto y generador preparados.
- Los **98 commits de esta versión todavía no están publicados**.
- Los **99 commits de 1995 se conservan intactos**, sin reescribir el historial.
- El propietario comprobó que su interfaz permite consultar desde 2015 y pidió este ajuste. La aparición final del nuevo dibujo sigue pendiente de publicación y comprobación.

## Archivos

- `dates.json`: 98 fechas y coordenadas; domingo = 0; primera semana empieza el 28/12/2014.
- `generate.py`: generador Python sin dependencias externas ni llamadas de red.
- `test_generate.py`: fechas, diseño, conservación del historial y prevención de duplicados.
- `hello-world.svg`: vista previa independiente del calendario real.
- Versión: `hello-world-2015-02-08-v2`.
- [Versión de 1995 conservada](https://github.com/CripterHack/hello_world/tree/75cd299a51066d9d8c3a246ea63d2ea4d63080fd).

El generador permite añadir 2015 sobre el historial de 1995, pero rechaza repetir esta misma versión, incluso si detecta solamente algunos de sus commits. Los commits de documentación mantienen sus fechas actuales.

## Pruebas y vista previa

Se requiere Python 3 y Git:

```sh
python3 -m unittest -v test_generate.py
python3 generate.py --output /tmp/hello-world-2015-preview
```

La carpeta de salida no debe contener archivos generados anteriormente: se rechaza sobrescribirlos.

## Generar los commits en un clon

Verifica la rama predeterminada (`master`), un árbol limpio y tu identidad Git. El script lee `git config user.name` y `git config user.email`, sin contener direcciones personales ni consultar GitHub para comprobar su asociación.

El propietario autorizó usar la identidad ya atribuida a su cuenta. Para otras reproducciones, usa un correo asociado y, si deseas privacidad, tu dirección `noreply` exacta de [GitHub → Settings → Emails](https://github.com/settings/emails). No presupongas que una dirección construida está vinculada.

```sh
git switch master
git pull --ff-only
python3 generate.py --append-history "$PWD"
git log -5 --format='%h %aI %cI %s'
```

El script añade commits vacíos sin modificar archivos, reescribir historial ni publicar datos. Autor y committer comparten fechas históricas, anteriores a las de sus padres recientes en el grafo Git. Después de revisar el resultado:

```sh
git push origin master
```

No uses `--force`. Si cambia el remoto, revisa la divergencia antes de continuar. No ejecutes de nuevo una versión publicada.

## Calendario de GitHub

GitHub usa la fecha del autor y exige un correo asociado y commits en la rama predeterminada de un repositorio independiente (o `gh-pages`). El calendario combina otras contribuciones de la cuenta; actividad existente en 2015 podría alterar el dibujo y sus colores. El SVG garantiza una vista independiente del diseño.

La actualización puede tardar hasta 24 horas. La vista inicial muestra el último año: selecciona 2015 para consultar este diseño. No se modifica la fecha real de creación de la cuenta ni del repositorio.

Referencias: [fechas en Git](https://git-scm.com/docs/git-commit), [criterios de contribuciones](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference), [visualización histórica](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/viewing-contributions-on-your-profile), [contribuciones ausentes](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions).
