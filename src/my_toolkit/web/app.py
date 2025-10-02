from flask import Flask, render_template, request, jsonify
from pathlib import Path
import uuid
import os  # 添加os模块用于文件操作
from my_toolkit.core.image_processor import process_image
from my_toolkit.utils.file_utils import ensure_directory, get_safe_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制

# 初始化必要目录
ensure_directory('uploads')
ensure_directory('static/processed')

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image_api():
    """
    图片处理API接口
    接收：图片文件 + 处理参数
    返回：JSON格式的处理结果
    """
    try:
        # ========== 添加验证代码：打印请求信息 ==========
        print("\n🔍 === 收到图片处理请求 ===")
        print("📋 表单数据:", dict(request.form))
        print("📁 文件信息:", dict(request.files))
        
        # 1. 验证文件上传
        if 'image' not in request.files:
            print("❌ 错误：请求中未找到image字段")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['image']
        if not file.filename:
            print("❌ 错误：文件名为空")
            return jsonify({'error': 'No selected file'}), 400

        # 2. 生成安全文件名
        original_name = get_safe_filename(file.filename)
        file_id = uuid.uuid4().hex
        file_ext = Path(original_name).suffix.lower()
        
        if file_ext not in ('.jpg', '.jpeg', '.png'):
            print("❌ 错误：不支持的文件类型:", file_ext)
            return jsonify({'error': 'Only JPG/PNG images allowed'}), 400

        # 3. 保存临时文件
        temp_path = Path('uploads') / f"{file_id}{file_ext}"
        file.save(temp_path)
        print(f"✅ 临时文件保存成功: {temp_path}")

        # 4. 准备处理参数
        operations = {}
        resize_flag = request.form.get('resize')
        print(f"📊 resize参数值: '{resize_flag}'")
        
        if resize_flag == 'true':
            width = int(request.form.get('width', 800))
            height = int(request.form.get('height', 600))
            operations['resize'] = {'width': width, 'height': height}
            print(f"📏 缩放尺寸: {width}x{height}")
        else:
            print("⚠️  未启用缩放功能")

        # 新增：处理旋转参数和翻转参数
        if request.form.get('rotate_left') == 'true':
            operations['rotate_left'] = True
            print("🔄 启用左旋90°")
        if request.form.get('rotate_right') == 'true':
            operations['rotate_right'] = True
            print("🔄 启用右旋90°")
        if request.form.get('flip_horizontal') == 'true':
            operations['flip_horizontal'] = True
            print("🔄 启用翻转°")

        # 新增：处理压缩参数
        if request.form.get('compress') == 'true':
            quality = int(request.form.get('quality', 80))
            operations['compress'] = {'quality': quality}
            print(f"🗜️ 启用压缩，质量: {quality}")

        print(f"⚙️  最终操作参数: {operations}")

        # 5. 处理图片
        output_filename = f"processed_{file_id}.jpg"
        output_path = Path('static/processed') / output_filename
        
        # ========== 添加验证代码：记录处理前文件信息 ==========
        original_size = os.path.getsize(temp_path)
        print(f"📊 原始文件大小: {original_size} 字节")
        
        # 调用处理函数
        print("🔄 正在处理图片...")
        process_image(str(temp_path), str(output_path), **operations)
        print("✅ 图片处理函数调用完成")

        # ========== 添加验证代码：记录处理后文件信息 ==========
        if os.path.exists(output_path):
            processed_size = os.path.getsize(output_path)
            print(f"📊 处理后文件大小: {processed_size} 字节")
            print(f"📈 文件大小变化: {processed_size - original_size} 字节")
        else:
            print("❌ 错误：输出文件未生成")

        # 6. 返回结果
        return jsonify({
            'success': True,
            'result_url': f'/static/processed/{output_filename}',
            'download_name': f"processed_{original_name}"
        })
        
    except Exception as e:
        # ========== 添加详细的错误信息 ==========
        print(f"🔥 发生异常: {str(e)}")
        import traceback
        error_traceback = traceback.format_exc()
        print(f"📝 错误堆栈:\n{error_traceback}")
        
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500

@app.after_request
def add_header(response):
    """禁用缓存"""
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)