import urllib.request, io, os
from PIL import Image, ImageDraw

os.makedirs("/Users/ybot/Mission_Control_Pokemon/icons", exist_ok=True)

url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png"
req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
sprite = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=15).read())).convert("RGBA")

def make_icon(size):
    img = Image.new("RGBA", (size, size), (8, 9, 10, 255))
    d = ImageDraw.Draw(img)
    for i in range(size // 2, 0, -1):
        t = i / (size // 2)
        r = int(8 + (94 - 8) * (1 - t))
        g = int(9 + (106 - 9) * (1 - t))
        b = int(10 + (210 - 10) * (1 - t))
        d.ellipse([size // 2 - i, size // 2 - i, size // 2 + i, size // 2 + i], fill=(r, g, b, 255))
    s = int(size * 0.62)
    sp = sprite.resize((s, s), Image.NEAREST)
    img.paste(sp, ((size - s) // 2, (size - s) // 2), sp)
    return img

for size in [192, 512]:
    make_icon(size).save(f"/Users/ybot/Mission_Control_Pokemon/icons/icon-{size}.png")
    print(f"icon-{size}.png written")

make_icon(512).save("/Users/ybot/Mission_Control_Pokemon/icons/icon-512-maskable.png")
print("done")
