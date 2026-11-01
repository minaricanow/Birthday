"""Ve lai bo sprite nhap bang code (hoa, mat troi, may, non, nha, trang, sao bang, banh kem), cung ty le pixel voi nhan vat 27x52,
roi chay pack.py. Nhan vat lay tu sprites/lynnie_1.png (khong bi ghi de); cai non lay tu chinh nhan vat do.
Ban co the ve de len bat ky file nao trong sprites/ - khong can chay file nay."""
import math, os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SPR = os.path.join(HERE, '..', 'sprites')
PAL = {'Y':'#ffd23f','O':'#f0a020','B':'#6b4220','D':'#3f2610','G':'#4fa04f','g':'#37783a','L':'#6fc06a','Z':'#ffd84d','z':'#fff0a0','u':'#d5dbf3','v':'#a9b4dc','V':'#8c97c6','F':'#ffffff','E':'#e6ecff','R':'#cfd9ff','S':'#9fb2ff','T':'#5b6bb8','y':'#ffe98a','P':'#ffeb80','b':'#8a5a2b',
       'q':'#d06a85','r':'#b8506a','Q':'#7f3350','c':'#8c6474','C':'#aa8394','w':'#cbb08c','x':'#a98f72','f':'#6a4a38','l':'#ffd36b','m':'#fff0a8','d':'#8c5732','k':'#6e4424','n':'#2a1b14','e':'#a39a8c','M':'#ece8c4','N':'#cbc59a','H':'#f8f4da'}
BRIGHT = {'Y':'#ffe66d','O':'#ffb02e','B':'#7a4a1f','D':'#43260f','G':'#5fb85f','g':'#43893f','L':'#82d37c','P':'#fff3a6'}
CAKE = {'a':'#f08fb0','A':'#d4709a','h':'#ffb5cd','v':'#fff3df','V':'#e6cfae','s':'#e03a4e','S':'#a82638','p':'#ece8f6','P':'#b9b2d6','y':'#ffd84d','o':'#ff9a2e','u':'#ffffff','k':'#8160c5','g':'#c7c7d9','W':'#2a1b14','1':'#7fd3ff','2':'#b88cf0','G':'#4fa04f'}

class Grid:
    def __init__(s, w, h): s.w, s.h = w, h; s.p = [['.'] * w for _ in range(h)]
    def set(s, x, y, c):
        x, y = int(math.floor(x + .5)), int(math.floor(y + .5))
        if 0 <= x < s.w and 0 <= y < s.h: s.p[y][x] = c
    def get(s, x, y): return s.p[y][x] if 0 <= x < s.w and 0 <= y < s.h else '.'
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.set(x, y, c)
    def ell(s, cx, cy, rx, ry, c):
        for y in range(s.h):
            for x in range(s.w):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: s.p[y][x] = c
    def img(s, pal):
        im = Image.new('RGBA', (s.w, s.h), (0, 0, 0, 0))
        for y in range(s.h):
            for x in range(s.w):
                c = s.p[y][x]
                if c in pal:
                    h = pal[c].lstrip('#'); im.putpixel((x, y), tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,))
        return im
def sheet(frames, pal):
    w, h = frames[0].w, frames[0].h; im = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames): im.paste(f.img(pal), (i * w, 0))
    return im

def flower(big, dx):
    if big: W, H, hx, hy, sx, rs, rp, lobes, amp, inner = 26, 36, 13 + dx * 2, 10.5, 12, 4.6, 8.0, 9, 1.9, 6.6
    else:   W, H, hx, hy, sx, rs, rp, lobes, amp, inner = 22, 24, 11 + dx * 1.5, 8.5, 10, 3.2, 6.4, 8, 1.2, 4.9
    g = Grid(W, H); base, ctrl, tip = (sx, H - 1), (sx + dx * .6, H * .66), (hx - .5, hy + (6 if big else 4)); pts = []
    for i in range(121):
        t = i / 120; x = (1-t)**2*base[0] + 2*t*(1-t)*ctrl[0] + t*t*tip[0]; y = (1-t)**2*base[1] + 2*t*(1-t)*ctrl[1] + t*t*tip[1]
        pts.append((x, y)); g.set(x, y, 'G'); g.set(x + 1, y, 'g')
    def leaf(idx, side, ln, lift):
        px0, py0 = pts[idx]
        for k in range(ln):
            t = k / (ln - 1); x = px0 + side * (k + 1.4); y = py0 - lift * math.sin(t * 1.6) * (1 if big else .8) - t
            th = 1 if t < .35 or t > .8 else 2
            for j in range(th): g.set(x, y + j, 'G' if side < 0 or j == 0 else 'g')
            if 0 < k < ln - 1 and th == 1: g.set(x, y, 'L')
    if big: leaf(70, -1, 8, 3.6); leaf(52, 1, 8, 3.6)
    else: leaf(62, 1, 5, 2.2)
    for y in range(H):
        for x in range(W):
            r = math.hypot(x - hx, y - hy); th = math.atan2(y - hy, x - hx); c = abs(math.cos(lobes / 2 * th)); R = rp + amp * (c ** 1.5)
            if r <= rs: g.set(x, y, 'D' if ((x * 3 + y * 5) % 7 in (0, 3)) else 'B')
            elif r <= R: g.set(x, y, 'O' if r <= inner else ('P' if (r > R - 1.3 and c > .9) else 'Y'))
    for y in range(H):
        for x in range(W):
            if g.get(x, y) == 'B' and math.hypot(x - hx, y - hy) > rs - 1.1: g.set(x, y, 'b')
    return g

