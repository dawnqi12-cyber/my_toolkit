from setuptools import setup, find_packages

setup(
    name="my-toolkit",
    version="0.1.0",
    packages=find_packages(where="src"),  # ✅ 修正：packages（复数）
    package_dir={"": "src"},
    install_requires=[
        "Pillow>=8.0.0",
        "pydub>=0.25.0",  # ✅ 修正：去掉空格
    ],
    entry_points={
        "console_scripts": [
            "my-toolkit=my_toolkit.cli:main",  # ✅ 修正：等号两边不要空格
        ],
    },
    author="Dawn qi",
    description="个人实用工具集合。",  # ✅ 修正：description 拼写
)