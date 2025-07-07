import os
import json
import argparse

def is_png_file(filename):
    return filename.lower().endswith('.png')

def generate_dataset_json(source_dir, output_file):
    dataset = {"labels": []}
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if is_png_file(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)
                label = os.path.basename(root)  # Use the name of the subfolder as the label
                dataset["labels"].append([relative_path.replace("\\", "/"), label])
    
    # 写入文件时手动格式化
    with open(output_file, 'w') as f:
        f.write('{\n  "labels": [\n')
        for idx, item in enumerate(dataset["labels"]):
            f.write('    ' + json.dumps(item))
            if idx < len(dataset["labels"]) - 1:
                f.write(',')
            f.write('\n')
        f.write('  ]\n}')
    
    print(f"dataset.json has been created with {len(dataset['labels'])} items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a JSON dataset of PNG images.')
    parser.add_argument('source_directory', type=str, help='The source directory containing the image files.')
    parser.add_argument('output_file', type=str, help='The output JSON file.')

    args = parser.parse_args()

    generate_dataset_json(args.source_directory, args.output_file)