def house(open_, flick):
    g = Grid(72, 60)
    g.rect(6, 22, 65, 59, 'w')                      # tuong
    for y in range(27, 56, 5): g.rect(6, y, 65, y, 'x')   # van go ngang
    g.rect(6, 56, 65, 59, 'x')                      # chan tuong
    for fy in range(0, 24):                          # mai
        half = int(fy * .75 + 1) * 2 - 1
        x0, x1 = max(0, 35 - half), min(71, 36 + half)
        row = fy // 4; off = (row % 2) * 3
        for x in range(x0, x1 + 1):
            c = 'q' if fy % 4 < 2 else 'r'
            if (x + off) % 6 == 0 and fy % 4 >= 1: c = 'Q'
            g.set(x, fy, c)
        g.set(x0, fy, 'Q'); g.set(x1, fy, 'Q'); g.set(x0 + 1, fy, 'Q'); g.set(x1 - 1, fy, 'Q')
    g.rect(0, 22, 71, 23, 'Q')                      # mep mai
    g.rect(52, 2, 59, 15, 'c')                      # ong khoi
    for y in range(2, 16, 3): g.rect(52, y, 59, y, 'C')
    for y in range(2, 16, 6): g.rect(55, y, 55, y + 2, 'C')
    g.rect(50, 0, 61, 1, 'C')
    glass = 'm' if flick else 'l'
    for wx in (14, 46):
        g.rect(wx, 30, wx + 11, 41, 'f'); g.rect(wx + 2, 32, wx + 9, 39, glass); g.rect(wx + 5, 32, wx + 6, 39, 'f'); g.rect(wx + 2, 35, wx + 9, 36, 'f')
        g.rect(wx - 1, 42, wx + 12, 43, 'x')
    g.rect(30, 38, 41, 59, 'f')                      # cua
    if open_:
        g.rect(32, 40, 39, 59, 'n'); g.rect(34, 42, 37, 59, 'Z'); g.rect(35, 42, 36, 59, 'm'); g.rect(28, 40, 31, 59, 'd'); g.rect(28, 40, 28, 59, 'k')
    else:
        g.rect(32, 40, 39, 59, 'd'); g.rect(33, 42, 38, 47, 'k'); g.rect(33, 50, 38, 57, 'k'); g.rect(34, 43, 37, 46, 'd'); g.rect(34, 51, 37, 56, 'd'); g.set(38, 50, 'Z'); g.set(38, 51, 'Z')
    g.rect(28, 58, 43, 59, 'e')
    return g

def moon():
    g = Grid(40, 40); g.ell(20, 20, 19.6, 19.6, 'N'); g.ell(19.2, 19.2, 18.4, 18.4, 'M'); g.ell(15.5, 15.5, 11.5, 11.5, 'H')
    for x in range(40):
        for y in range(40):
            if g.get(x, y) == 'M' and math.hypot(x + .5 - 17, y + .5 - 17) > 17.2: g.set(x, y, 'N')   # bong ben phai duoi
    for cx, cy, r in [(11, 12, 3.6), (25, 9, 2.5), (27, 23, 4.4), (14, 28, 3.0), (32, 14, 1.8), (22, 33, 2.1), (7, 23, 1.7), (20, 18, 1.5), (31, 31, 1.6)]:
        g.ell(cx, cy, r, r, 'N'); g.ell(cx - .8, cy - .8, r * .6, r * .6, 'M')
    return g

