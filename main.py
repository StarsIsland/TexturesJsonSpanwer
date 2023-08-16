import os
import json

namespace = "starsnature"

simplePath = "textures/item"


def generate_json(directory):
    result = {}
    paths_list = []
    special_json = []  # 用于保存特殊处理的json

    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 只获取文件名，不包括后缀
            name_without_extension, extension = os.path.splitext(filename)

            # 检查文件名是否包含“.png.mcmeta”后缀
            if filename.endswith('.png.mcmeta'):
                # 再次调用os.path.splitext()去除 .png 后缀
                name_without_png_extension, _ = os.path.splitext(name_without_extension)
                json_path = os.path.join(simplePath, name_without_png_extension).replace('\\', '/')
                special_entry = {
                    "flipbook_texture": json_path,
                    "atlas_tile": namespace + "-" + name_without_png_extension,
                    "ticks_per_frame": 10
                }
                special_json.append(special_entry)

                # 获取完整的文件路径并删除文件
                full_file_path = os.path.join(root, filename)
                os.remove(full_file_path)
            else:
                # 生成相对于给定目录的路径
                relative_path = os.path.relpath(root, directory)

                # 清理路径：如果是'.'（代表顶级目录），则将它设置为''
                clean_path = '' if relative_path == '.' else relative_path

                # 生成JSON结构中的路径
                json_path = os.path.join(simplePath, clean_path, name_without_extension).replace('\\', '/')

                # 更新结果字典
                result[namespace + "-" + name_without_extension] = {
                    "textures": {
                        "path": json_path
                    }
                }

                # 将生成的路径添加到列表中
                paths_list.append(json_path)

    # 以格式化的方式将生成的字典转换为JSON字符串
    json_output = json.dumps(result, indent=2)
    return json_output, paths_list, special_json


def save_json_to_file(directory):
    json_output, paths_list, special_json = generate_json(directory)

    # 保存生成的JSON到文件
    with open('output.json', 'w') as file:
        file.write(json_output)

    # 保存路径列表到另一个文件
    with open('paths_list.txt', 'w') as file:
        for path in paths_list:
            file.write("\"" + path + '\",\n')

    # 保存特殊处理的json到另一个文件
    with open('special_json_output.json', 'w') as file:
        json.dump(special_json, file, indent=2)


# 指定要读取文件名的目录
directory_path = "item"

# 调用函数并打印生成的JSON
save_json_to_file(directory_path)
