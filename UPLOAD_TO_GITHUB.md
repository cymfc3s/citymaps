# Quick Guide: Upload to GitHub

## Prerequisites

Git must be installed. If not installed:
1. Go to https://git-scm.com/download/win
2. Download and install Git (check "Add Git to PATH")
3. Restart PowerShell

## Quick Upload Steps

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `citymaps` (or your choice)
3. Description: "Generate city map posters as SVG for Fusion 360 and 3D printing"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README
6. Click **Create repository**

### Step 2: Run Setup Script

```powershell
powershell -ExecutionPolicy Bypass -File setup_github.ps1
```

Follow the prompts to:
- Initialize git repository
- Add all files
- Create commit
- Set up remote (enter your GitHub username and repo name)
- Push to GitHub

### Step 3: Authentication

GitHub requires a **Personal Access Token** (not password):

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it: "citymaps upload"
4. Select scope: **repo** (full control)
5. Click **Generate token**
6. **Copy the token** immediately (you won't see it again!)

When pushing:
- Username: Your GitHub username
- Password: Paste the token you just created

## Manual Commands (Alternative)

If you prefer manual setup:

```powershell
# Initialize repository
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: City map poster generator for Fusion 360"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Set branch to main
git branch -M main

# Push to GitHub (use your token as password)
git push -u origin main
```

## Troubleshooting

**Error: "git is not recognized"**
→ Install Git from https://git-scm.com/download/win

**Error: "Authentication failed"**
→ Use Personal Access Token instead of password
→ Get token from https://github.com/settings/tokens

**Error: "remote origin already exists"**
→ Run: `git remote remove origin` then add it again

**Files not uploading**
→ Make sure files are not ignored in `.gitignore`
→ Check: `git status` to see what's tracked

---

**Need help?** See `GITHUB_SETUP.md` for detailed instructions.
