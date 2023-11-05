@echo off
chcp 65001

set "pythonVersion=3.11"

REM 检查注册表中是否存在 Python 3.11 版本的安装路径
for /f "tokens=2*" %%A in ('reg query "HKLM\Software\Python\PythonCore\3.11\InstallPath" /ve 2^>nul') do (
    set "pythonPath=%%B"
)
for /f "tokens=2*" %%A in ('reg query "HKCU\Software\Python\PythonCore\3.11\InstallPath" /ve 2^>nul') do (
    set "pythonPath=%%B"
)

set "downloadVersion=3.11.6"
if not defined pythonPath (
    echo Python %pythonVersion% 未在计算机上找到。
    rem 下载 Python 安装包
    bitsadmin /transfer PythonInstaller https://www.python.org/ftp/python/%downloadVersion%/python-%downloadVersion%-amd64.exe %temp%\python-%downloadVersion%-amd64.exe
    
    rem 静默安装 Python
    %temp%\python-%downloadVersion%-amd64.exe /quiet InstallAllUsers=1 PrependPath=0
    
    rem 删除安装包
    del %temp%\python-%downloadVersion%-amd64.exe
    echo 安装python%downloadVersion%完成
) else (
    echo Python %pythonVesion% 已安装在 %pythonPath%
)

rem 安装依赖
py -3.11 -m pip install -r requirements.txt


rem 运行正式工具脚本
py -3.11 .\src\main.py
