SUNFLOWER CARD - thiep sinh nhat pixel: 1 man hinh lon, canh dong hoa huong duong co ngoi nha va ban banh kem o giua, doi duoc ngay / dem.

MAU / KHUNG
  Bang mau tim 'borahae' (tim oai huong, tim dam, xanh den tim) + 7 trai tim pixel duoi tieu de. Mau nam trong khoi CSS o dau tools/template.html (--frame1, --frame2, --btn1, --btn2...),
  mau bau troi ban ngay / ban dem nam trong ham buildBG (bands).

MO XEM
  Mo index.html bang trinh duyet la chay. Can mang de tai font (Press Start 2P, VT323); khong co mang van chay, chi doi font.
  Gui link cho nguoi nhan: dua ca thu muc len GitHub Pages hoac keo tha vao Netlify Drop.

CAU TRUC
  index.html              trang hoan chinh, sprite da nhung san. Day la file de host.
  sprites/*.png           sprite. lynnie_1.png la nhan vat cua ban; cac sprite khac la ban nhap Claude ve bang code, cung ty le pixel.
  tools/template.html     giao dien + logic (di chuyen, nha, banh kem, ngay/dem...). Sua chu, chinh hanh vi o day.
  tools/pack.py           ghep sprites/*.png vao template -> index.html   (python3 tools/pack.py, can: pip install pillow)
  tools/build_placeholder.py   ve lai bo sprite nhap bang code roi pack (it can dung; se ghi de sprite nhap, KHONG dong vao lynnie_1.png).

SUA CHU  (o dau phan <script> cua tools/template.html, hoac truc tiep index.html; sua template thi chay lai pack.py)
  const TO = "";            ten nguoi nhan (hien o tieu de va cau chuc mung)
  const MESSAGES = [...]    cac cau nhan vat noi moi lan bam nut trai tim (hoac phim Z, hoac bam vao nhan vat). Moi dong 1 cau trong dau ' ',
                            het danh sach thi quay lai cau dau. Viet tieng Viet co dau duoc (font VT323). Nen de duoi ~60 chu.
  const START_NIGHT = false;   true = mo trang len la ban dem.
  const TEXT = {...}        chu tren cac nut va cau noi khi thoi nen. Nut BLOOM va cau 'bloom!' / 'make a wish' nam rai rac trong template.

DOI NGAY / DEM
  Bam nut NIGHT MODE / DAY MODE duoi man hinh, hoac phim N. Muon trang mo len la ban dem: START_NIGHT = true.

TUONG TAC
  Bam len man hinh: nhan vat di toi do.   Phim mui ten / WASD: di chuyen.   Bam nhan vat: loi chuc.
  Nut TRAI TIM TIM / phim Z: loi chuc tiep theo + phao giay.
  BLOW CANDLES / phim X / bam vao ban banh kem: nhan vat chay toi ban, thoi nen, "Happy Birthday!" + phao giay. Nut doi thanh LIGHT CANDLES, bam de dot nen lai.
  BLOOM: tat ca hoa no.   Bam hoa: hoa no.   Bam nha: nhan vat toi cua, cua mo, co loi chuc.   Bam troi: sao bang + dieu uoc.

AM THANH: 7 HOA HUONG DUONG HAT HAPPY BIRTHDAY
  7 hoa huong duong LON (tu trai sang phai) moi hoa phat 1 doan am thanh: 1/7 ... 7/7. Bam hoa -> nhan vat chay toi, hoa no, doan am thanh phat,
  tim tim noi tren hoa dap theo nhac. Hoa nao CHUA co file am thanh thi khong co tim va bam vao chi no hoa.
  Thu tu hoa (trai -> phai): x=6 (hang truoc), x=12, x=80 (sau), x=86 (truoc), x=93, x=101 (truoc), x=106.
  Cach them am thanh (can ffmpeg: https://ffmpeg.org):
    A. Co 1 file duy nhat co du 7 nguoi hat:   python3 tools/split_audio.py file_cua_ban.mp3
         - tu dong tim 6 cho im lang giua cac nguoi de cat. Neu cat sai, tu dat moc giay:
           python3 tools/split_audio.py file.mp3 --times 3.1,6.4,9.8,13,16.5,20
         - hoac chia deu:  python3 tools/split_audio.py file.mp3 --mode equal
         ket qua: sounds/01.mp3 ... sounds/07.mp3
    B. Da co san 7 file: dat ten 01..07 (mp3 / ogg / m4a / wav) vao thu muc sounds/
    Sau do chay:  python3 tools/pack.py   (am thanh duoc nhung thang vao index.html, nen file van chay 1 minh)
  Doi nhan hien tren bong noi (1/7, 2/7, ...): SOUND_LABELS trong tools/template.html, vi du ten tung nguoi.
  Luu y: 7 doan nen ngan (vai giay) de index.html khong qua nang (cam bao ~100-200 KB). Trinh duyet chi cho phat am thanh sau khi nguoi xem bam/cham 1 lan.
  Ban quyen: chi dung file am thanh ban co quyen su dung; tang ca nhan thi ok, dang len mang cong khai thi nen can nhac.

THAY SPRITE CUA BAN
  Tat ca sprite ve CUNG MOT TY LE PIXEL (nhan vat cao 52 px; 1 pixel nhan vat = 1 pixel hoa = 1 pixel nha).
  1. Ve bang Piskel/Aseprite, xuat PNG: cac frame xep 1 hang ngang, cung kich thuoc, nen trong suot.
  2. Ghi de vao sprites/ voi dung ten file:
       lynnie_1.png   27x52 moi frame. Trang chi dung 4 frame dau (co non): dung, buoc trai, buoc phai, chop mat. 4 frame sau (khong non) de du phong.
       sunL.png       26x36 moi frame, 3 frame: hoa lon nghieng trai, thang, nghieng phai
       sunS.png       22x24 moi frame, 3 frame: hoa nho hang sau
       sunLb.png / sunSb.png: ban "sang len" khi nhan vat di gan (khong co thi tu tao)
       house.png      72x60 moi frame, 4 frame: cua dong/den thuong, cua mo/den thuong, cua dong/den sang, cua mo/den sang (ban dem dung 2 frame sang xen ke de nhap nhay)
       table.png      60x32, 1 frame: ban tron phu khan, de banh kem len tren. Mat ban nam o khoang y=9 (tam), banh dat vao do.
       cake.png       32x32 moi frame, 4 frame: nen sang kieu lua A, B, nen tat khoi A, B
       sun.png 28x28, cloud_day.png 40x12                      (ban ngay)
       moon.png 40x40, cloud_night.png 64x20 (2 frame, 2 kieu may), star.png 48x24 (4 frame, sao bang)   (ban dem)
  3. Chay  python3 tools/pack.py
  Doi kich thuoc sprite: sua bang FRAMES trong pack.py. Ve gap 3 lan (hoac khac 2) thi doi K = 2 trong template.html.
  Vi tri ban banh kem: TX, TY trong template.html (tam ban, mep tren ban). Hoa quanh ban da duoc don bot: danh sach addF(...) trong template.html.
