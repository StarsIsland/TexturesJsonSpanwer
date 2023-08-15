import os
import json

namespace = "starsnature"

simplePath = "textures/blocks/earth"

def generate_json(directory):
    result = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 只获取文件名，不包括后缀
            name_without_extension = os.path.splitext(filename)[0]

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

    # 以格式化的方式将生成的字典转换为JSON字符串
    json_output = json.dumps(result, indent=2)
    return json_output


def save_json_to_file(directory):
    json_output = generate_json(directory)
    with open('output.json', 'w') as file:
        file.write(json_output)


# 指定要读取文件名的目录
directory_path = "earth"

# 调用函数并打印生成的JSON
save_json_to_file(directory_path)