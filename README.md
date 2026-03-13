# 照片尺寸调整工具

一个专注于图片尺寸调整的Python工具，支持多种证件照尺寸和智能处理方式。

## 🎯 核心功能

- ✅ **多尺寸支持**: 7种证件照预设 + 自定义尺寸
- ✅ **智能处理**: 3种处理方式 (智能、裁剪、填充)
- ✅ **高质量输出**: 300 DPI，适合打印
- ✅ **批量处理**: 一次处理整个文件夹
- ✅ **简单易用**: 仅需 Pillow 一个依赖
- ✅ **快速安装**: 使用 uv 超快部署

## 安装和运行

### 前提条件
首先安装 uv (如果还没有安装):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或通过 Homebrew (macOS)
brew install uv
```

## 🚀 快速开始

```bash
# 1. 安装 uv (如果还没有)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装依赖
uv sync

# 3. 查看所有可用尺寸
uv run python photo_resizer.py --list

# 4. 调整图片尺寸
uv run python photo_resizer.py input.jpg -s 2寸

# 5. 批量处理
uv run python photo_resizer.py -b /path/to/photos -s 护照
```

### 处理方式对比

| 方式 | 描述 | 适用场景 |
|------|------|----------|
| `smart` | 智能裁剪+填充 (默认) | 🏆 推荐，保持人像完整 |
| `crop` | 等比缩放后裁剪 | 不介意丢失边缘内容 |
| `pad` | 等比缩放后填充 | 保持完整内容，可接受白边 |

```bash
# 不同处理方式示例
uv run python photo_resizer.py input.jpg -m smart  # 智能方式
uv run python photo_resizer.py input.jpg -m crop   # 裁剪方式
uv run python photo_resizer.py input.jpg -m pad    # 填充方式
```

## 📐 支持的尺寸

| 名称 | 像素尺寸 | 物理尺寸 | 用途 |
|------|----------|----------|------|
| 1寸 | 600×840px | 30×42mm | 标准证件照 |
| 2寸 | 708×1063px | 35×53mm | 大尺寸证件照 |
| 小2寸 | 567×850px | 28.3×42.5mm | 小证件照 |
| 大1寸 | 390×567px | 19.5×28.3mm | 迷你证件照 |
| 护照 | 1134×1417px | 48×60mm | 护照申请 |
| 签证 | 1134×1134px | 48×48mm | 签证申请 |
| 驾照 | 520×378px | 26×32mm | 驾驶证 (横版) |

```bash
# 查看完整列表
uv run python photo_resizer.py --list
```

## 🎨 使用示例

### 常见尺寸调整
```bash
# 1寸证件照 (默认)
uv run python photo_resizer.py selfie.jpg

# 2寸证件照
uv run python photo_resizer.py portrait.jpg -s 2寸

# 护照照片
uv run python photo_resizer.py photo.jpg -s 护照 -m smart

# 自定义尺寸 (社交媒体头像)
uv run python photo_resizer.py avatar.jpg --custom 400 400
```

### 批量处理
```bash
# 处理整个文件夹
uv run python photo_resizer.py -b ./photos -s 2寸

# 输出会保存在: ./photos/调整尺寸_2寸_smart/
```

### 不同处理方式
```bash
# 智能方式 (推荐，平衡质量和完整性)
uv run python photo_resizer.py input.jpg -m smart

# 裁剪方式 (保持清晰度，可能丢失边缘)
uv run python photo_resizer.py input.jpg -m crop

# 填充方式 (保持完整，可能有白边)
uv run python photo_resizer.py input.jpg -m pad
```

## 🔧 安装选项

### 基础安装 (推荐)
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# 或: brew install uv

# 安装项目
uv sync

# 开始使用
uv run python photo_resizer.py --help
```

### 命令行工具
```bash
# 激活环境后可直接使用
uv shell
photo-resize input.jpg -s 2寸
```

### 开发模式
```bash
# 安装开发工具
uv sync --extra dev

# 代码格式化
uv run black .
uv run isort .
```

## 🚀 Python API 使用

```python
# 激活环境
# uv shell

from photo_resizer import PhotoResizer, batch_process

# 单个文件处理
resizer = PhotoResizer()
resizer.set_size("2寸")  # 设置预设尺寸
# 或 resizer.set_custom_size(400, 600)  # 自定义尺寸

output_path = resizer.process_photo('input.jpg', method='smart')
print(f"处理完成: {output_path}")

# 批量处理
batch_process('./photos', size='护照', method='smart')
```

## 📁 项目结构

```
picture_resize/
├── photo_resizer.py       # 🏆 主程序 (尺寸调整工具)
├── pyproject.toml        # uv 项目配置
├── .gitignore           # Git 忽略文件
└── README.md            # 使用说明
```

