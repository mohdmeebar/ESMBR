"""Cuts the Deem wordmark and Deem product photos out of the client's images.
Usage: python3 -I deem_assets.py <uploads dir> <project assets dir>
Text and logos printed on the marketing photos are painted out with the
background colour of the same row, so only the product remains."""
import sys
from PIL import Image

UP, OUT = sys.argv[1], sys.argv[2]
S = 800


def load(fid):
    return Image.open(f"{UP}/{fid}-image.jpg").convert("RGB")


def paint_out(im, box, sample_x):
    """Fill box row by row with the pixel colour at column sample_x."""
    px = im.load()
    l, t, r, b = box
    for y in range(t, b):
        c = px[sample_x, y]
        for x in range(l, r):
            px[x, y] = c


def square(im, box, name, pad_rows=False):
    l, t, r, b = box
    w, h = r - l, b - t
    crop = im.crop(box)
    if w != h:
        side = max(w, h)
        canvas = Image.new("RGB", (side, side))
        # extend the crop's own edge rows / columns into the padding
        if w < h:
            dx = (side - w) // 2
            for y in range(side):
                canvas.paste(crop.getpixel((0, y)), (0, y, dx, y + 1))
                canvas.paste(crop.getpixel((w - 1, y)), (dx + w, y, side, y + 1))
            canvas.paste(crop, (dx, 0))
        else:
            dy = (side - h) // 2
            for x in range(side):
                canvas.paste(crop.getpixel((x, 0)), (x, 0, x + 1, dy))
                canvas.paste(crop.getpixel((x, h - 1)), (x, dy + h, x + 1, side))
            canvas.paste(crop, (0, dy))
        crop = canvas
    crop.resize((S, S), Image.LANCZOS).save(f"{OUT}/products/{name}", quality=90)


# Deem wordmark: white letters on grey -> transparent PNG
src = load("a116a903")
mark = src.crop((80, 120, 450, 300)).convert("L")
alpha = mark.point(lambda v: max(0, min(255, int((v - 125) * 2.4))))
bb = alpha.point(lambda v: 255 if v > 60 else 0).getbbox()
alpha = alpha.crop((bb[0] - 8, bb[1] - 8, bb[2] + 8, bb[3] + 8))
alpha = alpha.resize((alpha.width * 3, alpha.height * 3), Image.LANCZOS)
logo = Image.new("RGBA", alpha.size, (246, 236, 214, 0))
logo.putalpha(alpha)
logo.save(f"{OUT}/deem-cream.png")
print("deem", logo.size)

# dallas (gold, silver): square crops below the Arab Dalla mark
square(load("5f128e28"), (160, 400, 1439, 1679), "deem-1.jpg")
square(load("59a6ce94"), (100, 400, 1379, 1679), "deem-2.jpg")

# Guests Dalla: paint out the wordmark and the headline, keep the appliance
im = load("a116a903")
paint_out(im, (70, 110, 460, 310), 30)
paint_out(im, (870, 110, 1420, 520), 1432)
square(im, (90, 120, 1350, 1380), "deem-3.jpg")

# Milk heater: paint out the "one touch" badge, crop to the jug
im = load("c8f343e2")
paint_out(im, (300, 570, 670, 770), 290)
square(im, (380, 290, 1440, 1350), "deem-4.jpg")

# Karak tea maker: the headline sits above the pot, so crop below it
square(load("04d9d55a"), (110, 440, 1108, 1438), "deem-5.jpg")

# Turkish coffee maker: wide shot, padded to a square from its own edges
im = load("f55d468c")
paint_out(im, (1260, 20, 1440, 110), 1250)
square(im, (330, 60, 1440, 804), "deem-6.jpg")
