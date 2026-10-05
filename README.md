# Carola Page · Paisajismo

Vive dentro de `Dropbox/ process trabajo/Carola Page/sitio web/`.

Dos opciones sobre el mismo diseño de Figma
(`KOP4jow3oc1qL1ould4uPJ`, archivo *Carola Page*). HTML y CSS planos, sin build
ni dependencias. Se publican por separado: eliges una y subes esa carpeta.

```
web/       ← el sitio completo, las seis pantallas del Figma
landing/   ← alternativa: una sola página con lo esencial
```

## web/ — el sitio completo

Siete páginas, todas calcadas del Figma:

| Archivo | Pantalla del Figma |
|---|---|
| `index.html` | Home |
| `proyectos.html` | Proyectos (destacados + archivo con filtros) |
| `proyecto-<slug>.html` | Seis fichas de proyecto, una por obra |
| `noticia-<slug>.html` | Once fichas de exposición, clase o charla |
| `quienes-somos.html` | Quiénes Somos (bio, cronología, oficina, qué hacemos) |
| `noticias.html` | listado de noticias |
| `noticia.html` | Días de Campo en Las Cardillas |
| `contacto.html` | Contacto |

La sección de talleres vive solo en Noticias. La cabecera y el pie están
repetidos en cada archivo: si cambias uno, cámbialos todos.

### Los once proyectos

**Residenciales** (de `seleccion proyectos`, en el orden y con el título de cada carpeta):

| # | Proyecto | Fotos | Narrativa |
|---|---|---|---|
| 1 | Punta Pite | portada + 17 | del Word (Casa Nico) |
| 2 | Aguas Claras AP | portada + 7 | **pendiente** |
| 3 | Aguas Claras Sur LV | portada + 8 | **pendiente** |
| 4 | Aguas Claras Norte PI | portada + 19 | del Word (Casa PI) |
| 5 | El Pangue CT | portada + 13 | del Word |
| 6 | Marbella CM | portada + 6 | **pendiente** |

Cada `PORTADA` de la carpeta es la foto principal: abre la ficha y es la que sale
en el home y en Proyectos. El resto va en el orden del prefijo numérico del
archivo. Los datos y los textos están en `proyectos.py` (junto al generador), no
repartidos por el HTML.

**Comerciales** (de `material/COMERCIAL`, carpetas 0 a 4):

| # | Proyecto | Fotos | Narrativa |
|---|---|---|---|
| 0 | Edificio Manuel Montt | portada + 3 | **falta** |
| 1 | Edificio Francisco de Aguirre | portada + 9 | **falta** |
| 2 | Edificio Dali | portada + 7 | **falta** |
| 3 | Edificio Hernán Cortés | portada + 17 | del Word |
| 4 | Edificio Campoamor | portada + 2 | **falta** |

Esas carpetas no traen `PORTADA`, así que la portada es la primera foto numerada
o, si no hay numeración, la más grande.

**El Word de las carpetas comerciales es el mismo archivo copiado cinco veces** y
su contenido habla de Edificio Hernán Cortés. Solo se usó ahí; para los otros
cuatro no sirve y el texto queda pendiente.

### Archivo

Sección aparte al final de Proyectos: un mosaico de **cinco por fila**, once fotos,
una por proyecto, **sin enlaces**. La idea es mostrar la amplitud de la obra, no
navegar. Usa la primera foto de galería de cada proyecto, no la portada, para no
repetir lo que ya se vio arriba.

Al pasar por encima sube una **cortina** desde abajo con la ficha: nombre, año,
lugar y superficie. Los campos vacíos no se dibujan. Es el mismo gesto del telón
que usa el sitio al cambiar de página. En pantallas táctiles no hay rollover, así
que la ficha va impresa debajo de cada foto.

**El color de fondo de cada cortina sale de su propia foto.** Se calcula del
promedio de matiz del 62% inferior de la imagen — se descarta el cielo, que si no
tiñe todo de azul — y después se le baja la luminosidad hasta garantizar al menos
6:1 de contraste con el texto claro. Dan verdes oliva con variación, un café y un
azul pizarra. Los valores están en `img/proyectos/tonos.json`; si se cambia una
foto hay que recalcular ese tono o quedará descolgado.

*Francisco de Aguirre* se calculó aparte, restringiendo la muestra a los píxeles
de vegetación (matiz entre 55° y 165°): el cálculo general le daba un azul que se
despegaba del resto.

