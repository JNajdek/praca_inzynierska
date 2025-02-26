@echo off
setlocal

    echo "C:\Program Files (x86)\Delsys, Inc\Trigno SDK\SensorBaseControl.exe"
    if not exist "C:\Program Files (x86)\Delsys, Inc\Trigno SDK\SensorBaseControl.exe" (
        echo Executable file not found at: "C:\Program Files (x86)\Delsys, Inc\Trigno SDK\SensorBaseControl.exe"
        pause
        exit /b
    )
    start "Trigno" "C:\Program Files (x86)\Delsys, Inc\Trigno SDK\SensorBaseControl.exe"

    start "" python application_code.py
endlocal