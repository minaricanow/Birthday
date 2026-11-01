"""Ghep sprites/*.png vao template.html -> index.html (thiep sinh nhat: man hinh lon, ngay/dem, nha, ban banh kem).
Dung khi ban da ve/thay sprite:   python3 tools/pack.py        (can Python 3 va  pip install pillow)

Moi PNG la 1 hang ngang cac frame cung kich thuoc, nen trong suot. Kich thuoc frame o bang FRAMES (rong, cao).
sunLb.png / sunSb.png (hoa sang len khi nhan vat di gan) tu tao tu sunL / sunS neu thieu."""
import base64, io, json, os
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__)); SPR = os.path.join(HERE, '..', 'sprites'); OUT = os.path.join(HERE, '..')

FRAMES = {                      # ten file: (rong 1 frame, cao 1 frame)
    'lynnie_1':    (27, 52),    # nhan vat; trang chi dung 4 frame dau (dung, buoc trai, buoc phai, chop mat); 4 frame sau de du phong
    'sunL':        (26, 36),    # hoa lon, 3 frame: nghieng trai, thang, nghieng phai
    'sunS':        (22, 24),    # hoa nho hang sau, 3 frame
    'sun':         (28, 28),    # mat troi (ban ngay)
    'cloud_day':   (40, 12),    # may ban ngay
    'table':       (60, 32),    # ban tron phu khan, dat banh kem len tren
    'house':       (72, 60),    # nha, 4 frame: cua dong/mo x den thuong/sang
    'moon':        (40, 40),    # mat trang
    'cloud_night': (64, 20),    # may ban dem, 2 frame (2 kieu may)
    'star':        (48, 24),    # sao bang, 4 frame (dau o goc duoi phai, duoi keo len tren trai)
    'cake':        (32, 32),    # banh kem, 4 frame: nen sang A, nen sang B, nen tat A, nen tat B
}

# ten trong trang  ->  (file, so frame dau lay, hoac None = lay het)
THEMES = {
    'birthday': ('template.html', 'index.html', {
        'girl': ('lynnie_1', 4), 'house': ('house', None), 'table': ('table', None), 'cake': ('cake', None),
        'sunL': ('sunL', None), 'sunS': ('sunS', None), 'sun': ('sun', None), 'cloud': ('cloud_day', None),
        'moon': ('moon', None), 'cloudN': ('cloud_night', None), 'star': ('star', None)}),
}

SND = os.path.join(HERE, '..', 'sounds')
MIME = {'.mp3': 'audio/mpeg', '.ogg': 'audio/ogg', '.opus': 'audio/ogg', '.m4a': 'audio/mp4', '.aac': 'audio/aac', '.wav': 'audio/wav'}
def sounds():   # sounds/01.* ... 07.*  (1 file cho moi bong hoa nhac); thieu file nao thi bong hoa do khong co tieng
    out, total = [], 0
    for i in range(1, 8):
        found = [f for f in sorted(os.listdir(SND)) if os.path.splitext(f)[0] == '%02d' % i and os.path.splitext(f)[1].lower() in MIME] if os.path.isdir(SND) else []
        if not found: out.append(None); continue
        raw = open(os.path.join(SND, found[0]), 'rb').read(); total += len(raw)
        out.append('data:%s;base64,%s' % (MIME[os.path.splitext(found[0])[1].lower()], base64.b64encode(raw).decode()))
    if total: print('Nhung %d/7 file am thanh, tong %.1f KB' % (sum(1 for x in out if x), total / 1024))
    if total > 8 * 1024 * 1024: print('CANH BAO: am thanh tren 8 MB, trang se nang. Nen cat ngan hon hoac giam bitrate.')
    return out

def brighten(im):
    rgb, a = im.convert('RGB'), im.getchannel('A')
    rgb = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.25)).enhance(1.4)
    out = rgb.convert('RGBA'); out.putalpha(a); return out

def load(name):
    p = os.path.join(SPR, name + '.png')
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGBA'); fw, fh = FRAMES.get(name, (None, None))
    if fw and (im.height != fh or im.width % fw):
        raise SystemExit('%s.png phai cao %d va rong chia het cho %d (hien la %dx%d)' % (name, fh, fw, im.width, im.height))
    return im

def entry(im, fw, fh):
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return {'src': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), 'w': fw, 'h': fh, 'n': im.width // fw}

for theme, (tpl_name, out_name, mapping) in THEMES.items():
    sp = {}
    for key, (fname, nframes) in mapping.items():
        im = load(fname)
        if im is None: raise SystemExit('Thieu file sprites/%s.png' % fname)
        fw, fh = FRAMES[fname]
        if nframes: im = im.crop((0, 0, fw * nframes, fh))
        sp[key] = entry(im, fw, fh)
        if key in ('sunL', 'sunS'):   # ban sang len khi nhan vat di gan
            big = load(key + 'b') or brighten(im)
            sp[key + 'b'] = entry(big, fw, fh)
    tpl = open(os.path.join(HERE, tpl_name), encoding='utf-8').read()
    html = tpl.replace('__SPRITES__', json.dumps(sp)).replace('__SOUNDS__', json.dumps(sounds()))
    open(os.path.join(OUT, out_name), 'w', encoding='utf-8').write(html)
    print('Da tao', out_name, {k: v['n'] for k, v in sp.items()})
