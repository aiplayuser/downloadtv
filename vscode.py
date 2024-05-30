
import os

os.system(f'conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main')  
os.system(f'conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2')
os.system(f'conda config --set show_channel_urls yes')
os.system(f'pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/')
os.system(f'pip config set install.trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/') #配置国内镜像
os.system(f'pip install matplotlib pandas tushare you-get scikit-learn fire regex m3u8 pyCryptodome playwright')
os.system(f'playwright install') #安装库


# esp开发板网址
# http://arduino.esp8266.com/stable/package_esp8266com_index.json
# https://ai.bemfa.com/esp8266/stable/package_esp8266com_index.json
# https://ai.bemfa.com/esp32/stable/package_esp32_index.json
# http://192.168.31.106/package_esp32_index.json
# http://192.168.31.106/package_esp8266com_index.json
# 系统复位后出现乱码，分两种情况： 冷启动或硬件复位。
# 初次上电或硬件复位时，系统一定会输出乱码，除非您使用 74880 波特率的固件。这是因为系统上电
# 时，会运行厂商芯片内部的 Boot loader.然而 Boot loader 因为某些原因会将整个 SoC 的波特率初始
# 化成 74880.您的串口软件很有可能不在这个波特率上，因此会出现乱码。
# 如果您想知道这些乱码的含义，请设置成 74880 波特率。

# https://code.visualstudio.com/  //安装vscode
# https://developer.nvidia.com/cuda-toolkit-archive  //安装cuda11.7
# https://developer.nvidia.com/rdp/cudnn-archive  //安装cudnn
# https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe    //安装python
# https://git-scm.com/downloads     // 安装git，添加到系统终端，添加到vscode
# https://docs.microsoft.com/zh-CN/cpp/windows/latest-supported-vc-redist?view=msvc-170   //安装visual c++ 
# https://download.visualstudio.microsoft.com/download/pr/85473c45-8d91-48cb-ab41-86ec7abc1000/83cd0c82f0cde9a566bae4245ea5a65b/windowsdesktop-runtime-6.0.16-win-x64.exe  //启动器依赖库
# https://code.visualstudio.com/   //安装vscode配置vscode command prompt为默认终端 

# git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git  //安装sd-webuui
# https://pytorch.org/ # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
# import torch  //torch.version.cuda  //torch.cuda.is_available()  //torch.backends.cudnn.version()  //torch.backends.cudnn.is_available() 

# https://docs.conda.io/en/latest/miniconda.html  //安装miniconda3  //conda search cudatoolkit  //conda search cudnn  //conda install cudatoolkit  //conda install cudnn
# python -m pip install --upgread pip #升级pip  //python -V  //pip -V  //nvcc -V  //nvidia-smi
# C:\Users\texiao\AppData\Roaming\pip\pip.ini # 配置pip国内源 # trusted-host 解决地址不受信任问题
# pip install tensorflow-gpu==2.10 # 2.10以后不再支持gpu

# Hex Editor 二进制文件查看
# platformio ide  单片机代码编辑
# xml format 网页代码格式化
# Sourcery 代码优化提示
# tabnine ai autocomplete ai自动补代码
# Comment Translate：★★★★★ 完美的英文注释查看助手，选中即可自动翻译
# Codelf：★★★★★ 通过搜索GitHub, Bitbucket, GitLab来找到真实的使用变量名，为你提供一些高频使用的词汇
# Partial Diff：文本比较
# 代码搜索：Sourcegraph
# 免费 ChatGPT4 编程 AI 助手：Bito,TalkX,chatgpt中文版








