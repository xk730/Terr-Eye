import os
import requests
import time
import itertools
import datetime

# API URLs
version_api_url = "https://terraria.org/api/get/dedicated-servers-names"

mobile_download_base_url = "https://terraria.org/api/download/mobile-dedicated-server/"

pc_download_base_url = "https://terraria.org/api/download/pc-dedicated-server/"


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
        versions = list(set(response.json()))  # 去重并转换为列表
        print(f"成功获取远程版本信息-{response}")
        print(f"官网最新版本api: {versions}\n")
        
        if len(versions) != 2:
            print("警告: 返回的版本信息数量不符合预期，无法区分电脑和移动端版本")
            return [], []

        # 假设第一个是电脑版本，第二个是移动端版本
        pc_version = versions[0]
        mobile_version = versions[1]
        
        return pc_version, mobile_version
    except requests.RequestException as e:
        print(f"获取远程版本信息时出错: {e}")
        return [], []


    

def get_local_versions(directory):
    print("检查本地版本...")
    local_versions = []

    # 检查本地目录中的版本文件
    for filename in os.listdir(directory):
        if filename.startswith("terraria-server-") and filename.endswith(".zip"):
            version = filename.split("-")[2].replace(".zip", "")
            #local_versions.append(version)
            print(f"找到本地版本: {version}")

    # 如果没有找到任何本地版本，尝试从日志文件中读取
    if not local_versions:
        try:
            with open(log_file, 'r') as log:
                for line in log:
                    if line.startswith("last_down_version = "):
                        version = line.split("=")[1].strip()
                        local_versions.append(version)
                        print(f"从日志文件中读取到版本: {version}")
        except FileNotFoundError:
            print("未找到版本日志文件，创建新的日志文件")
            # 创建一个新的日志文件
            with open(log_file, 'w') as log:
                log.write("last_down_version = 0\n")
                log.write("xk730 = kyzh0730@gmail.com\n")

    # 如没找到任何版本信息，将其设置为默认值 "0"
    if not local_versions:
        print("未找到任何本地版本，设置默认版本为 0")
        local_versions.append("0")

    return local_versions




def download_file(filename,dow_input):

    if dow_input == '1':
        print(f"正在下载: 移动端服端")

        url = mobile_download_base_url + filename

    elif dow_input == '2':
        print(f"正在下载: PC端服端")

        url = pc_download_base_url + filename
        
    else :
        print(f"无效参数({dow_input}): 默认下载 移动端 服务端")

        url = mobile_download_base_url + filename

    
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
        return True
    except requests.RequestException as e:
        print(f"下载 {filename} 时出错: {e}")
        return False


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
    print("---更新检查系统版本:1.2.7---")
    print("正在执行更新检查...")
    ensure_directory_exists(local_directory)

    # remote_versions = get_remote_versions()
    # 调用函数并获取电脑和移动端的版本
    
    pc_version, mobile_version = get_remote_versions()
    
    print(f"电脑端服务器最新版本: {pc_version}")
    
    print(f"移动端服务器最新版本: {mobile_version}")

    local_versions = get_local_versions(local_directory)


    local_versions_are_latest = (
    any(mobile_version > local_version for local_version in local_versions) or
    any(pc_version > local_version for local_version in local_versions)
)


    if local_versions_are_latest:

        print("---本地版本已是最新，无需更新---")

        return

       

    else:
        print("---发现新版本---")
    #     dow_input = input("请选择下载的服务端类型：移动端服务器请输入1, PC端服务器请输入2:")



    dow_input = input("请选择下载的服务端类型：移动端服务器请输入1, PC端服务器请输入2:")

    

    print("dow_input="+dow_input)

    #local_versions = get_local_versions(local_directory)

    if dow_input == '1':
        selected_version = mobile_version
        print("选择了移动端服务器")
    elif dow_input == '2':
        selected_version = pc_version
        print("选择了PC端服务器")
    else:
        print("无效输入，取消更新检查")
        return

    # 提取版本号
    print(f"selected_version: {selected_version}, type: {type(selected_version)}")


    selected_remote_version = selected_version.split("-")[2].replace(".zip", "")

    #print(f"selected_remote_version = {selected_remote_version}")
    
    if all(selected_remote_version > local_version for local_version in local_versions):
        
        download_successful = download_file(selected_version, dow_input)
        
        if download_successful:
            log_version(selected_remote_version)
            print("服务端安装包更新已完成")
        else:
            print("下载失败，终止更新检查系统")
    else:
        print("本地版本已是最新，无需更新")



    print("更新检查完毕")

if __name__ == "__main__":
    check_for_updates()