def cloud(v):   # v = 0, 1: hai kieu may
    g = Grid(64, 20)
    puffs = [[(12, 13, 10, 6), (26, 9, 12, 8), (42, 11, 12, 8), (54, 14, 9, 5)], [(10, 14, 8, 5), (22, 10, 10, 7), (36, 8, 12, 8), (50, 12, 11, 7)]][v]
    for cx, cy, rx, ry in puffs: g.ell(cx, cy, rx, ry, 'u')
    for x in range(64):
        for y in range(17, 20): g.set(x, y, '.')
    for x in range(64):
        for y in range(20):
            if g.get(x, y) == 'u' and (y >= 15 or (y >= 13 and (x + y) % 3 == 0)): g.set(x, y, 'v')
            if g.get(x, y) == 'v' and y == 16: g.set(x, y, 'V')
    return g

def star(f):   # sao bang: dau (4 canh sang) o goc duoi phai, duoi keo len tren trai, mo dan
    g = Grid(48, 24); hx, hy = 42, 18
    for k in range(0, 36):
        x, y = hx - 1.2 * k, hy - .6 * k
        c = 'F' if k < 5 else 'E' if k < 12 else 'R' if k < 20 else 'S' if k < 28 else 'T'
        wd = 3 if k < 8 else 2 if k < 20 else 1
        for j in range(wd): g.set(x, y + j - (wd - 1) / 2 + .2, c)
        if k > 22 and k % 2: g.set(x, y, '.')
    arm = [5, 4, 6, 4][f]
    for d in range(-arm, arm + 1): g.set(hx + d, hy, 'F'); g.set(hx, hy + d, 'F')
    for d in (-1, 1):
        g.set(hx + d, hy + d, 'F'); g.set(hx + d, hy - d, 'F'); g.set(hx + 2 * d, hy, 'F')
    for d in (-3, 3): g.set(hx + d, hy + 1, 'R'); g.set(hx + d, hy - 1, 'R'); g.set(hx + 1, hy + d, 'R'); g.set(hx - 1, hy + d, 'R')
    return g

def cake(f):   # f: 0,1 = nen sang (2 kieu lua), 2,3 = nen tat (2 kieu khoi)
    g = Grid(32, 32)
    g.ell(16, 30.3, 15.6, 2.2, 'P'); g.ell(16, 29.2, 15.6, 2.0, 'p')
    g.rect(4, 17, 27, 28, 'a'); g.rect(25, 17, 27, 28, 'A'); g.rect(4, 27, 27, 28, 'A'); g.rect(4, 18, 5, 26, 'h')
    for x, y in ((4, 17), (27, 17), (4, 28), (27, 28)): g.set(x, y, '.')
    g.rect(4, 17, 27, 18, 'v')
    for x, ln in ((6, 4), (10, 3), (15, 5), (20, 3), (24, 4)): g.rect(x, 19, x + 1, 18 + ln, 'v')
    for x, y, c in ((8, 23, 'y'), (13, 25, '1'), (18, 22, '2'), (23, 25, 'y'), (10, 26, '2'), (21, 26, '1'), (15, 23, 'u')): g.set(x, y, c); g.set(x + 1, y, c)
    g.rect(8, 10, 23, 16, 'v'); g.rect(21, 10, 23, 16, 'V'); g.rect(8, 16, 23, 16, 'V')
    g.rect(8, 10, 23, 11, 'h')
    for x, ln in ((10, 3), (15, 4), (19, 2)): g.rect(x, 12, x + 1, 11 + ln, 'h')
    for x in (4, 25):
        g.rect(x, 15, x + 1, 16, 's'); g.set(x, 16, 'S'); g.set(x + 1, 16, 'S'); g.set(x, 14, 'G')
    for cxs in (11, 15, 19):
        for y in range(4, 10): g.rect(cxs, y, cxs + 1, y, 'u' if y % 2 == 0 else 'k')
        g.set(cxs, 3, 'W')
        if f in (0, 1):
            g.set(cxs + (1 if f else 0), 0, 'y'); g.rect(cxs, 1, cxs + 1, 1, 'y'); g.rect(cxs, 2, cxs + 1, 2, 'o')
        else:
            g.set(cxs + (f - 2), 1, 'g'); g.set(cxs + 1 - (f - 2), 0, 'g')
    return g


def sun():
    g = Grid(28, 28); g.ell(14, 14, 13.6, 13.6, 'O'); g.ell(14, 14, 12.2, 12.2, 'Z'); g.ell(13.2, 13.2, 7.4, 7.4, 'y')
    return g

