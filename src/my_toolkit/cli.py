import argparse
from my_toolkit import image_utils

def main():
    parser = argparse.ArgumentParser(description="图像处理工具")
    subparsers = parser.add_subparsers(dest="command", help = '可用命令')

    # 图片处理
    img_parser = subparsers.add_parser('resize',help = '调整图像大小')
    img_parser.add_argument('--input', type=str, help='输入文件夹')
    img_parser.add_argument('--output', type=str, help='输出文件夹')
    img_parser.add_argument('--width', type=int, default=800, help='宽度')
    img_parser.add_argument('--height', type=int, default=600, help='高度')
    
    args = parser.parse_args()

    if args.command == 'resize':
        image_utils.resize_images(args.input, args.output, size=(args.width, args.height))  
        print("图片处理完成!")

if __name__ == "__main__":
    main()