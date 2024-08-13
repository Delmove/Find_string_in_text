import os


def search_string_in_files(folder_path, file_extension, search_string):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_path = os.path.join(root, file_name)

                # 检查文件名是否包含搜索字符串
                if search_string in file_name:
                    results.append((file_path, 'Filename Match', file_name))

                # 检查文件内容是否包含搜索字符串
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_number, line in enumerate(file, 1):
                        if search_string in line:
                            results.append((file_path, line_number, line.strip()))
    return results
