@echo off
setlocal

if exist ".env" (
    echo .env file found. Launching applications...

   
    for /f "tokens=1,* delims==" %%A in (.env) do (
        if "%%A"=="TRIGNO_PATH" set TRIGNO_PATH=%%B
    )
    echo %TRIGNO_PATH%
    if not exist "%TRIGNO_PATH%" (
        echo Executable file not found at: %TRIGNO_PATH%
        pause
        exit /b
    )
    start "Trigno" "%TRIGNO_PATH%"

    start "" python application_code.py
) else (
    echo .env file not found! Applications will not be launched.
    pause
)

endlocal