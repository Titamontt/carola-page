# -*- coding: utf-8 -*-
"""Datos de los proyectos nuevos incorporados desde el Drive (sept 2026).

Lo que está en None sale como PENDIENTE en la página: no se inventa.
El año, cuando existe, viene del nombre de la carpeta en el Drive.
"""

NUEVOS = [
    # --- residenciales ---
    # lugar y año salen del nombre de la carpeta en JARDINES PRIVADOS del Drive
    dict(slug="casa-jj", titulo="Casa JJ", cat="residencial",
         lugar="Concepción", comuna=None, anio="2023", superficie=None),
    dict(slug="el-nocedal", titulo="El Nocedal", cat="residencial",
         lugar="Lo Barnechea", comuna="Santiago", anio="2010", superficie="2.000 m²",
         encargo="Diseño y ejecución de jardín y arquitectura exterior: jardineras de "
                 "hormigón a la vista, pavimentos, gradas y maceteros de huerta en madera.",
         contexto="La casa se relaciona con el jardín desde adentro, a través de una "
                  "sucesión de patios. El jardín no se ve de una vez: aparece en tramos, "
                  "distinto desde cada ventana y en cada punto del recorrido.",
         intencion="Seguir las líneas de la arquitectura y componer cada patio como una "
                   "vista, pensada tanto desde el interior de la casa como desde el propio jardín.",
         propuesta="Cada espacio recibe un lenguaje y un colorido propios según su uso: "
                   "huerta, jardinera de segundo piso, jardín de gravilla, antejardín de "
                   "acceso, jardín de maceteros y jardín principal con pasto. Las obras "
                   "civiles —fogón, jardineras de hormigón a la vista con bancos en obra, "
                   "gradas y terraza de piscina— se diseñaron junto con la vegetación. Los "
                   "patios de gravilla acotan la superficie de pasto y bajan el consumo de "
                   "agua del conjunto."),
    dict(slug="casa-anwandter", titulo="Casa Anwandter", cat="residencial",
         lugar="Camino La Oliva", comuna=None, anio="2007", superficie=None),
    dict(slug="casa-abaroa", titulo="Casa Abaroa", cat="residencial",
         lugar="Valle Escondido", comuna=None, anio="2007", superficie=None),
    dict(slug="casa-valdes", titulo="Casa Valdés", cat="residencial",
         lugar="Santa María de Manquehue", comuna="Vitacura",
         anio="2010", superficie="700 m²",
         encargo="Diseño y ejecución de jardín y arquitectura exterior: vegetación, "
                 "circulaciones, pileta de agua, muros medianeros, jardineras y quincho.",
         contexto="Un patio de acceso: el primer espacio que se ve al entrar a la casa, "
                  "y el que decide con qué impresión se llega a la puerta.",
         intencion="Que el recorrido hacia la entrada principal se sienta más amplio de lo "
                   "que es, llevando la mirada hacia un costado en vez de empujarla al frente.",
         propuesta="Una pileta de agua en movimiento con plantas acuáticas abre esa vista "
                   "lateral. La paleta mezcla lo mediterráneo con lo de campo y lo silvestre: "
                   "ciprés piramidal, juncos de arena, pelargonios blancos y un pasto "
                   "ornamental gris azulado."),
    # --- comerciales ---
    dict(slug="los-clarines", titulo="Edificio Los Clarines", cat="comercial",
         lugar="Santiago", comuna=None, anio=None, superficie=None),
    dict(slug="edificio-era", titulo="Edificio ERA", cat="comercial",
         lugar="Santiago", comuna=None, anio="2007", superficie=None),
    dict(slug="pde-valdivia", titulo="Edificio Pedro de Valdivia", cat="comercial",
         lugar="Santiago", comuna=None, anio=None, superficie=None),
    dict(slug="edificio-sucre", titulo="Edificio Sucre", cat="comercial",
         lugar="Santiago", comuna=None, anio=None, superficie=None),
]

# Proyectos que ya estaban y recibieron una selección mejor desde el Drive.
# Las fotos nuevas reemplazan a las publicadas; la ficha no cambia.
REEMPLAZOS = {"punta-pite": "punta-pite-v2",
              # "Casa Cotton" del Drive es este mismo jardín
              "el-pangue-ct": "cotton",
              # "Casa Pipa" del Drive es este mismo proyecto
              "aguas-claras-norte-pi": "casa-pipa",
              "marbella-cm": "marbella-cm-v2",
              "campoamor": "campoamor-v2"}