**Ocho de los once proyectos no tienen año ni superficie**, así que su dorso solo
muestra nombre y lugar: Aguas Claras AP, Aguas Claras Sur LV, Marbella CM y los
cinco comerciales (Hernán Cortés tiene superficie pero no año). Se completan en
`proyectos.py` y `comercial.py`, agregando `("Año", "...")` y
`("Superficie", "...")` a la `ficha` de cada uno.

### Movimiento

Todo vive en `site.js` (148 líneas, sin librerías) y en `styles.css`. Es
progresivo: sin JavaScript el sitio se ve y funciona igual, solo sin animación.
Todo respeta `prefers-reduced-motion`, así que quien tenga el sistema en "reducir
movimiento" ve la página quieta.

- **Hero con movimiento de dron.** No es un video: es la foto fija con un
  recorrido lento de zoom y desplazamiento (`@keyframes vuelo`, 34 s, ida y
  vuelta). Para un dron de verdad hace falta un archivo de video — ver abajo.
- **Titulares que caen.** El texto se parte en líneas y cada una entra desde
  arriba con 85 ms de diferencia. Se recalcula al cambiar el ancho de la ventana.
  Se marcan con `data-revelar` en el HTML.
- **Rollover de proyectos.** En *Proyectos destacados*, la ficha de encima crece
  un 6% y las demás se oscurecen (`brightness .45`). Usa `:has()`, soportado por
  todos los navegadores actuales; donde no lo esté, simplemente no oscurece.
- **Transición entre páginas.** Un telón que sube al salir y sigue subiendo al
  entrar, alternando color en cada salto: café de marca `#433323`, el otro café del
  logo `#897E6F`, verde salvia `#8C9B62` y verde musgo `#646C42`. El color se
  guarda en `sessionStorage`, así que el que tapa al salir es el mismo que destapa
  al entrar. Para probar otra combinación, cambia la lista `COLORES` al principio
  de `site.js` (y los `--telon-*` de `styles.css`, que son los mismos).
  Respeta cmd+clic, clic central, enlaces externos, `mailto:`, `tel:` y anclas.

- **Scroll suave (Lenis).** Es lo que hace que la página "fluya": al soltar la
  rueda sigue corriendo un poco en vez de frenar en seco. Es la misma librería y
  la misma configuración que usa el sitio de Naetive (duration 1.1, easing
  expo.out, `smoothWheel`). Va autoalojada en `js/lenis.min.js` (18 KB, MIT), sin
  depender de ningún CDN.
  - En **teléfonos no se toca el scroll**: `syncTouch` queda en false, así que el
    táctil sigue siendo el nativo del sistema, que es el que la gente espera.
  - Se desactiva con `prefers-reduced-motion` y sin JavaScript.
  - Las anclas (`#carola`, `#archivo`) las maneja Lenis con un desplazamiento
    igual al alto real de la cabecera. Por eso se sacó `scroll-behavior: smooth`
    del CSS: los dos peleaban por el mismo control.

### Otros detalles

- **Tipografía: Afical Neue**, autoalojada, cuatro pesos, sin dependencia de
  Google Fonts. Los cuatro `.woff2` pesan 230 KB en total; Regular y Medium van
  con `preload`.
- **El pie va en café** (`--ink`) con el contenido en el crudo del fondo. El icono
  de LinkedIn pasó a trazo para que funcione sobre cualquier fondo.
- **El velo del hero** solo oscurece los dos extremos; el centro de la foto queda
  limpio. Medido sobre la foto actual: titular 4,08:1, bajada 4,87:1 y menú
  7,35:1, todos sobre el mínimo de WCAG. Si cambias la foto del hero por una más
  clara, vuelve a mirarlo.
- **La bajada del home va en Afical Neue Light (300)**, más liviana que el resto
  (que va en 500). Se cambia en `.intro-text h2`.
- **Los saltos de ancla** usan `--header-real`, que `site.js` mide en vivo: la
  cabecera de Quiénes Somos es más alta porque lleva subnav, y con un valor fijo
  el título quedaba tapado. El arranque de las páginas sigue usando `--header-h`,
  fijo, para que las interiores empiecen todas a la misma altura.

## landing/ — la alternativa corta

Una sola página con hero, bajada, tres proyectos destacados, qué hacemos y
contacto. Sirve para salir antes de tener el sitio completo.

## Ver en local

