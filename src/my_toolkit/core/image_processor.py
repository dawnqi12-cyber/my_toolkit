from PIL import Image
import os
from pathlib import Path

def process_image(input_path: str, output_path: str, **operations):
    """
    简化版图像处理函数
    """
    print(f"🎯 开始处理图片: {input_path}")
    print(f"📋 操作参数: {operations}")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    with Image.open(input_path) as img:
        print(f"📊 原始尺寸: {img.size}")
        
        # 应用所有操作
        if 'resize' in operations:
            resize_params = operations['resize']
            width = resize_params['width']
            height = resize_params['height']
            print(f"📏 执行缩放: {width}x{height}")
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            print(f"✅ 缩放后尺寸: {img.size}")


        if operations.get('rotate_left'):
            print("🔄 执行左旋转90度")
            img = img.rotate(90, expand=True)
            print(f"✅ 旋转后尺寸: {img.size}")
        
        if operations.get('rotate_right'):
            print("🔄 执行右旋转90度")
            img = img.rotate(-90, expand=True)
            print(f"✅ 旋转后尺寸: {img.size}")

        if operations.get('flip_horizontal'):
            print("🔄 执行水平左翻转")
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            print(f"✅ 翻转后尺寸: {img.size}")

        if 'compress' in operations:
            compress_params = operations['compress']
            quality = compress_params.get('quality')
            print(f"🗜️ 执行压缩，质量: {quality}")
            img.save(output_path, quality=quality, optimize=True)
        else:
            img.save(output_path)

        # # 保存处理后的图片
        # img.save(output_path)
        print(f"💾 图片已保存: {output_path}")
    
    return True