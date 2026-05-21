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

Write-Host "[3/4] Building GUI version (This may take several minutes)..." -ForegroundColor Yellow
pyinstaller --clean build_gui.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[4/4] Cleaning build directory..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "Removed build directory"
}

$distFiles = Get-ChildItem -Path "dist" -Filter "*.exe"
if ($distFiles.Count -eq 0) {
    Write-Host "ERROR: No exe file found in dist directory!" -ForegroundColor Red
} else {
    Write-Host "SUCCESS: $($distFiles[0].Name) generated in dist directory!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$exeName = "店小秘做单工具.exe"
Write-Host "Executable location:" -ForegroundColor Yellow
$distFiles = Get-ChildItem -Path "dist" -Filter "*.exe"
if ($distFiles.Count -gt 0) {
    Write-Host "  - dist\$($distFiles[0].Name)" -ForegroundColor Green
} else {
    Write-Host "  - dist: NOT FOUND" -ForegroundColor Red
}

Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "1. Double-click 店小秘做单工具.exe to run"
Write-Host "2. Select or drag-drop the order file from 店小秘"
Write-Host "3. Choose output directory"
Write-Host "4. Click 开始执行"
Write-Host ""