def cloud_day():
    g = Grid(40, 12)
    for cx, cy, rx, ry in [(10, 8.4, 9, 4.4), (20, 6, 10, 5.6), (30, 8.4, 9, 4.4)]: g.ell(cx, cy, rx, ry, 'W')
    for x in range(40):
        for y in range(10, 12): g.set(x, y, '.')
    for x in range(40):
        if g.get(x, 9) == 'W': g.set(x, 9, 'X')
        if g.get(x, 8) == 'W' and g.get(x, 9) == 'X' and x % 2 == 0: g.set(x, 8, 'X')
    return g

def hat_frames():   # cai non: lay phan khac nhau giua frame co non va khong non trong lynnie_1.png, xoay 4 goc
    import numpy as np
    a = np.array(Image.open(os.path.join(SPR, 'lynnie_1.png')).convert('RGBA'))
    A, B = a[:, 0:27], a[:, 108:135]
    d = (A != B).any(axis=2) & (A[:, :, 3] > 0); ys, xs = np.where(d); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    hat = Image.new('RGBA', (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
    for y, x in zip(ys, xs): hat.putpixel((int(x - x0), int(y - y0)), tuple(int(v) for v in A[y, x]))
    S = max(hat.size); sq = Image.new('RGBA', (S, S), (0, 0, 0, 0)); sq.paste(hat, ((S - hat.width) // 2, (S - hat.height) // 2))
    out = Image.new('RGBA', (S * 4, S), (0, 0, 0, 0))
    for i, f in enumerate([sq, sq.transpose(Image.ROTATE_270), sq.transpose(Image.ROTATE_180), sq.transpose(Image.ROTATE_90)]): out.paste(f, (i * S, 0))
    return out


def table():   # ban tron phu khan tim vien vang, de dat banh kem len tren (mat ban nhin hoi tu tren xuong)
    g = Grid(60, 32)
    g.ell(30, 9, 28.5, 7.2, 'q'); g.ell(30, 8.2, 27.2, 6.4, 'h')
    for y in range(9, 28):     # khan ru xuong
        half = 28.5 - (y - 9) * .02
        for x in range(60):
            if abs(x + .5 - 30) <= half and ((x + .5 - 30) / 28.5) ** 2 + ((y - 9) / 7.2) ** 2 >= 0 and (y >= 9): g.set(x, y, 'q' if ((x // 4) % 2) else 'r')
    for x in range(60):          # vien luon song o mep duoi
        if g.get(x, 26) != '.':
            g.set(x, 26, 'y' if (x // 3) % 2 else 'Y'); g.set(x, 27, 'y' if (x // 3) % 2 == 0 else 'Y')
            if (x // 3) % 2: g.set(x, 28, 'Y')
    for x in range(60):          # soc vang tren khan
        if g.get(x, 20) != '.': g.set(x, 20, 'Y'); g.set(x, 21, 'Y')
    g.ell(30, 8.2, 27.2, 6.4, 'h'); g.ell(30, 8.2, 23.5, 5.2, 'q')   # mat ban sang, co vien
    for x in range(60):
        for y in range(32):
            if g.get(x, y) == 'q' and y < 9 and ((x - 30) / 23.5) ** 2 + ((y - 8.2) / 5.2) ** 2 > .82: g.set(x, y, 'h')
    return g

def save(name, frames, pal):
    im = sheet(frames, pal); os.makedirs(SPR, exist_ok=True); im.save(os.path.join(SPR, name + '.png'))
save('sunL', [flower(True, d) for d in (-1, 0, 1)], PAL);  save('sunLb', [flower(True, d) for d in (-1, 0, 1)], {**PAL, **BRIGHT})
save('sunS', [flower(False, d) for d in (-1, 0, 1)], PAL); save('sunSb', [flower(False, d) for d in (-1, 0, 1)], {**PAL, **BRIGHT})
save('house', [house(0, 0), house(1, 0), house(0, 1), house(1, 1)], PAL)
save('sun', [sun()], PAL); save('cloud_day', [cloud_day()], {**PAL, 'W': '#ffffff', 'X': '#dcebf7'})
save('moon', [moon()], PAL); save('cloud_night', [cloud(0), cloud(1)], PAL); save('star', [star(i) for i in range(4)], PAL); save('cake', [cake(i) for i in range(4)], CAKE); save('table', [table()], {**PAL, 'q': '#8e6fe0', 'r': '#7a5bd0', 'h': '#b39cf5', 'y': '#ffd93b', 'Y': '#d9a300'})
subprocess.run([sys.executable, os.path.join(HERE, 'pack.py')], check=True)
