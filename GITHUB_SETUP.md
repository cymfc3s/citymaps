# Uploading to GitHub - Step by Step Guide

## Step 1: Install Git

Git is not currently installed on your system. Here's how to install it:

### Option 1: Download from Git Website (Recommended)

1. Go to https://git-scm.com/download/win
2. Download the installer for Windows
3. Run the installer
4. Use default settings (check "Add Git to PATH")
5. Complete the installation

### Option 2: Using winget (if available)

```powershell
winget install Git.Git
```

### Option 3: Using Chocolatey (if installed)

```powershell
choco install git
```

## Step 2: Verify Git Installation

After installation, restart PowerShell and run:

```powershell
git --version
```

You should see something like: `git version 2.x.x`

## Step 3: Configure Git (First Time Only)

Set your name and email (replace with your info):

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `citymaps` (or your preferred name)
3. Description: "Generate beautiful city map posters as SVG for Fusion 360 and 3D printing"
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click **Create repository**

## Step 5: Upload to GitHub

After Git is installed, run the setup script:

```powershell
powershell -ExecutionPolicy Bypass -File setup_github.ps1
```

Or manually follow these commands:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: City map poster generator for Fusion 360"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/citymaps.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Troubleshooting

### Authentication Issues

GitHub no longer accepts passwords. You'll need a **Personal Access Token**:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it (e.g., "citymaps upload")
4. Select scope: **repo** (full control)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

When pushing, use your token as the password:
- Username: Your GitHub username
- Password: The token you just created

### Alternative: Use GitHub Desktop

If command line is confusing, use GitHub Desktop:

1. Download from https://desktop.github.com/
2. Sign in to GitHub
3. File → Add Local Repository
4. Select your `citymaps` folder
5. Commit and push using the UI

---

**Ready?** Install Git first, then we can set up the repository!
