import os
import requests
import time
import itertools
import datetime

# API URLs
version_api_url = "https://terraria.org/api/get/dedicated-servers-names"
download_base_url = "https://terraria.org/api/download/mobile-dedicated-server/"
# 电脑版本是 https://terraria.org/api/download/pc-dedicated-server/

# 本地目录，检查现有文件
local_directory = "./dow"
log_file = "version_log.txt"  # 版本日志文件

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")
    else:
        print(f"目录已存在: {directory}")

def get_remote_versions():
    print("获取远程版本信息...")
    try:
        response = requests.get(version_api_url)
        response.raise_for_status()
        print(f"成功获取远程版本信息-{response}")
        print(f"官网最新版本api: {set(response.json())}\n")
        return list(set(response.json()))  # 去重
    except requests.RequestException as e:
        print(f"获取远程版本信息时出错: {e}")
        return []

def get_local_versions(directory):
    print("检查本地版本...")
    local_versions = []

    for filename in os.listdir(directory):
        if filename.startswith("terraria-server-") and filename.endswith(".zip"):
            version = filename.split("-")[2].replace(".zip", "")
            local_versions.append(version)
            print(f"找到本地版本: {version}")

    if not local_versions:
        try:
            with open(log_file, 'r') as log:
                for line in log:
                    if line.startswith("last_down_version = "):
                        version = line.split("=")[1].strip()
                        local_versions.append(version)
                        print(f"从日志文件中读取到版本: {version}")
        except FileNotFoundError:
            print("未找到版本日志文件")

    if not local_versions:
        print("未找到任何本地版本")

    return local_versions



def download_file(filename):
    url = download_base_url + filename
    print(f"开始下载文件: {filename}...")
    
    # 创建循环迭代器
    spinner = itertools.cycle(['owo', 'ovo', '>-<', '>o<'])
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 每次读取的块大小

        downloaded_size = 0
        last_print_time = time.time()

        with open(os.path.join(local_directory, filename), 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded_size += len(data)

                # 刷新进度
                if time.time() - last_print_time >= 0.2:
                    progress = (downloaded_size / total_size) * 100
                    #spinner_char = next(spinner)  # 获取下一个动画字符
                    spinner_chars = ''.join([next(spinner) for _ in range(1)])
                    # 输出
                    print(f"\n已下载: {downloaded_size} / {total_size} bytes ({progress:.2f}%) {spinner_chars}", end='')
                    last_print_time = time.time()

        # 下载完成后换行
        print(f"\n下载完成: {filename}")
    except requests.RequestException as e:
        print(f"下载 {filename} 时出错: {e}")


def log_version(version):
    print(f"记录最新版本号: {version}")
    
    # 读取现有的日志文件内容
    try:
        with open(log_file, 'r') as log:
            lines = log.readlines()
    except FileNotFoundError:
        lines = []

    # 查找并替换特定字段
    field_found = False
    for i, line in enumerate(lines):
        if line.startswith("last_down_version = "):
            lines[i] = f"last_down_version = {version}\n"
            field_found = True
            break

    # 如果没有找到字段，则添加新的字段
    if not field_found:
        lines.append(f"last_down_version = {version}\n")

    # 写回修改后的内容
    with open(log_file, 'w') as log:
        log.writelines(lines)
        # 其他信息写入
        if not any(line.startswith("xk730 = ") for line in lines):
            log.write(f"xk730 = kyzh0730@gmail.com\n")


def check_for_updates():
    print("---更新检查系统版本:1.1.1---")
    print("正在执行更新检查...")
    ensure_directory_exists(local_directory)

    remote_versions = get_remote_versions()
    local_versions = get_local_versions(local_directory)

    for remote_file in remote_versions:
        remote_version = remote_file.split("-")[2].replace(".zip", "")
        
        if all(remote_version > local_version for local_version in local_versions):
            download_file(remote_file)
            log_version(remote_version)

    print("更新检查完毕")

if __name__ == "__main__":
    check_for_updates()
