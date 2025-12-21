import os
import subprocess
import zipfile
from dow import check_for_updates
import shutil

# 本地目录和文件设置
local_directory = "./dow"
extraction_directory = "./terraria_server"
server_executable = "./terraria_server/TerrariaServer.bin.x86_64 -config serverconfig.txt -lang zh-Hans"
server_executable_permission = "./terraria_server"
extracted_version_log = os.path.join(extraction_directory, "version_log.txt")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")
    else:
        print(f"目录已存在: {directory}")

def extract_and_prepare(version):
    zip_file_path = os.path.join(local_directory, f"terraria-server-{version}.zip")
    print(f"解压文件: {zip_file_path} 到 {extraction_directory}")

    ensure_directory_exists(extraction_directory)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_directory)

    extracted_version_dir = os.path.join(extraction_directory, version, "Linux")
    
    for item in os.listdir(extracted_version_dir):
        s = os.path.join(extracted_version_dir, item)
        d = os.path.join(extraction_directory, item)
        os.rename(s, d)
    
    # 写入解压后的版本日志
    with open(extracted_version_log, 'w') as log:
        log.write(f"version = {version}\n")
        print(f"记录解压后的版本号: {version}")
    
    # 删除多余的文件夹
    shutil.rmtree(os.path.join(extraction_directory, version))

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
    print(f"版本:1.1.0")
    print(f"作者:xk730_kyzh0730@gmail.com")
    print("开始执行更新检查...")
    
    check_for_updates()  # 调用 dow.py 中的更新检查函数

    latest_version = None
    try:
        with open("version_log.txt", 'r') as log:
            for line in log:
                if line.startswith("version = "):
                    latest_version = line.split("=")[1].strip()
                    print(f"最新版本号: {latest_version}")
                    break
    except FileNotFoundError:
        print("未找到版本日志文件，无法检查更新")
        return

    # 检查解压后的版本日志以确定是否需要更新
    extracted_version = None
    if os.path.exists(extracted_version_log):
        with open(extracted_version_log, 'r') as log:
            for line in log:
                if line.startswith("version = "):
                    extracted_version = line.split("=")[1].strip()
                    break

    if latest_version != extracted_version:
        print("发现新版本，准备解压和运行服务器...")
        extract_and_prepare(latest_version)
    else:
        print("已是最新版本，即将启动服务器...")

        # 设置执行权限
    set_executable_permission(server_executable_permission)

        

    run_server()

if __name__ == "__main__":
    main()
