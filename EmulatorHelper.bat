@rem
@echo off

set "_root=%~dp0"
set "_root=%_root:~0,-1%"
cd "%_root%"
echo "%_root%

color F0

set "_pyBin=%_root%\toolkit"
set "_adbBin=%_root%\toolkit\Lib\site-packages\adbutils\binaries"
set "PATH=%_root%\toolkit\alias;%_root%\toolkit\command;%_pyBin%;%_pyBin%\Scripts;%_adbBin%;%PATH%"

title EmulatorHelper Updater
python -m deploy.installer
if %errorlevel% neq 0 (
    pause >nul
) else (
    start "EmulatorHelper" "%_root%\toolkit\webapp\EmulatorHelper.exe"
)
