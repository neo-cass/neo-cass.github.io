#!/usr/bin/env python3
"""Regenerate every derived image on the site from the untouched originals.

The originals (iPhone HEIC/JPEG files with EXIF, GPS and colour profiles) are
NOT stored in this repo. Everything published is produced here, so the process
is reproducible and can never leak metadata:

  * pixels are converted to sRGB, then saved WITHOUT any EXIF / XMP / ICC block
  * the output is re-read and the script fails if any metadata survived

Usage (nothing is installed globally; uv builds a throwaway environment):

  uv run --with pillow --with pillow-heif --with pymupdf \\
      python scripts/build_images.py --originals /path/to/originals [--cv-pdf /path/to/cv.pdf]

Outputs
All under public/ (copied to the site by scripts/build.py):
  assets/images/profile.webp                   avatar (400 px)
  assets/images/og-image.jpg                   1200x630 social-share card
  assets/images/gallery/<name>.webp            1200 px, shown on click
  assets/images/gallery/thumbs/<name>.webp     640 px, shown in the strip
  assets/images/cv-preview.webp                first page of the CV (only with --cv-pdf)
  assets/icons/icon-192.png, apple-touch-icon.png, favicon.ico

The CV preview is a snapshot: re-run with --cv-pdf whenever the CV changes.
"""
import argparse
import io
import sys
from pathlib import Path

import pillow_heif
import pymupdf
from PIL import Image, ImageCms, ImageDraw, ImageOps

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
IMG = PUBLIC / "assets" / "images"
ICONS = PUBLIC / "assets" / "icons"

# name -> (original file, crop box in upright pixels). Crops are deliberately
# minimal: only dead space (ceiling, a stranger's shoes) is trimmed.
GALLERY = {
    "cern-tunnel": ("IMG_1860.HEIC", (0, 0, 3024, 4032)),
    "graduation": ("IMG_5073.HEIC", (0, 0, 3024, 4032)),
    "thesis-talk": ("IMG_1909.HEIC", (480, 700, 2500, 3300)),  # screen + speaker + lectern
    "poster-day": ("IMG_2651.jpeg", (0, 0, 2733, 2540)),
}
PROFILE = ("IMG_5073.HEIC", (1062, 740, 1922, 1600))  # head and shoulders
FACE = ("IMG_5073.HEIC", (1208, 812, 1776, 1380))     # tight crop for tiny icons
OG = ("IMG_5073.HEIC", (480, 560, 2480, 1610))        # 1200:630 ratio

SRGB = ImageCms.createProfile("sRGB")


def load(originals: Path, name: str) -> Image.Image:
    """Open an original as an upright, sRGB, metadata-free RGB image."""
    im = Image.open(originals / name)
    icc = im.info.get("icc_profile")
    im = ImageOps.exif_transpose(im).convert("RGB")
    if icc:
        im = ImageCms.profileToProfile(
            im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB"
        )
    # Pillow's PNG writer re-attaches anything left in .info (e.g. the original
    # colour profile) to every derived image, so clear it at the source.
    im.info.clear()
    return im


def fit_width(im: Image.Image, width: int) -> Image.Image:
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def save_webp(im: Image.Image, path: Path, width: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fit_width(im, width).save(path, "WEBP", quality=82, method=6)


def circle(im: Image.Image, size: int) -> Image.Image:
    """Square RGBA with a smooth circular alpha channel (4x supersampled)."""
    im = im.resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    im.putalpha(mask.resize((size, size), Image.LANCZOS))
    return im


def assert_no_metadata(path: Path) -> None:
    with Image.open(path) as im:
        leaked = [k for k in ("exif", "icc_profile", "xmp", "photoshop") if im.info.get(k)]
        if im.getexif():
            leaked.append("exif-tags")
    if leaked:
        sys.exit(f"metadata survived in {path}: {leaked}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--originals", required=True, type=Path, help="folder holding the original photos")
    ap.add_argument("--cv-pdf", type=Path, help="built CV PDF; renders its first page as the site preview")
    args = ap.parse_args()
    originals = args.originals.expanduser()
    written: list[Path] = []

    for name, (src, box) in GALLERY.items():
        im = load(originals, src).crop(box)
        for path, width in ((IMG / "gallery" / f"{name}.webp", 1200),
                            (IMG / "gallery" / "thumbs" / f"{name}.webp", 640)):
            save_webp(im, path, width)
            written.append(path)

    src, box = PROFILE
    save_webp(load(originals, src).crop(box), IMG / "profile.webp", 400)
    written.append(IMG / "profile.webp")

    src, box = OG
    og = IMG / "og-image.jpg"
    load(originals, src).crop(box).resize((1200, 630), Image.LANCZOS).save(
        og, "JPEG", quality=85, optimize=True, progressive=True)
    written.append(og)

    if args.cv_pdf:
        preview = IMG / "cv-preview.webp"
        pix = pymupdf.open(args.cv_pdf.expanduser())[0].get_pixmap(matrix=pymupdf.Matrix(3, 3))
        save_webp(Image.frombytes("RGB", (pix.width, pix.height), pix.samples), preview, 600)
        written.append(preview)

    # Icons: round favicon with transparency; iOS wants an opaque square.
    src, box = FACE
    face = load(originals, src).crop(box)
    ICONS.mkdir(parents=True, exist_ok=True)
    circle(face, 256).save(PUBLIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    circle(face, 192).quantize(256, method=Image.Quantize.FASTOCTREE).save(
        ICONS / "icon-192.png", optimize=True)
    face.resize((180, 180), Image.LANCZOS).quantize(256).save(
        PUBLIC / "apple-touch-icon.png", optimize=True)
    written += [ICONS / "icon-192.png", PUBLIC / "apple-touch-icon.png", PUBLIC / "favicon.ico"]

    for path in written:
        if path.suffix != ".ico":
            assert_no_metadata(path)
        print(f"{path.relative_to(ROOT)!s:55} {path.stat().st_size / 1024:6.0f} KB")
    print("OK: all outputs re-read, no metadata present.")


if __name__ == "__main__":
    main()
