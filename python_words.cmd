@echo off
cd /d "%~dp0python"

:MENU
cls
echo.
echo.
echo Welcome to Python Words!
echo.
echo What would you like to do?
echo.
echo 1. Create Puzzles
echo 2. Play Puzzles
echo 3. Exit
echo.
set /p SELECTION=Choose an option: 

if "%SELECTION%"=="1" (
    python "%~dp0python\puzzle_creator.py"
    goto MENU
) else if "%SELECTION%"=="2" (
    python "%~dp0python\wordfinder.py"
    goto MENU
) else if "%SELECTION%"=="3" (
    echo bye
    exit /b
) else (
    echo.
    echo Invalid response
    echo.
    goto MENU
)
