# -*- coding: utf-8 -*-
"""Reordena las fichas de proyecto al esquema pedido:

    título + frase de apertura   →   foto grande   →   datos   →   texto y fotos

Antes el texto iba en una columna fija a un costado. Ahora la página se lee de
arriba hacia abajo y los datos (lugar, año, superficie, encargo) quedan bajo la
primera foto, como en la referencia de Snøhetta.
"""
import os, re, glob

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def trozo(patron, s, flags=re.S):
    m = re.search(patron, s, flags)
    return m.group(0) if m else ""


def reordenar(s):
    detail = trozo(r'<div class="detail">.*?</div>\s*</div>\s*</section>', s)
    if not detail:
        return s, False

    titulo = trozo(r'<h1 class="detail-title">.*?</h1>', detail)
    ficha = trozo(r'<dl class="ficha">.*?</dl>', detail)
    pager = trozo(r'<nav class="pager".*?</nav>', detail)
    cuerpo = trozo(r'<div class="detail-body">.*?</div>\s*(?=</div>)', detail)
    media = trozo(r'<div class="media-stack">.*?</div>\s*(?=</div>\s*</section>)', detail)

    # la frase de apertura es el primer bloque de texto (el contexto)
    frase = ""
    secciones = re.findall(r'<section><h2>.*?</section>', cuerpo, re.S)
    if secciones:
        frase = trozo(r'<p>(.*?)</p>', secciones[0])
        frase = re.sub(r'^<p>|</p>$', '', frase)
        cuerpo = cuerpo.replace(secciones[0], "")
    else:
        pend = trozo(r'<p class="pendiente">.*?</p>', cuerpo)
        if pend:
            cuerpo = cuerpo.replace(pend, "")

    # la portada se separa del resto de las fotos
    figuras = re.findall(r'<figure>.*?</figure>|<div class="media-row">.*?</div>', media, re.S)
    portada = figuras[0] if figuras else ""
    resto = "".join(figuras[1:])

    cuerpo_limpio = re.sub(r'<div class="detail-body">|</div>\s*$', '', cuerpo).strip()

    nuevo = (
        '<section class="shell ficha-top">\n'
        '    %s\n'
        '    %s\n'
        '    %s\n'
        '  </section>\n'
        '  <section class="ficha-portada">%s</section>\n'
        '  <section class="shell ficha-datos">%s</section>\n'
        '  <section class="shell ficha-cuerpo">\n'
        '    %s\n'
        '    <div class="media-stack">%s</div>\n'
        '  </section>'
        % (titulo,
           ('<p class="ficha-frase">%s</p>' % frase) if frase else "",
           pager, portada, ficha,
           ('<div class="ficha-texto">%s</div>' % cuerpo_limpio) if cuerpo_limpio else "",
           resto)
    )
    viejo = trozo(r'<section class="shell page-top">\s*<div class="detail">.*?</div>\s*</div>\s*</section>', s)
    return s.replace(viejo, nuevo), True


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(W, "proyecto-*.html"))):
        s = open(f, encoding="utf-8").read()
        s2, ok = reordenar(s)
        if ok and s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            n += 1
    print("fichas reordenadas:", n)


if __name__ == "__main__":
    main()
