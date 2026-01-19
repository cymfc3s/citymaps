# PowerShell script to set up and upload project to GitHub
# Run this after installing Git: powershell -ExecutionPolicy Bypass -File setup_github.ps1

Write-Host "GitHub Repository Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking for Git installation..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if ($gitCheck) {
    $gitVersion = git --version 2>&1
    Write-Host "[OK] Git is installed: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "1. Go to https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "2. Download and install Git" -ForegroundColor White
    Write-Host "3. Restart PowerShell and run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Opening Git download page..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    Start-Process "https://git-scm.com/download/win"
    exit 1
}

Write-Host ""

# Check if already a git repository
if (Test-Path .git) {
    Write-Host "Git repository already initialized." -ForegroundColor Yellow
    $continue = Read-Host "Continue with setup? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 0
    }
} else {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Adding files..." -ForegroundColor Yellow
git add .
Write-Host "[OK] Files added" -ForegroundColor Green

Write-Host ""
Write-Host "Checking for uncommitted changes..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: City map poster generator for Fusion 360"
    Write-Host "[OK] Commit created" -ForegroundColor Green
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "===========" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Don't initialize with README (we already have files)" -ForegroundColor White
Write-Host ""
Write-Host "3. Run these commands (replace YOUR_USERNAME and REPO_NAME):" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

$autoSetup = Read-Host "Do you want to set up the remote now? (y/n)"
if ($autoSetup -eq "y" -or $autoSetup -eq "Y") {
    $username = Read-Host "Enter your GitHub username"
    $repoName = Read-Host "Enter repository name (default: citymaps)"
    if ([string]::IsNullOrWhiteSpace($repoName)) {
        $repoName = "citymaps"
    }
    
    Write-Host ""
    Write-Host "Adding remote origin..." -ForegroundColor Yellow
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$username/$repoName.git"
    Write-Host "[OK] Remote added" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Setting branch to main..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "[OK] Branch set to main" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Ready to push! Run this command:" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Note: GitHub uses Personal Access Tokens, not passwords." -ForegroundColor Yellow
    Write-Host "Get one at: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host ""
    
    $pushNow = Read-Host "Push now? (y/n)"
    if ($pushNow -eq "y" -or $pushNow -eq "Y") {
        Write-Host ""
        Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
        Write-Host "(You'll be prompted for username and token)" -ForegroundColor Yellow
        git push -u origin main
    }
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
