import os
import json
import shutil
import re

# 读取IP.json文件
with open('IP.json', 'r', encoding='utf-8') as f:
    ip_data = [line.strip() for line in f.readlines()]

# 读取info.json文件
with open('info.json', 'r', encoding='utf-8') as f:
    info_data = json.load(f)

# 获取当前目录下的所有Word文件
word_files = [f for f in os.listdir('.') if f.endswith('.docx') or f.endswith('.doc')]

# 创建结果文件夹
result_folder = '中高危漏洞报告'
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# 初始化计数器
moved_files_count = 0

# 遍历Word文件
for word_file in word_files:
    # 从文件名中提取IP地址
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', word_file)
    if match:
        ip = match.group(1)
        
        # 检查IP是否在IP.json中
        if ip in ip_data:
            # 移动文件到结果文件夹
            src_path = os.path.join('.', word_file)
            dst_path = os.path.join(result_folder, word_file)
            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                moved_files_count += 1
                print(f'移动文件到结果文件夹：{word_file}')
            else:
                print(f'文件不存在，无法移动：{word_file}')

# 进入结果文件夹
os.chdir(result_folder)

# 遍历结果文件夹中的所有Word文件
word_files = [f for f in os.listdir('.') if f.endswith('.docx') or f.endswith('.doc')]

# 遍历每个JSON对象
for entry in info_data:
    ips = entry['ips']
    info_system = entry['information system']

    # 遍历当前目录中的所有 .doc 和 .docx 文件
    for filename in word_files:
        # 从文件名中提取IP地址
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', filename)
        if match:
            ip = match.group(1)
            if ip in ips:
                # 创建文件夹并移动文件
                folder_name = info_system
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                src_path = os.path.join('.', filename)
                dst_path = os.path.join(folder_name, filename)
                if os.path.exists(src_path):
                    shutil.move(src_path, dst_path)
                    moved_files_count += 1
                    print(f'移动文件到{folder_name}：{filename}')
                else:
                    print(f'文件不存在，无法移动：{filename}')

# 输出未匹配的文件名
unmatched_files = []
for filename in os.listdir('.'):
    if filename.endswith('.doc') or filename.endswith('.docx'):
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', filename)
        if match:
            ip = match.group(1)
            if not any(ip in entry['ips'] for entry in info_data):
                unmatched_files.append(filename)

# 输出结果
print(f'处理完成！共移动 {moved_files_count} 个文件。')
if unmatched_files:
    print(f'未匹配的文件：{unmatched_files}')
else:
    print('所有文件均已匹配并移动。')
