@echo off
:: Thư mục chứa virtual environment
set VENV_DIR=.venv
set PYTHON=%VENV_DIR%\Scripts\python.exe

:: Kiểm tra nếu virtual environment không tồn tại
if NOT EXIST "%PYTHON%" (
    echo Virtual environment không tồn tại. Hãy tạo bằng lệnh `python -m venv %VENV_DIR%`.
    pause
    exit /b
)

:: Tên file Python của bạn
set SCRIPT=modules\launch.py

:: Kiểm tra nếu file script không tồn tại
if NOT EXIST "%SCRIPT%" (
    echo Không tìm thấy file %SCRIPT%.
    pause
    exit /b
)

:: Chạy file Python với venv
"%PYTHON%" %SCRIPT%

pause
