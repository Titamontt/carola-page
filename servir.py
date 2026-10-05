# -*- coding: utf-8 -*-
"""Servidor de previsualización, sin caché.

El navegador se quedaba con styles.css y site.js viejos y los cambios no
aparecían. Esto fuerza a pedirlos de nuevo en cada carga.

    python3 servir.py            →  http://localhost:4331
"""
import http.server, functools, os, sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
PUERTO = 4331


class SinCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    raiz = sys.argv[1] if len(sys.argv) > 1 else RAIZ
    print("sirviendo %s en http://localhost:%d" % (raiz, PUERTO))
    http.server.HTTPServer(("127.0.0.1", PUERTO),
                           functools.partial(SinCache, directory=raiz)).serve_forever()