```bash
cd web && python3 -m http.server 4331
```

## Publicar

Estático puro: sirve cualquier hosting. En Vercel, arrastra `web/` (o `landing/`).

---

## Antes de salir al aire

1. **LinkedIn.** Sigue en `href="#"`, marcado con `data-pendiente`. El Instagram
   ya quedó puesto: `carolapage_paisajista`.
2. **ESP/ENG.** El selector está arriba a la derecha, como en el Figma, pero solo
   existe el español: *ENG* está en `href="#"` con `data-pendiente="ingles"`.
   Hay que traducir las siete páginas o sacar el selector antes de publicar.
3. ~~**Teléfono.**~~ Confirmado: `+56 9 8888 5338` es el número real, aparece en
   el pie de todas sus láminas de presentación.
4. **Licencia de la tipografía.** El sitio va con **Afical Neue** autoalojada en
   `fonts/` (Light, Regular, Medium y SemiBold, convertidas a `.woff2`). Hay que
   confirmar que la licencia cubra *webfont embedding*: una licencia de escritorio
   no siempre autoriza servirla desde un sitio.
5. **"Paisajimo".** En el Figma la bajada del logo dice *Paisajimo* (y en las
   páginas interiores *Paisajimo del paisaje*). Acá quedó *Paisajismo* en dos
   líneas, igual en todo el sitio.

## Noticias: exposiciones, clases y charlas

Salen de `Carola Page/material/{EXPOSICIONES, CHARLAS Y PRESENTACIONES}`. Once
entradas, de la más nueva a la más antigua. Los datos están en `noticias.py`.

| Entrada | Categoría | Fecha | Texto |
|---|---|---|---|
| **Expo Jardines 2026** · PRÓXIMAMENTE | Exposiciones | 15–18 oct 2026 | sí |
| Charla en el Festival de la Rosa | Clases y Charlas | 7–9 nov 2025 | sí |
| Charla en Expo Jardines, Lo Matta | Clases y Charlas | 16–19 oct 2025 | sí |
| Días de Campo en Las Cardillas | Exposiciones | 22.07.2024 | sí |
| Festival de las Rosas | Exposiciones | 2019 | **falta** |
| «Jardín de Playa», Jardinera | Exposiciones | 2018 | **falta** |
| Clases del Magíster UC | Clases y Charlas | 2017 | **falta** |
| «Jardín de Greda», Jardinera | Exposiciones | 2014 | sí |
| «Agua de Piedra», Jardinera | Exposiciones | 2013 | **falta** |
| «Simple», Casa Mater | Exposiciones | 2009 | sí |
| Casa Mater, Quinta Normal | Exposiciones | 2007 | **falta** |
| «Sobrerelieve», Casa Mater | Exposiciones | 2004 | **falta** |
| Casa Mater — primer lugar | Exposiciones | 2002 | **falta** |
| «Pecados Capitales», Hotel Sheraton | Exposiciones | por confirmar | **falta** |

Los datos de los eventos de 2025 y 2026 se verificaron contra las páginas de
Vitacura Cultura, Lo Matta Cultural, el Club de Jardines de Chile y la
Corporación Cultural Las Condes.

**Sobre las portadas de las tres charlas agregadas:** no se bajaron imágenes de
los organizadores. Las portadas salen de material propio de Carola — fotos
extraídas de sus propias presentaciones `.pptx` y, en Casa Mater 2002, sus fotos
originales de 640 px ampliadas. Si se quiere el afiche oficial de cada evento,
hay que pedirlo a los organizadores: publicar el de un tercero en un sitio
comercial sin permiso es un problema de derechos.

`PPT_CASA LOEWE` y `PPT_O20` siguen fuera: no son charlas, son presentaciones de
proyecto para clientes.

## Contenido que falta

### Narrativa de tres proyectos

**Aguas Claras AP**, **Aguas Claras Sur LV** y **Marbella CM** no tienen texto.
Los dos primeros Word venían con el formulario en blanco (solo el encargo) y
*Aguas Claras Sur LV* no traía Word. En esas tres fichas aparece un aviso visible
diciendo que falta el texto — no inventé nada. Se agregan en `proyectos.py`,
llenando `contexto`, `intencion` y `propuesta`.

### Expo Jardines 2026

