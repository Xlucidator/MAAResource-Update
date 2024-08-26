@REM Haven't been Checked yet

setlocal

set "skip_download=false"

set "rsrc_url=https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip"
@REM set "maa_dir=MAA-v5.5.11452-win-x64"
set "maa_dir=test"

set "maarsrc_dir=MaaResource-main"
set "zip_file=%maarsrc_dir%.zip"

if exist "%dst_dir%" (
    echo [error] Target MAA directory does not exist
    exit /b 1
)

:clean_up
echo Cleaning up
if exist "%zip_file%" (
    del /q "%zip_file%"
)
if exist "%maarsrc_dir%" (
    rmdir /s /q "%maarsrc_dir%"
)
goto :eof

:download_file
echo Downloading from %rsrc_url% ...
powershell -Command "Invoke-WebRequest -Uri %rsrc_url% -OutFile %zip_file%"
if errorlevel 1 (
    echo [error] Download failed
    exit /b 1
)
goto :eof

:unzip_file
echo Unzipping the file ...
powershell -Command "Expand-Archive -Path %zip_file% -DestinationPath ."
if errorlevel 1 (
    echo [error] Unzip failed
    call :clean_up
    exit /b 1
)
goto :eof

:process_file
echo Copying cache\ and resource\ to %maa_dir%
xcopy "%maarsrc_dir%\cache" "%maa_dir%\" /s /e /i /y
xcopy "%maarsrc_dir%\resource" "%maa_dir%\" /s /e /i /y
echo Finished.
goto :eof

:help
echo Usage: %~nx0 [-s|--skip-download] [-h|--help]
echo   -s, --skip-download    Skip downloading operation
echo   -h, --help             Show help information
exit /b 0

:parse_args
setlocal enabledelayedexpansion
:loop
if "%~1"=="" goto :done
if "%~1"=="-s" (
    set "skip_download=true"
    shift
) else if "%~1"=="--skip-download" (
    set "skip_download=true"
    shift
) else if "%~1"=="-h" (
    call :help
    exit /b 0
) else if "%~1"=="--help" (
    call :help
    exit /b 0
) else (
    echo Invalid argument: %~1
    exit /b 1
)
shift
goto :loop
:done
endlocal

call :parse_args

if "%skip_download%"=="true" (
    echo Skip Downloading zip file
) else (
    call :download_file
)

call :unzip_file
call :process_file
call :clean_up