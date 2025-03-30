@echo off
REM Vibe Code Scanner - Docker Wrapper Script

IF "%~1"=="" (
  echo Error: Please provide a path to the project you want to scan.
  echo Usage: docker-scan.bat "C:\path\to\your\project" [optional: -l language]
  exit /b 1
)

REM Check if Docker is installed
docker --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo Error: Docker is not installed or not in your PATH.
  echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
  exit /b 1
)

REM Check if Docker Desktop is running
docker ps > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo Error: Docker Desktop is not running.
  echo Please start Docker Desktop and try again.
  exit /b 1
)

REM Check if user is logged in to Docker
docker info > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo You need to log in to Docker Desktop first.
  echo Please open Docker Desktop, sign in with your Docker account, and try again.
  exit /b 1
)

REM Get absolute path to the project
set PROJECT_PATH=%~f1
echo Project path: %PROJECT_PATH%

REM Create reports directory if it doesn't exist
set REPORTS_PATH=%~dp0reports
if not exist "%REPORTS_PATH%" (
  echo Creating reports directory: %REPORTS_PATH%
  mkdir "%REPORTS_PATH%"
)

REM Build the Docker image
echo Building Docker image for Vibe Code Scanner...
docker build -t vibe-code-scanner . || (
  echo.
  echo Error building Docker image. This could be due to:
  echo 1. Docker Desktop is not running
  echo 2. You're not logged in to Docker Desktop
  echo 3. Network connectivity issues
  echo.
  echo Please check Docker Desktop status and try again.
  exit /b 1
)

REM Run the scanner in Docker
echo Running Vibe Code Scanner in Docker...
docker run --rm -v "%PROJECT_PATH%:/code" -v "%REPORTS_PATH%:/reports" vibe-code-scanner /code -o /reports %2 %3 %4 %5

echo Scan complete! Reports will be available in: %REPORTS_PATH%
