# Build Script for GUI Version

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "makeOrders GUI Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python --version | Out-Null
} catch {
    Write-Host "Error: Python not found. Please install Python 3.11+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/4] Cleaning old build files..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "Removed build directory"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "Removed dist directory"
}
$rootExePattern = "做单工具.exe"
if (Test-Path $rootExePattern) {
    Remove-Item -Force $rootExePattern
    Write-Host "Removed old exe from root"
}

Write-Host "[3/4] Building GUI version (This may take several minutes)..." -ForegroundColor Yellow
pyinstaller --clean build_gui.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[4/4] Copying to root directory..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "Removed build directory"
}

Write-Host "Looking for exe file in dist directory..."
$distFiles = Get-ChildItem -Path "dist" -Filter "*.exe"
if ($distFiles.Count -eq 0) {
    Write-Host "ERROR: No exe file found in dist directory!" -ForegroundColor Red
} else {
    $distExe = $distFiles[0].FullName
    $exeName = $distFiles[0].Name
    Write-Host "Found: $exeName"

    $rootExePath = Join-Path -Path (Get-Location) -ChildPath $exeName
    Write-Host "Copying to root: $exeName"
    Copy-Item -Path $distExe -Destination $rootExePath -Force

    if (Test-Path $rootExePath) {
        Write-Host "SUCCESS: $exeName copied to root directory!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to copy $exeName to root directory!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootExePattern = "做单工具.exe"
Write-Host "Executable locations:" -ForegroundColor Yellow
if (Test-Path $rootExePattern) {
    Write-Host "  - Root: $rootExePattern" -ForegroundColor Green
} else {
    Write-Host "  - Root: NOT FOUND" -ForegroundColor Red
}
if (Test-Path "dist\$rootExePattern") {
    Write-Host "  - dist: dist\$rootExePattern" -ForegroundColor Green
} else {
    Write-Host "  - dist: NOT FOUND" -ForegroundColor Red
}

Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "1. Double-click 做单工具.exe to run"
Write-Host "2. Select or drag-drop the order file from 店小秘"
Write-Host "3. Choose output directory"
Write-Host "4. Click 开始执行"
Write-Host ""
