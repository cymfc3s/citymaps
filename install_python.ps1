# PowerShell script to help install Python on Windows
# Run this script: Right-click and "Run with PowerShell" or run: powershell -ExecutionPolicy Bypass -File install_python.ps1

Write-Host "Python Installation Helper for Windows" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is already installed
Write-Host "Checking for existing Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is already installed: $pythonVersion" -ForegroundColor Green
    
    try {
        $pipVersion = pip --version 2>&1
        Write-Host "✓ pip is available: $pipVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "Python and pip are ready to use!" -ForegroundColor Green
        Write-Host "Next step: Run 'pip install -r requirements.txt'" -ForegroundColor Cyan
        exit 0
    } catch {
        Write-Host "✗ pip not found. Python may not be fully installed." -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Python is not installed." -ForegroundColor Red
}

Write-Host ""
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host "1. Download from python.org (Recommended)"
Write-Host "2. Install via Microsoft Store"
Write-Host "3. Install via winget (if available)"
Write-Host ""

$choice = Read-Host "Enter your choice (1-3) or 'q' to quit"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Opening Python download page..." -ForegroundColor Yellow
        Write-Host "IMPORTANT: When installing, check 'Add Python to PATH'" -ForegroundColor Red
        Start-Process "https://www.python.org/downloads/"
    }
    "2" {
        Write-Host ""
        Write-Host "Opening Microsoft Store..." -ForegroundColor Yellow
        Start-Process "ms-windows-store://pdp/?ProductId=9NRWMJP3717K"
    }
    "3" {
        Write-Host ""
        Write-Host "Attempting to install via winget..." -ForegroundColor Yellow
        try {
            winget install Python.Python.3.12
            Write-Host "Installation started. Please wait for it to complete." -ForegroundColor Green
        } catch {
            Write-Host "✗ winget not available. Please use option 1 or 2." -ForegroundColor Red
        }
    }
    "q" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "After installation, restart PowerShell and run:" -ForegroundColor Cyan
Write-Host "  python --version" -ForegroundColor White
Write-Host "  pip --version" -ForegroundColor White
Write-Host "  pip install -r requirements.txt" -ForegroundColor White
