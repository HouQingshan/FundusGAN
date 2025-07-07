import os
import shutil

def copy_and_rename_images(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 获取源文件夹下的所有文件
    files = os.listdir(src_dir)
    
    # 过滤图像文件
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # 按文件名排序
    image_files.sort()
    
    for i, filename in enumerate(image_files):
        # 源文件路径
        src_path = os.path.join(src_dir, filename)
        
        # 新的文件名，统一为png格式
        new_filename = f"{i + 1:04d}.png"
        
        # 目标文件路径
        dest_path = os.path.join(dest_dir, new_filename)
        
        # 复制并重命名文件
        shutil.copyfile(src_path, dest_path)
    
    print(f"Copied and renamed {len(image_files)} images from {src_dir} to {dest_dir}")

# 示例用法
src_dir = "/home/hou_qingshan/QS/EYE-52/EYE-52/Albinism"
dest_dir = "/home/hou_qingshan/QS/EYE-process/Albinism"

copy_and_rename_images(src_dir, dest_dir)