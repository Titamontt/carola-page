# -*- coding: utf-8 -*-
"""Operaciones sobre los sets de fotos de un proyecto.

promover(slug, n): la foto n pasa a ser la primera (y la portada). La que era
primera no se bota: baja una posición. quitar(slug, n): elimina una foto y
renumera. En ambos casos se regenera portada.jpg.
"""
import os, glob, shutil, sys

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
IMG = os.path.join(W, "img", "proyectos")


def _fotos(slug):
    return sorted(glob.glob(os.path.join(IMG, slug, "[0-9][0-9].jpg")))


def _reescribir(slug, orden):
    d = os.path.join(IMG, slug)
    tmp = os.path.join(d, "_tmp")
    os.makedirs(tmp, exist_ok=True)
    for i, f in enumerate(orden, 1):
        shutil.copy2(f, os.path.join(tmp, "%02d.jpg" % i))
    for f in _fotos(slug):
        os.remove(f)
    for f in sorted(glob.glob(os.path.join(tmp, "*.jpg"))):
        shutil.move(f, os.path.join(d, os.path.basename(f)))
    os.rmdir(tmp)
    shutil.copy2(os.path.join(d, "01.jpg"), os.path.join(d, "portada.jpg"))
    return len(orden)


def promover(slug, n):
    fs = _fotos(slug)
    i = n - 1
    orden = [fs[i]] + fs[:i] + fs[i + 1:]
    return _reescribir(slug, orden)


def quitar(slug, n):
    fs = _fotos(slug)
    orden = [f for k, f in enumerate(fs) if k != n - 1]
    return _reescribir(slug, orden)


if __name__ == "__main__":
    op, slug, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    print(slug, op, n, "→", (promover if op == "promover" else quitar)(slug, n), "fotos")