**依赖**: 仅需 `Pillow` - 轻量、快速、可靠！

## 🔧 技术规格

### 输入输出格式
- **输入格式**: JPG, JPEG, PNG, BMP, TIFF, WebP
- **输出格式**: JPG (高质量, 300 DPI)
- **颜色空间**: RGB
- **质量设置**: 95% JPEG 质量

### 处理算法
- **缩放算法**: Lanczos 重采样 (高质量)
- **锐化**: UnsharpMask 滤镜
- **对比度增强**: 轻微优化 (5%)
- **DPI设置**: 300 DPI (适合打印)

## 📝 使用技巧

### 获得最佳效果
1. **原图质量**: 使用高分辨率原图 (建议 ≥ 1000px)
2. **人像位置**: 确保人物居中，头部占图片约1/3
3. **光线条件**: 充足均匀的光线，避免阴影
4. **服装要求**: 深色衣服 (黑色或深色正装)

### 处理方式选择
- **人像较小**: 选择 `pad` 模式，避免过度放大
- **人像较大**: 选择 `crop` 模式，保持清晰度
- **不确定**: 选择 `smart` 模式 (默认)，自动优化

### 批量处理技巧
```bash
# 处理不同尺寸到同一目录
uv run python photo_resizer.py -b ./photos -s 1寸 -m smart
uv run python photo_resizer.py -b ./photos -s 2寸 -m smart
uv run python photo_resizer.py -b ./photos -s 护照 -m smart
```

## ⚠️ 故障排除

### 常见问题

1. **输出图片模糊**
   ```bash
   # 解决方案：使用更高分辨率原图，避免过度放大
   uv run python photo_resizer.py input.jpg -s 1寸 -m pad
   ```

2. **人像被裁掉头部**
   ```bash
   # 解决方案：使用填充模式或检查原图人像位置
   uv run python photo_resizer.py input.jpg -m pad
   ```

3. **输出尺寸不对**
   ```bash
   # 检查可用尺寸
   uv run python photo_resizer.py --list

   # 使用自定义尺寸
   uv run python photo_resizer.py input.jpg --custom 600 840
   ```

4. **批量处理失败**
   ```bash
   # 检查目录是否存在和权限
   ls -la /path/to/photos

   # 使用绝对路径
   uv run python photo_resizer.py -b "$(pwd)/photos"
   ```

### 错误信息说明

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `文件不存在` | 路径错误 | 检查文件路径，使用绝对路径 |
| `不支持的尺寸` | 尺寸名称错误 | 使用 `--list` 查看可用尺寸 |
| `无法读取图像` | 格式不支持 | 转换为 JPG/PNG 格式 |
| `权限被拒绝` | 无写入权限 | 检查输出目录权限 |

## 进阶使用

### 自定义尺寸

如需其他尺寸的证件照，可以修改代码中的参数：

```python
# 在 SimpleIDPhotoProcessor 类中修改
self.target_width = 600   # 宽度
self.target_height = 840  # 高度
```

常用证件照尺寸：
- 1寸: 600×840px (30×42mm)
- 2寸: 708×1063px (35×53mm)
- 小2寸: 567×850px (28.3×42.5mm)

## 🚀 开发和API

### Python API 使用

```python
# 激活环境
# uv shell

from photo_resizer import PhotoResizer

# 创建处理器
resizer = PhotoResizer()

# 设置尺寸
resizer.set_size("2寸")  # 或使用预设尺寸
resizer.set_custom_size(400, 600)  # 或自定义尺寸

# 处理图片
output_path = resizer.process_photo('input.jpg', method='smart')
print(f"处理完成: {output_path}")

# 批量处理
from photo_resizer import batch_process
batch_process('./photos', size='护照', method='smart')
```

### 开发工具

```bash
# 安装开发依赖
uv sync --extra dev

# 代码格式化
uv run black .
uv run isort .

# 类型检查
uv run mypy photo_resizer.py

# 测试 (如果有)
uv run pytest
```

### 项目结构
```
picture_resize/
├── photo_resizer.py        # 🏆 主要工具 (尺寸调整)
├── id_photo_simple.py      # 简单证件照处理
├── id_photo_processor.py   # 高级证件照处理 (需OpenCV)
├── pyproject.toml         # uv 项目配置
├── .gitignore            # Git 忽略文件
└── README.md             # 使用说明
```

## 许可证

MIT License - 可自由使用和修改

---

**为什么选择 uv？**
- 🚀 比 pip 快 10-100 倍的安装速度
- 🔒 自动依赖锁定，确保环境一致性
- 🛠️ 内置虚拟环境管理
- 📦 现代化的 Python 项目工具链
