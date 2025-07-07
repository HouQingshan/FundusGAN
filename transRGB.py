from PIL import Image
import os

def convert_to_rgb(image_path):
    try:
        with Image.open(image_path) as img:
            # 检查图像是否成功打开
            if img is None:
                raise ValueError("Image could not be opened")
            
            # 如果图像不是 RGB 模式，转换它
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return img
    except Exception as e:
        raise ValueError(f"Error opening image: {str(e)}")

def process_dataset(dataset_path):
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                try:
                    # 检查文件是否存在
                    if not os.path.exists(image_path):
                        print(f"File does not exist: {image_path}")
                        continue

                    # 检查文件大小
                    if os.path.getsize(image_path) == 0:
                        print(f"File is empty: {image_path}")
                        continue

                    img = convert_to_rgb(image_path)
                    # 保存转换后的图像，覆盖原图像
                    img.save(image_path)
                    print(f"Processed: {image_path}")
                except Exception as e:
                    print(f"Error processing {image_path}: {str(e)}")

# 使用示例
dataset_path = '/home/qs/PeojectGAN/EYE-process/Total'
process_dataset(dataset_path)