"""Cat 1 file audio thanh 7 doan, luu vao sounds/01.mp3 ... sounds/07.mp3 (moi doan gan vao 1 bong hoa huong duong).

Dung:   python3 tools/split_audio.py duong_dan_file_audio.mp3
        python3 tools/split_audio.py file.m4a --times 3.2,7.5,11.0,15.4,19.9,24.1     (tu chon 6 moc cat, don vi giay)
        python3 tools/split_audio.py file.wav --mode equal                             (chia deu 7 phan, khong tim cho im lang)

Mac dinh (--mode auto): chia 7 phan gan deu, roi nhich moi moc cat toi cho im lang gan nhat (neu co) de khong cat ngang tieng hat.
Can cai ffmpeg (https://ffmpeg.org) va co lenh ffmpeg / ffprobe trong PATH. Sau khi cat xong chay:  python3 tools/pack.py
Chi dung audio ban co quyen su dung; neu dua trang len mang cong khai thi audio cung nam trong trang do."""
import argparse, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'sounds')

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def duration(path):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', path])
    try: return float(r.stdout.strip())
    except ValueError: sys.exit('Khong doc duoc do dai file (ffprobe loi): ' + r.stderr.strip())

def silences(path, noise='-32dB', dur=0.18):
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'silencedetect=noise=%s:d=%s' % (noise, dur), '-f', 'null', '-'])
    starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', r.stderr)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    return [(s + e) / 2 for s, e in zip(starts, ends)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('--parts', type=int, default=7)
    ap.add_argument('--mode', choices=['auto', 'equal'], default='auto'); ap.add_argument('--times', help='cac moc cat, cach nhau dau phay (parts-1 moc)')
    ap.add_argument('--bitrate', default='96k')
    a = ap.parse_args()
    if not os.path.exists(a.input): sys.exit('Khong thay file: ' + a.input)
    if run(['ffmpeg', '-version']).returncode != 0: sys.exit('Chua co ffmpeg trong PATH.')
    d = duration(a.input); n = a.parts
    if a.times:
        cuts = [float(x) for x in a.times.split(',')]
        if len(cuts) != n - 1: sys.exit('Can dung %d moc cat (dang co %d).' % (n - 1, len(cuts)))
    else:
        cuts = [d * i / n for i in range(1, n)]
        if a.mode == 'auto':
            sil = silences(a.input); seg = d / n; snapped = []
            for t in cuts:
                near = [s for s in sil if abs(s - t) <= seg * .4]
                snapped.append(min(near, key=lambda s: abs(s - t)) if near else t)
            print('Tim thay %d cho im lang; %d/%d moc cat duoc nhich vao cho im lang.' % (len(sil), sum(1 for c, t in zip(snapped, cuts) if c != t), n - 1))
            cuts = snapped
    pts = [0.0] + sorted(cuts) + [d]
    os.makedirs(OUT, exist_ok=True)
    for i in range(n):
        s, e = pts[i], pts[i + 1]; out = os.path.join(OUT, '%02d.mp3' % (i + 1))
        fade = max(0.0, min(0.06, (e - s) / 4))
        af = 'afade=t=in:d=%.3f,afade=t=out:st=%.3f:d=%.3f' % (fade, max(0.0, e - s - fade), fade)
        r = run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', '%.3f' % s, '-t', '%.3f' % (e - s), '-i', a.input, '-vn', '-af', af, '-ac', '2', '-b:a', a.bitrate, out])
        if r.returncode: sys.exit('ffmpeg loi: ' + r.stderr)
        print('%02d  %7.2fs -> %7.2fs  (%.2fs)  %s' % (i + 1, s, e, e - s, os.path.relpath(out)))
    print('Xong. Chay tiep:  python3 tools/pack.py')
main()
