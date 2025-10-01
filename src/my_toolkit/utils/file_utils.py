import os
from pathlib import Path
from werkzeug.utils import secure_filename

def ensure_directory(path: str):
    """确保目录存在"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_safe_filename(filename: str) -> str:
    """生成安全的文件名"""
    return secure_filename(filename)