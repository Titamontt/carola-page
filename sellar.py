# -*- coding: utf-8 -*-
"""Pone ?v=<fecha> en styles.css y site.js de todas las páginas.

Sin esto el navegador se queda con la hoja de estilos y el script viejos
aunque el HTML sea nuevo, y los cambios no aparecen.
Hay que correrlo después de tocar styles.css o site.js.
"""
import os, re, glob

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

def sello(nombre):
    return str(int(os.path.getmtime(os.path.join(W, nombre))))

def main():
    v_css, v_js = sello("styles.css"), sello("site.js")
    n = 0
    for f in glob.glob(os.path.join(W, "*.html")):
        s = o = open(f, encoding="utf-8").read()
        s = re.sub(r'href="styles\.css(?:\?v=\d+)?"', 'href="styles.css?v=%s"' % v_css, s)
        s = re.sub(r'src="site\.js(?:\?v=\d+)?"', 'src="site.js?v=%s"' % v_js, s)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print("sellado en %d páginas (css %s, js %s)" % (n, v_css, v_js))

if __name__ == "__main__":
    main()
