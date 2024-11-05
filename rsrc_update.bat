@echo off
setlocal

set "skip_download=false"

set "rsrc_url=https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip"
set "maa_dir=MAA-v5.5.11452-win-x64"
set "maarsrc_dir=MaaResource-main"
set "zip_file=%maarsrc_dir%.zip"

@REM React to Ctrl+C interrupt, but seems useless
@REM for /f "tokens=2 delims==" %%i in ('"exit /b 0"') do set "trap=call :%trap_handler%" > nul 2>&1

if not exist "%maa_dir%" (
    echo [error] Target MAA directory does not exist
    exit /b 1
)

for %%i in (%*) do (
    if "%%i"=="-s" (
        set "skip_download=true"
    ) else if "%%i"=="-h" (
        echo Usage: %0 [-s|--skip-download] [-h|--help]
        echo   -s, --skip-download    Skip the download operation
        echo   -h, --help             Display help information
        exit /b 0
    ) else (
        echo Invalid argument: %%i
        exit /b 1
    )
)

if "%skip_download%"=="true" (
    echo Skipping download of zip file
) else (
    call :download_file
)
call :unzip_file
call :process_file
call :clean_up
exit /b 0

@REM /* Definition of Functions */

:clean_up
echo Cleaning up
if exist "%zip_file%" (
    del /f "%zip_file%"
)
if exist "%maarsrc_dir%" (
    rmdir /s /q "%maarsrc_dir%"
)
goto :eof

:download_file
echo Downloading from %rsrc_url% ...
powershell -Command "Invoke-WebRequest -Uri '%rsrc_url%' -OutFile '%zip_file%'"
if %ERRORLEVEL% neq 0 (
    echo [error] Download failed
    exit /b 1
)
goto :eof

:unzip_file
echo Unzipping the file ...
powershell -Command "Expand-Archive -Path '%zip_file%' -DestinationPath ."
if %ERRORLEVEL% neq 0 (
    echo [error] Unzip failed
    call :clean_up
    exit /b 1
)
goto :eof

:process_file
echo Copying cache/ and resource/ to %maa_dir%
xcopy /s /e /y "%maarsrc_dir%\cache" "%maa_dir%\cache\"
xcopy /s /e /y "%maarsrc_dir%\resource" "%maa_dir%\resource\"
echo Finished.
goto :eof

:trap_handler
call :clean_up
exit /b 1

