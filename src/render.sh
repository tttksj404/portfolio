#!/bin/sh
# out/*.html을 Chrome 헤드리스로 2배 렌더하고 여백을 잘라 out/*.png로 저장한다. 인자: html 파일 이름들(생략하면 전부)
CH="${CHROME:-/c/Program Files/Google/Chrome/Application/chrome.exe}"
cd "$(dirname "$0")/out" || exit 1
D="$(pwd -W 2>/dev/null || pwd)"
for f in ${1:-*.html}; do b=${f%.html}; "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=940,1400 --screenshot="$D/$b.raw.png" "file:///$D/$f" >/dev/null 2>&1; done
python - <<'PY'
from PIL import Image, ImageChops
import glob, os
for p in sorted(glob.glob("*.raw.png")):
    im = Image.open(p).convert("RGB")
    bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    if bb:
        l, t, r, b = bb
        im = im.crop((max(l - 6, 0), max(t - 6, 0), min(r + 6, im.width), min(b + 6, im.height)))
    im.save(p.replace(".raw.png", ".png"), optimize=True)
    os.remove(p)
    print(p.replace(".raw.png", ""), im.size)
PY
