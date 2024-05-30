
import os

os.system(f'conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main')  
os.system(f'conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2')
os.system(f'conda config --set show_channel_urls yes')
os.system(f'pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/')
os.system(f'pip config set install.trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/') #配置国内镜像
os.system(f'pip install scikit-learn fire regex m3u8 pyCryptodome playwright')
os.system(f'playwright install') #安装库











