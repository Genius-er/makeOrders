REM 检查是否已经安装了Python3
python --version >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    REM 如果已经安装了Python3，则直接运行脚本
    py -3 ./src/main.py
) ELSE (
    REM 如果没有安装Python3，则下载最新版的Python3安装包
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe', 'python-3.9.7-amd64.exe')"
    REM 安装Python3
    python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    REM 下载openpyxl和pillow
    py -3 -m pip install openpyxl pillow
    REM 运行脚本
    py -3 ./src/main.py
)
pause