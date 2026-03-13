#!/usr/bin/env python3
"""
图片尺寸调整程序
专门处理证件照尺寸转换，暂不处理背景
"""

from PIL import Image, ImageEnhance, ImageFilter
import argparse
import os
from pathlib import Path

class PhotoResizer:
    def __init__(self):
        # 常用证件照尺寸预设 (像素)
        self.sizes = {
            "1寸": (600, 840),      # 30mm × 42mm
            "2寸": (708, 1063),     # 35mm × 53mm
            "小2寸": (567, 850),    # 28.3mm × 42.5mm
            "大1寸": (390, 567),    # 19.5mm × 28.3mm
            "护照": (1134, 1417),   # 48mm × 60mm
            "签证": (1134, 1134),   # 48mm × 48mm
            "驾照": (520, 378),     # 26mm × 32mm (横版)
        }

        # 默认使用1寸
        self.target_width = 600
        self.target_height = 840
        self.size_name = "1寸"

    def set_size(self, size_name):
        """设置目标尺寸"""
        if size_name in self.sizes:
            self.target_width, self.target_height = self.sizes[size_name]
            self.size_name = size_name
            print(f"✅ 设置目标尺寸: {size_name} ({self.target_width}×{self.target_height}px)")
        else:
            available = ", ".join(self.sizes.keys())
            raise ValueError(f"不支持的尺寸: {size_name}。可用尺寸: {available}")

    def set_custom_size(self, width, height):
        """设置自定义尺寸"""
        self.target_width = width
        self.target_height = height
        self.size_name = f"自定义{width}×{height}"
        print(f"✅ 设置自定义尺寸: {width}×{height}px")

    def smart_crop_portrait(self, img):
        """
        智能裁剪人像：优先保持人物居中
        """
        width, height = img.size
        target_ratio = self.target_width / self.target_height
        current_ratio = width / height

        if abs(current_ratio - target_ratio) < 0.05:
            # 比例已经很接近，直接返回
            return img

        if current_ratio > target_ratio:
            # 图像太宽，裁剪宽度
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            right = left + new_width
            top, bottom = 0, height
            print(f"📐 裁剪宽度: {width}→{new_width}px (居中裁剪)")
        else:
            # 图像太高，裁剪高度
            new_height = int(width / target_ratio)
            # 人像通常在上半部分，从10%位置开始
            top = max(0, int(height * 0.1))
            bottom = min(height, top + new_height)
            if bottom - top < new_height:
                top = max(0, bottom - new_height)
            left, right = 0, width
            print(f"📐 裁剪高度: {height}→{new_height}px (偏上裁剪)")

        return img.crop((left, top, right, bottom))

    def resize_with_padding(self, img, pad_color=(255, 255, 255)):
        """
        调整尺寸，不足部分用指定颜色填充
        """
        # 先等比例缩放到目标范围内
        img_ratio = img.width / img.height
        target_ratio = self.target_width / self.target_height

        if img_ratio > target_ratio:
            # 以宽度为准
            new_width = self.target_width
            new_height = int(self.target_width / img_ratio)
        else:
            # 以高度为准
            new_height = self.target_height
            new_width = int(self.target_height * img_ratio)

        # 高质量缩放
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"🔄 缩放至: {new_width}×{new_height}px")

        # 如果尺寸完全匹配，直接返回
        if new_width == self.target_width and new_height == self.target_height:
            return resized_img

        # 创建目标尺寸的背景
        result = Image.new('RGB', (self.target_width, self.target_height), pad_color)

        # 计算居中位置
        x = (self.target_width - new_width) // 2
        y = (self.target_height - new_height) // 2

        # 粘贴图像到中心
        result.paste(resized_img, (x, y))
        print(f"📏 填充至标准尺寸: {self.target_width}×{self.target_height}px")

        return result

    def resize_with_crop(self, img):
        """
        调整尺寸，超出部分裁剪掉
        """
        # 等比例缩放到刚好覆盖目标尺寸
        img_ratio = img.width / img.height
        target_ratio = self.target_width / self.target_height

        if img_ratio > target_ratio:
            # 以高度为准
            new_height = self.target_height
            new_width = int(self.target_height * img_ratio)
        else:
            # 以宽度为准
            new_width = self.target_width
            new_height = int(self.target_width / img_ratio)

        # 高质量缩放
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"🔄 缩放至: {new_width}×{new_height}px")

        # 如果尺寸完全匹配，直接返回
        if new_width == self.target_width and new_height == self.target_height:
            return resized_img

        # 居中裁剪到目标尺寸
        left = (new_width - self.target_width) // 2
        top = (new_height - self.target_height) // 2
        right = left + self.target_width
        bottom = top + self.target_height

        result = resized_img.crop((left, top, right, bottom))
        print(f"✂️  裁剪至标准尺寸: {self.target_width}×{self.target_height}px")

        return result

    def enhance_quality(self, img):
        """
        轻微增强图像质量
        """
        # 轻微锐化
        img = img.filter(ImageFilter.UnsharpMask(radius=0.5, percent=100, threshold=2))

        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.05)

        return img

    def process_photo(self, input_path, output_path=None, method="smart"):
        """
        处理照片主流程

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            method: 处理方法 ("smart", "crop", "pad")
        """
        try:
            print(f"📸 正在处理: {input_path}")

            # 1. 读取图像
            img = Image.open(input_path)
            original_size = img.size
            print(f"📐 原始尺寸: {original_size[0]}×{original_size[1]}px")

            # 2. 根据方法处理
            if method == "smart":
                # 智能裁剪 + 填充
                img = self.smart_crop_portrait(img)
                img = self.resize_with_padding(img)
            elif method == "crop":
                # 纯裁剪方式
                img = self.resize_with_crop(img)
            elif method == "pad":
                # 纯填充方式
                img = self.resize_with_padding(img)
            else:
                raise ValueError(f"不支持的处理方法: {method}")

            # 3. 质量增强
            print("✨ 增强图像质量...")
            img = self.enhance_quality(img)

            # 4. 保存结果
            if output_path is None:
                input_file = Path(input_path)
                suffix = f"_{self.size_name}_{method}"
                output_path = input_file.parent / f"{input_file.stem}{suffix}.jpg"

            print("💾 保存图像...")
            # 以高质量保存，设置DPI
            img.save(output_path, 'JPEG', quality=95, dpi=(300, 300))

            print("✅ 处理完成！")
            print(f"📤 输出文件: {output_path}")
            print(f"📏 目标尺寸: {self.size_name} ({self.target_width}×{self.target_height}px)")

            return str(output_path)

        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            raise

    def list_sizes(self):
        """列出所有可用尺寸"""
        print("📋 可用的证件照尺寸:")
        for name, (w, h) in self.sizes.items():
            # 计算物理尺寸 (按300 DPI)
            mm_w = round(w * 25.4 / 300, 1)
            mm_h = round(h * 25.4 / 300, 1)
            print(f"  {name:6} {w:4}×{h:4}px  ({mm_w:4.1f}×{mm_h:4.1f}mm)")

