# -*- coding: utf-8 -*-
"""Genera las fichas de proyecto nuevas y actualiza proyectos.html.

La cabecera y el pie se copian de una página existente en vez de escribirse
aquí, para que no se desincronicen cuando se toque el sitio a mano.
"""
import os, re, sys, glob, subprocess

P = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(P, "web")
IMG = os.path.join(W, "img", "proyectos")
sys.path.insert(0, P)
import proyectos_datos as D

MODELO = os.path.join(W, "proyecto-campoamor.html")


def dims(p):
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                       capture_output=True, text=True).stdout
    return (int(re.search(r'pixelWidth:\s*(\d+)', o).group(1)),
            int(re.search(r'pixelHeight:\s*(\d+)', o).group(1)))


def partes():
    s = open(MODELO, encoding="utf-8").read()
    cab = s[:s.index('<main id="contenido">')]
    pie = s[s.index('</main>'):]
    return cab, pie


def ficha(p):
    filas = []
    if p["lugar"]:
        lugar = p["lugar"] + (", " + p["comuna"] if p["comuna"] else "")
        filas.append("<dt>Ubicación</dt><dd>%s</dd>" % lugar)
    if p["anio"]:
        filas.append("<dt>Año</dt><dd>%s</dd>" % p["anio"])
    if p["superficie"]:
        filas.append("<dt>Superficie</dt><dd>%s</dd>" % p["superficie"])
    return '<dl class="ficha">%s</dl>' % "".join(filas) if filas else ""


def galeria(slug, titulo, lugar):
    fotos = sorted(glob.glob(os.path.join(IMG, slug, "[0-9][0-9].jpg")))
    por = os.path.join(IMG, slug, "portada.jpg")
    out = []
    if os.path.exists(por):
        w, h = dims(por)
        out.append('<figure><img src="img/proyectos/%s/portada.jpg" width="%d" height="%d" '
                   'alt="Portada del proyecto %s"></figure>' % (slug, w, h, titulo))
    # el resto va de a dos por fila, saltando la 01 que ya es la portada
    resto = fotos[1:]
    for i in range(0, len(resto), 2):
        par = resto[i:i + 2]
        figs = []
        for j, f in enumerate(par):
            w, h = dims(f)
            figs.append('<figure><img src="img/proyectos/%s/%s" width="%d" height="%d" '
                        'alt="%s — vista %d" loading="lazy"></figure>'
                        % (slug, os.path.basename(f), w, h, titulo, i + j + 2))
        out.append('<div class="media-row">%s</div>' % "".join(figs))
    return '<div class="media-stack">%s</div>' % "".join(out)


def cuerpo_texto(p):
    """La narrativa en tres partes, como el resto del sitio. Si el proyecto no
    tiene texto se deja el aviso: no se inventa."""
    # solo el contexto: va como frase de apertura. Intención y propuesta se
    # sacaron del sitio por pedido del cliente.
    tramos = [("El contexto", p.get("contexto"))]
    tramos = [(t, c) for t, c in tramos if c]
    if not tramos:
        return ('<p class="pendiente">Texto pendiente: falta la descripción '
                'de este proyecto.</p>')
    return "".join("<section><h2>%s</h2><p>%s</p></section>" % (t, c) for t, c in tramos)


def pagina(p, cab, pie, prev, sig):
    lugar = (p["lugar"] + (", " + p["comuna"] if p["comuna"] else "")) if p["lugar"] else ""
    desc = "%s%s. Paisajismo y diseño de obra por Carola Page." % (
        p["titulo"], ", " + lugar if lugar else "")
    c = cab
    c = re.sub(r'<title>[^<]*</title>', '<title>%s · Carola Page</title>' % p["titulo"], c)
    c = re.sub(r'(<meta name="description" content=")[^"]*"', r'\g<1>%s"' % desc, c)
    c = re.sub(r'(<meta property="og:title" content=")[^"]*"',
               r'\g<1>%s · Carola Page"' % p["titulo"], c)
    c = re.sub(r'(<meta property="og:description" content=")[^"]*"', r'\g<1>%s"' % desc, c)

    nav = []
    if prev: nav.append('<a href="proyecto-%s.html">← %s</a>' % (prev["slug"], prev["titulo"]))
    else:    nav.append('<span aria-disabled="true">← Anterior</span>')
    if sig:  nav.append('<a href="proyecto-%s.html">%s →</a>' % (sig["slug"], sig["titulo"]))
    else:    nav.append('<span aria-disabled="true">Siguiente →</span>')

    cuerpo = (
        '<main id="contenido">\n'
        '  <section class="shell page-top">\n'
        '    <div class="detail">\n'
        '      <div>\n'
        '        <h1 class="detail-title">%s<span>%s</span></h1>\n'
        '        %s\n'
        '        <nav class="pager" aria-label="Navegación entre proyectos">%s</nav>\n'
        '        <div class="detail-body">%s</div>\n'
        '      </div>\n'
        '      %s\n'
        '    </div>\n'
        '  </section>\n'
        % (p["titulo"], lugar, ficha(p), "".join(nav), cuerpo_texto(p),
           galeria(p["slug"], p["titulo"], lugar))
    )
    return c + cuerpo + pie


def main():
    cab, pie = partes()
    hechos = []
    for i, p in enumerate(D.NUEVOS):
        if not os.path.isdir(os.path.join(IMG, p["slug"])):
            print("  sin fotos, se salta:", p["slug"]); continue
        prev = D.NUEVOS[i - 1] if i else None
        sig = D.NUEVOS[i + 1] if i + 1 < len(D.NUEVOS) else None
        dest = os.path.join(W, "proyecto-%s.html" % p["slug"])
        open(dest, "w", encoding="utf-8").write(pagina(p, cab, pie, prev, sig))
        n = len(glob.glob(os.path.join(IMG, p["slug"], "[0-9][0-9].jpg")))
        hechos.append((p["slug"], n))
        print("  %-18s %2d fotos" % (p["slug"], n))
    return hechos


if __name__ == "__main__":
    print("Fichas generadas:")
    main()
    # el orden final (título, frase, foto, datos, texto) lo pone este módulo,
    # que también sabe convertir las fichas antiguas
    import reordenar_fichas
    reordenar_fichas.main()
