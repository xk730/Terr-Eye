#运行此部分您需要：  
1，确保python已安装  
2，确保必要的库已安装  
3，确保您的设备可以连接泰拉瑞亚官方网站  
#To run this section, you need:  
1. Ensure that Python is installed  
2. Ensure that the necessary libraries have been installed  
3. Ensure that your device can connect to the official Terraria website  

#该部分的使用方法是：  
运行start.py(也许是py start.py，也有可能是python start.py 或是别的什么,这决定于你设备上python的安装设置)  
Run start.py (it may be py start.py or python start.py or ...?, depending on the installation settings of Python on your device)  

#该部分的运作机制是：  
start.py调用dow.py进行版本自检，如版本为最新则直接启动服务器(服务器在\terraria_server),如dow.py检测到新版本则会下载安装包，后start.py会进行解压更新处理并启动服务器  