def batch_process(input_dir, size="1寸", method="smart", output_dir=None):
    """
    批量处理功能
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        return

    if output_dir is None:
        output_dir = input_path / f"调整尺寸_{size}_{method}"

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    resizer = PhotoResizer()
    resizer.set_size(size)

    # 支持的图像格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = [f for f in input_path.iterdir()
                   if f.suffix.lower() in image_extensions]

    if not image_files:
        print("❌ 没有找到支持的图像文件")
        return

    print(f"🔍 找到 {len(image_files)} 个图像文件")

    for i, img_file in enumerate(image_files, 1):
        try:
            print(f"\n[{i}/{len(image_files)}] 处理: {img_file.name}")
            output_file = output_path / f"{img_file.stem}_{size}_{method}.jpg"
            resizer.process_photo(str(img_file), str(output_file), method)
        except Exception as e:
            print(f"❌ 处理 {img_file.name} 失败: {e}")
            continue

    print(f"\n🎉 批量处理完成！输出目录: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='图片尺寸调整程序 - 专门处理证件照尺寸',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python photo_resizer.py input.jpg                          # 调整为1寸
  python photo_resizer.py input.jpg -s 2寸                   # 调整为2寸
  python photo_resizer.py input.jpg -s 护照                  # 调整为护照尺寸
  python photo_resizer.py input.jpg --custom 400 600         # 自定义尺寸
  python photo_resizer.py input.jpg -m crop                  # 使用裁剪方式
  python photo_resizer.py input.jpg -m pad                   # 使用填充方式
  python photo_resizer.py -b /path/to/photos -s 2寸          # 批量处理
  python photo_resizer.py --list                            # 列出所有尺寸

处理方法:
  smart: 智能裁剪+填充 (默认，推荐)
  crop:  裁剪方式 (可能丢失边缘内容)
  pad:   填充方式 (可能有白边)
        """)

    parser.add_argument('input', nargs='?', help='输入图像文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-s', '--size', default='1寸', help='目标尺寸 (默认: 1寸)')
    parser.add_argument('-m', '--method', choices=['smart', 'crop', 'pad'],
                       default='smart', help='处理方法 (默认: smart)')
    parser.add_argument('--custom', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                       help='自定义尺寸 (宽度 高度)')
    parser.add_argument('-b', '--batch', metavar='DIR', help='批量处理目录')
    parser.add_argument('--list', action='store_true', help='列出所有可用尺寸')
    parser.add_argument('--show', action='store_true', help='处理完成后显示图片')

    args = parser.parse_args()

    # 列出尺寸
    if args.list:
        resizer = PhotoResizer()
        resizer.list_sizes()
        return

    # 批量处理
    if args.batch:
        batch_process(args.batch, args.size, args.method)
        return

    # 单文件处理
    if not args.input:
        parser.print_help()
        return

    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}")
        return

    resizer = PhotoResizer()

    try:
        # 设置尺寸
        if args.custom:
            resizer.set_custom_size(args.custom[0], args.custom[1])
        else:
            resizer.set_size(args.size)

        # 处理照片
        output_path = resizer.process_photo(args.input, args.output, args.method)

        # 显示结果
        if args.show:
            try:
                img = Image.open(output_path)
                img.show()
            except Exception as e:
                print(f"⚠️  无法显示图片: {e}")

    except Exception as e:
        print(f"❌ 处理失败: {e}")

if __name__ == "__main__":
    main()