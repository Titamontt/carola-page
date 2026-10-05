# -*- coding: utf-8 -*-
"""Saca el color de la cortina del Archivo a partir de la foto.

Promedia el tercio inferior (donde está el jardín, no el cielo) y baja la
luminosidad hasta garantizar contraste 6:1 con el texto claro que va encima.
"""
import os, re, glob, struct, subprocess, tempfile


def _tiff_rgb(path, lado=24):
    """Devuelve la lista de píxeles RGB de una miniatura, vía sips."""
    with tempfile.TemporaryDirectory() as td:
        t = os.path.join(td, "m.tiff")
        subprocess.run(["sips", "-s", "format", "tiff", "-s", "formatOptions", "none",
                        "-Z", str(lado), path, "--out", t], capture_output=True)
        d = open(t, "rb").read()
    orden = "<" if d[:2] == b"II" else ">"
    n = struct.unpack(orden + "H", d[4:6])[0] if False else None
    # lectura mínima de IFD
    off = struct.unpack(orden + "I", d[4:8])[0]
    cnt = struct.unpack(orden + "H", d[off:off + 2])[0]
    campos = {}
    for i in range(cnt):
        b = off + 2 + i * 12
        tag, typ, num = struct.unpack(orden + "HHI", d[b:b + 8])
        val = struct.unpack(orden + "I", d[b + 8:b + 12])[0]
        if typ == 3 and num == 1:
            val = struct.unpack(orden + "H", d[b + 8:b + 10])[0]
        campos[tag] = val
    w, h = campos.get(256), campos.get(257)
    spp = campos.get(277, 3)
    datos = campos.get(273)
    if None in (w, h, datos):
        return []
    px = []
    for y in range(h):
        for x in range(w):
            i = datos + (y * w + x) * spp
            if i + 3 <= len(d):
                px.append((d[i], d[i + 1], d[i + 2], y, h))
    return px


def _lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def tono(path, fondo=(252, 250, 248), minimo=6.0):
    px = _tiff_rgb(path)
    if not px:
        return "#5C6430"
    bajos = [p for p in px if p[3] >= p[4] * 0.55] or px
    r = sum(p[0] for p in bajos) // len(bajos)
    g = sum(p[1] for p in bajos) // len(bajos)
    b = sum(p[2] for p in bajos) // len(bajos)
    lf = _lum(fondo)
    for _ in range(40):
        razon = (lf + 0.05) / (_lum((r, g, b)) + 0.05)
        if razon >= minimo:
            break
        r, g, b = int(r * 0.92), int(g * 0.92), int(b * 0.92)
    return "#%02X%02X%02X" % (r, g, b)


if __name__ == "__main__":
    import sys
    IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "img", "proyectos")
    for d in sorted(os.listdir(IMG)):
        f = os.path.join(IMG, d, "01.jpg")
        if os.path.exists(f):
            print("%-20s %s" % (d, tono(f)))