Primera entrada, con el distintivo **PRÓXIMAMENTE**. Datos del afiche oficial:
Parque Bicentenario de Vitacura, 15 al 18 de octubre, 10:00 a 22:00, organiza el
Club de Jardines de Chile. La portada es el render que acompañaba el artículo de
la Revista Club de Jardines de Chile.

### Datos por confirmar

- **Los sufijos de los títulos** (AP, LV, PI, CT, CM) parecen iniciales de cliente.
  Están tal cual salen en las carpetas, como pediste. Si no van al público, se
  cambian en `proyectos.py`.
- **Marbella CM**: el Word decía "Cachagua, Zapallar", que contradice el nombre de
  la carpeta. Dejé solo "Marbella". Falta la ubicación real, superficie y año.
- **Aguas Claras Sur LV**: sin Word, puse "Cachagua, Zapallar" por el sector.
  Confirmar.
- **Aguas Claras AP**: sin superficie ni año.
- **Ubicación de los comerciales**: solo Hernán Cortés la trae en el Word (Ñuñoa).
  En los otros cuatro puse "Santiago", que es seguro pero impreciso — falta la
  comuna, la superficie y el año.
- **El año de Hernán Cortés** quedó fuera: el Word dice "AÑO: 20", incompleto.
- **«Dali»** quedó tal cual sale en la carpeta. Si es Salvador Dalí, lleva tilde.
- **La bajada del hero** dice "Aguas Claras Norte, Cachagua, Zapallar". La foto del
  hero es la misma que la portada de ese proyecto — antes decía solo "Aguas Claras,
  Cachagua", que venía del Figma.

### Fotos

- **La portada de Aguas Claras AP venía en 1280×960**, la más chica de todas. Se
  amplió a 1400 px, pero ampliar no inventa detalle: conviene reexportarla desde
  el original. En esa carpeta hay tomas de dron de 4856 px que servirían mejor.
- **El Pangue CT, foto 13** venía en 640×640 (descargada de redes). Ampliada a
  1400 px, se va a ver blanda.
- Descarté tres imágenes de Aguas Claras AP y una de El Pangue que venían en
  640×640 y 240×300: a ese tamaño no hay forma de que se vean bien.
- Las dos fotos marcadas **ANTES** de Aguas Claras AP quedaron fuera de la
  galería. Si quieres el antes//después, se arma aparte.
- Las carpetas `extra` se ignoraron, como pediste.

El Figma tiene la estructura lista pero el contenido todavía es de relleno. Lo
que hay que reemplazar:

- **Los cuatro servicios.** El Figma repite el mismo párrafo en las cuatro
  columnas. Acá van los cuatro títulos con el párrafo real de Carola como
  entrada. Falta el texto propio de cada servicio.
- **Cronología.** Ya no sale del Figma. Las once filas de ahí eran relleno: tres
  entradas repetidas, todas fechadas 2025. Ahora se genera sola desde las entradas
  de Noticias, que tienen año verificado — trece filas, de 2026 a 2002. Si se
  agrega una noticia con año, aparece en la cronología automáticamente.
- **Noticias.** Solo *Días de Campo en Las Cardillas* tiene texto real. Las otras
  tres tarjetas repiten el marcador del Figma.
- **Traducción al inglés.** No existe.

## Diferencias respecto al Figma

- **El listado de noticias no existe en el Figma** (hay ficha de noticia, pero no
  índice). Lo armé con el mismo patrón de tarjeta de la sección Talleres.
- **El hero es una foto sola** con movimiento simulado. El diseño insinúa un
  carrusel — los guiones abajo a la derecha. Si quieres un dron de verdad, hay que
  grabarlo y montarlo como `<video>`; el recorrido sobre la foto es una
  aproximación.
- **Fotos.** El Figma expone solo veinte imágenes por API y el archivo tiene más,
  así que las de Papudo, la oficina, las charlas y la tarjeta de taller salieron
  recortadas del render (entre 389 y 1084 px de ancho). Se ven bien a tamaño
  normal, algo blandas en retina. Conviene reemplazarlas por los originales.
- En *Papudo* la ubicación dice "Papudo, Chile". El Figma decía "Zapallar, Chile"
  en todas las fichas, que parece copiado.

## Accesibilidad

El color `--muted` (#897E6F) sobre el fondo da ~3,7:1 de contraste, bajo el 4,5:1
que pide WCAG AA para texto chico. Es color de marca, así que se respetó: está
solo en metadatos, bajadas, el crédito y enlaces subrayados, nunca en texto
corrido.
