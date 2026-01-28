import os
import subprocess
import zipfile
from dow import check_for_updates
import shutil
import datetime


# 本地目录和文件设置
local_directory = "./dow"
extraction_directory = "./terraria_server"
log_directory = ""
server_executable = "./terraria_server/TerrariaServer.bin.x86_64 -config serverconfig.txt -lang zh-Hans"
server_executable_permission = "./terraria_server"
extracted_version_log = os.path.join(log_directory, "version_log.txt")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")
    else:
        print(f"目录已存在: {directory}")


        

def extract_and_prepare(version):  # 更新服务端

    zip_file_path = os.path.join(local_directory, f"terraria-server-{version}.zip")
    # 构建 ZIP 文件的路径

    print(f"正在解压文件: {zip_file_path} 到 {extraction_directory}")
    # 打印解压缩操作的信息

    ensure_directory_exists(extraction_directory)
    # 确保解压缩文件的目标目录存在，如果不存在则创建

    # 备份当前服务端文件夹
    current_time = datetime.datetime.now().strftime("_old_%Y%m%d%H")
    backup_dir = extraction_directory + current_time
    ensure_directory_exists(backup_dir)

    for item in os.listdir(extraction_directory):
        # 遍历当前服务端目录中的每个项目（文件或子目录）

        s = os.path.join(extraction_directory, item)
        # 构建源路径，指向当前项目在服务端目录中的完整路径

        d = os.path.join(backup_dir, item)
        # 构建目标路径，指向备份目录中该项目的完整路径

        shutil.move(s, d)
        print(f"已将原服务端文件夹 {s} 移动到 {backup_dir}, 请前往服务端目录手动迁移您需要保留的文件(配置文件、存档等)")

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 打开指定路径的 ZIP 文件，以读取模式打开
        
        zip_ref.extractall(extraction_directory)
        # 将 ZIP 文件中的所有内容解压缩到目标目录

    extracted_version_dir = os.path.join(extraction_directory, version, "Linux")
    # 构建路径，指向解压后的特定版本目录中的 "Linux" 子目录

    # 移动 Linux 文件夹中的内容到主目录
    for item in os.listdir(extracted_version_dir):
        s = os.path.join(extracted_version_dir, item)
        d = os.path.join(extraction_directory, item)
        shutil.move(s, d)
    
    # 删除多余的文件夹
    shutil.rmtree(os.path.join(extraction_directory, version))

    # 写入解压后的版本日志
    update_version_log(extracted_version_log, version)







def update_version_log(log_file_path, version):
    # 读取现有的日志文件内容
    try:
        with open(log_file_path, 'r') as log:
            lines = log.readlines()
    except FileNotFoundError:
        lines = []

    # 查找并替换特定字段
    field_found = False
    for i, line in enumerate(lines):
        if line.startswith("version = "):
            lines[i] = f"version = {version}\n"
            field_found = True
            break

    # 如果没有找到字段，则添加新的字段
    if not field_found:
        lines.append(f"version = {version}\n")

    # 写回修改后的内容
    with open(log_file_path, 'w') as log:
        log.writelines(lines)
        print(f"记录解压后的版本号: {version}")


        
def run_server():
    print("---------------------------------------------------")
    print("         888      8888888888  .d8888b.   .d8888b.  ")
    print("         888            d88P d88P  Y88b d88P  Y88b ")
    print("         888           d88P       .d88P 888    888 ")
    print("888  888 888  888     d88P       8888'  888    888 ")
    print("`Y8bd8P' 888 .88P    8888         'Y8b. 888    888 ")
    print("  X88K   888888K    d88P     888    888 888    888 ")
    print(".d8''8b. 888 '88b  d88P      Y88b  d88P Y88b  d88P ")
    print("888  888 888  888 d88P        'Y8888P'   'Y8888P'  ")
    print("                                                   ")
    print("                                                   ")
    print("---------------------------------------------------")
    print("#####正在启动服务器#####")
    try:
        subprocess.run(server_executable, shell=True)
        print("服务器已启动")
    except Exception as e:
        print(f"启动服务器时出错: {e}")



def set_executable_permission(directory):
    print(f"设置目录下所有文件的执行权限: {directory}")
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # 赋予文件所有者执行权限
                os.chmod(file_path, 0o755)
                print(f"权限设置成功: {file_path}")
    except Exception as e:
        print(f"设置权限时出错: {e}")


def main():

    print("""

           0                              
            0        0    0               
            0         0  0 0   0          
            0        0 0  0    0          
             0       0   0 0  0 0         
            0 0 0 0 0   0  0   0      0   
          0 0    0   0      0 0 0   0     
              0 0 0 0 0 00 0  0    0 00   
           0 0 0000 0 00  0 0  0          
          0  000 000 00000  0 0  0 0      
        0 00 0 0000000000 00000 0  0      
       0 0 0 0000 00 00000 00000 0        
     0  00 00000000 000 0 0000000 0       
      0 0 000000000000 0000 00000         
     0  00 00 00000 00000 000 00 00       
    0  0 000000000 000000000 000000       
     0  00 0 000 00 0 0000000000 0 0      
     0 0 0000000000 0000000000 0000       
      0    0 0 0000000000000 0000         
       00 0 000 0000 00000 0000000        
         0         0000000000000          
           0  0  0   0 000000 0           
             0      0   0 0                
              0      0                    
               0  0                        

""")




    print(f"---terraria服务端启动程序---")
    print(f"版本:1.2.4")
    print(f"作者:xk730_kyzh0730@gmail.com")
    # 询问是否执行


    print("开始执行更新同步检查...")
    
    check_for_updates()  # 调用 dow.py 中的更新同步检查函数

    # 初始化最新版本号为 None
    latest_version = None

    try:
        # 尝试打开版本日志文件 "version_log.txt" 以读取最新版本号
        with open("version_log.txt", 'r') as log:
            for line in log:
                # 查找以 "last_down_version = " 开头的行
                if line.startswith("last_down_version = "):
                    # 提取版本号并去除两端的空格
                    
                    latest_version = line.split("=")[1].strip()
                    print(f"最新版本号: {latest_version}")
                    break  # 找到后立即退出循环
    except FileNotFoundError:
        # 如果文件未找到，打印错误信息并返回
        print("未找到版本日志文件，无法检查更新")
        return

    # 初始化解压后的版本号为 None
    extracted_version = None

    # 检查解压后的版本日志文件是否存在以确定是否需要更新
    if os.path.exists(extracted_version_log):
        # 打开解压后的版本日志文件以读取已解压的版本号
        with open(extracted_version_log, 'r') as log:
            for line in log:
                
                # 查找以 " " 开头的行
                
                if line.startswith("version = "):
                    
                    # 提取已解压的版本号并去除两端的空格
                    
                    extracted_version = line.split("=")[1].strip()
                    
                    break  # 找到后立即退出循环


    if latest_version != extracted_version:
        print("发现新版本("+latest_version+")，准备解压和运行...")
        user_input = input("建议您在继续更新前手动备份存档，是否继续执行更新？输入 'y' 继续，输入 'n' 则不执行更新，直接启动服务端: ").strip().lower()
        if user_input != 'y':
            print("---更新计划已经取消---")

        elif user_input == 'y':
            
            print("---开始更新---...")
            
            extract_and_prepare(latest_version)
    else:
        print("服务包最新版本为：("+latest_version+")，服务端当前版本为：("+extracted_version+")")
        print("已是最新版本，即将启动服务器...")

        # 设置执行权限
    set_executable_permission(server_executable_permission)

        
    run_server()

if __name__ == "__main__":
    main()
