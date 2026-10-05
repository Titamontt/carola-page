# -*- coding: utf-8 -*-
"""Reescribe width/height de cada <img> según el archivo real.

Al reordenar o quitar fotos, los números del HTML quedan apuntando a imágenes
distintas y el navegador las deforma. Esto los vuelve a dejar correctos.
"""
import os, re, glob, subprocess

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
_cache = {}


def dims(rel):
    if rel in _cache:
        return _cache[rel]
    p = os.path.join(W, rel)
    if not os.path.exists(p):
        return None
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                       capture_output=True, text=True).stdout
    try:
        d = (int(re.search(r'pixelWidth:\s*(\d+)', o).group(1)),
             int(re.search(r'pixelHeight:\s*(\d+)', o).group(1)))
    except AttributeError:
        return None
    _cache[rel] = d
    return d


def main():
    tocados = 0
    for f in glob.glob(os.path.join(W, "*.html")):
        s = o = open(f, encoding="utf-8").read()

        def arregla(m):
            tag = m.group(0)
            src = re.search(r'src="([^"]+)"', tag)
            if not src:
                return tag
            d = dims(src.group(1).split("?")[0])
            if not d:
                return tag
            tag = re.sub(r'\swidth="\d+"', ' width="%d"' % d[0], tag)
            tag = re.sub(r'\sheight="\d+"', ' height="%d"' % d[1], tag)
            return tag

        s = re.sub(r'<img [^>]*>', arregla, s)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
            tocados += 1
    print("dimensiones corregidas en %d páginas" % tocados)


if __name__ == "__main__":
    main()
