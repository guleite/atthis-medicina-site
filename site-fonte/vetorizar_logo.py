# -*- coding: utf-8 -*-
"""
Vetoriza localmente o logo Atthis (imagem JPEG enviada pelo cliente) em SVG.
Separa as duas tintas (dourado da libélula e verde do texto), amplia 6x,
extrai contornos e gera caminhos suavizados. Saída em site/assets/img/.
Uso: python site-fonte/vetorizar_logo.py
"""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "WhatsApp Image 2026-11-25 at 16.43.42 (1).jpeg")
OUT = os.path.join(ROOT, "site", "assets", "img")

S = 6                       # fator de ampliação antes de extrair contornos
CROP = (330, 212, 892, 492)  # x0, y0, x1, y1 do logo na imagem original

from PIL import Image  # cv2.imread não lê caminhos com acento no Windows
img = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
x0, y0, x1, y1 = CROP
img = img[y0:y1, x0:x1]
bg = np.array([221., 213., 202.])
d = np.sqrt(((img - bg) ** 2).sum(-1))
alpha = np.clip((d - 6) / 95, 0, 1)
col = np.clip(np.where(alpha[..., None] > .02, bg + (img - bg) / np.maximum(alpha[..., None], .02), bg), 0, 255)
gold = (col[..., 0] - col[..., 1]) > 4
# a libélula fica só à esquerda; fora dela toda tinta é verde (evita pontos dourados nas letras)
yy, xx = np.mgrid[0:gold.shape[0], 0:gold.shape[1]]
dragonfly_zone = (xx < 235) & ~((yy > 183) & (xx > 70))
gold = gold & dragonfly_zone


def layer(mask_bool, thr):
    a = (alpha * mask_bool).astype(np.float32)
    big = cv2.resize(a, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), S * 0.35)
    m = (big > thr).astype(np.uint8) * 255
    cnts, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    parts = []
    for c in cnts:
        if cv2.contourArea(c) < (S * S * 1.2):
            continue
        pts = c[:, 0, :].astype(np.float32)
        if len(pts) > 12:  # suaviza ao longo do contorno
            k = 5
            pad = np.concatenate([pts[-k:], pts, pts[:k]])
            ker = np.ones(2 * k + 1) / (2 * k + 1)
            pts = np.stack([np.convolve(pad[:, i], ker, "valid") for i in (0, 1)], 1)
        ap = cv2.approxPolyDP(pts.astype(np.float32).reshape(-1, 1, 2), 0.6, True)[:, 0, :]
        if len(ap) < 3:
            continue
        ap = ap / S
        parts.append("M" + " L".join(f"{p[0]:.2f} {p[1]:.2f}" for p in ap) + "Z")
    return " ".join(parts)


def ink(mask_bool):
    sel = (alpha > .85) & mask_bool
    c = np.median(col[sel], axis=0)
    return "#%02x%02x%02x" % tuple(int(v) for v in c)


gold_path = layer(gold, 0.42)
green_path = layer(~gold, 0.45)
gold_c, green_c = ink(gold), ink(~gold)
w, h = x1 - x0, y1 - y0

# recorte vertical sem o slogan (para usos muito pequenos)
def svg(name, paths, viewbox):
    body = "".join(f'<path fill="{c}" fill-rule="evenodd" d="{p}"/>' for c, p in paths)
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="Atthis — Gestão personalizada da saúde">{body}</svg>'
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, len(s) // 1024, "KB")


svg("logo-atthis-completo.svg", [(gold_c, gold_path), (green_c, green_path)], f"0 0 {w} {h}")
svg("logo-atthis-completo-claro.svg", [("#d4c6a2", gold_path), ("#efe7da", green_path)], f"0 0 {w} {h}")
print("tintas:", gold_c, green_c)
