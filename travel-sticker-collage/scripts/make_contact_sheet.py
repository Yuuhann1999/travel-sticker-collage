#!/usr/bin/env python3
"""把多张照片整理成带编号的临时素材板，供图像生成模型识别。"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def make_sheet(paths: list[Path], start_index: int, args: argparse.Namespace) -> Image.Image:
    """按输入顺序生成一张素材板。"""
    gutter = max(8, args.cell_size // 32)
    rows = (len(paths) + args.columns - 1) // args.columns
    width = gutter + args.columns * (args.cell_size + gutter)
    height = gutter + rows * (args.cell_size + gutter)
    sheet = Image.new("RGB", (width, height), "#f3f1ed")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for offset, path in enumerate(paths):
        image = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        tile = ImageOps.contain(
            image,
            (args.cell_size, args.cell_size),
            method=Image.Resampling.LANCZOS,
        )
        x = gutter + (offset % args.columns) * (args.cell_size + gutter)
        y = gutter + (offset // args.columns) * (args.cell_size + gutter)
        tile_bg = Image.new("RGB", (args.cell_size, args.cell_size), "#dedbd4")
        tile_bg.paste(
            tile,
            ((args.cell_size - tile.width) // 2, (args.cell_size - tile.height) // 2),
        )
        sheet.paste(tile_bg, (x, y))

        label = str(start_index + offset)
        label_box = (x + 10, y + 10, x + 14 + max(28, len(label) * 10), y + 38)
        draw.rounded_rectangle(label_box, radius=9, fill="#111111")
        draw.text((label_box[0] + 9, label_box[1] + 7), label, fill="#ffffff", font=font)

    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description="生成编号素材板")
    parser.add_argument("paths", nargs="+", type=Path, help="输入图片，按传入顺序编号")
    parser.add_argument("--output-dir", required=True, type=Path, help="输出目录")
    parser.add_argument("--prefix", default="contact-sheet", help="输出文件名前缀")
    parser.add_argument("--max-per-sheet", type=int, default=12, help="每张素材板最多放几张图")
    parser.add_argument("--columns", type=int, default=3, help="每行列数")
    parser.add_argument("--cell-size", type=int, default=384, help="单格边长")
    parser.add_argument("--quality", type=int, default=95, help="JPEG 质量")
    args = parser.parse_args()

    if args.max_per_sheet < 1 or args.columns < 1 or args.cell_size < 32:
        parser.error("--max-per-sheet、--columns 必须大于 0，--cell-size 至少为 32")
    for path in args.paths:
        if not path.is_file():
            parser.error(f"找不到输入图片：{path}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for page, offset in enumerate(range(0, len(args.paths), args.max_per_sheet), start=1):
        batch = args.paths[offset : offset + args.max_per_sheet]
        sheet = make_sheet(batch, offset + 1, args)
        output = args.output_dir / f"{args.prefix}-{page:02d}.jpg"
        sheet.save(output, quality=args.quality, optimize=True)
        output_paths.append(output)

    for output in output_paths:
        print(output)


if __name__ == "__main__":
    main()
