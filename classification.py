import os
import json
import shutil
import re

# 读取JSON文件
with open('info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历每个JSON对象
for entry in data:
    ips = entry['ips']
    info_system = entry['information system']

    # 遍历当前目录中的所有 .doc 和 .docx 文件
    for filename in os.listdir('.'):
        if filename.endswith('.doc') or filename.endswith('.docx'):
            # 从文件名中提取IP地址
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', filename)
            if match:
                ip = match.group(1)
                if ip in ips:
                    # 创建文件夹并移动文件
                    folder_name = info_system
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    shutil.move(filename, os.path.join(folder_name, filename))

# 输出未匹配的文件名
for filename in os.listdir('.'):
    if filename.endswith('.doc') or filename.endswith('.docx'):
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', filename)
        if match:
            ip = match.group(1)
            if not any(ip in entry['ips'] for entry in data):
                print(f"未匹配的文件: {filename}")