# Installing Python and pip on Windows

## Quick Installation Guide

### Method 1: Download from Python.org (Recommended)

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.x.x" button
   - This downloads the installer for the latest Python version

2. **Run the Installer:**
   - Double-click the downloaded `.exe` file
   - **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
   - Click "Install Now" (or "Customize installation" for more options)
   - Wait for installation to complete

3. **Verify Installation:**
   - Open PowerShell (press Windows key + X, then select Windows PowerShell)
   - Run:
     ```powershell
     python --version
     pip --version
     ```
   - You should see version numbers for both

### Method 2: Using Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.12" (or latest version)
3. Click "Get" or "Install"
4. Wait for installation

### Method 3: Using winget (Windows Package Manager)

If you have winget installed (Windows 11 or Windows 10 with App Installer):

```powershell
winget install Python.Python.3.12
```

### After Installation

Once Python is installed, pip will be available automatically. Verify with:

```powershell
pip --version
```

### Install Project Dependencies

After Python and pip are installed, navigate to this project folder and run:

```powershell
cd c:\Users\srw\citymaps
pip install -r requirements.txt
```

## Troubleshooting

### "Python is not recognized"

If `python` command doesn't work after installation:

1. **Check if Python is installed:**
   - Search for "Python" in Start menu
   - If it appears, Python is installed but not in PATH

2. **Add Python to PATH manually:**
   - Find where Python is installed (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\` or `C:\Python3xx\`)
   - Add both these paths to System Environment Variables:
     - `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`
     - `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\Scripts\`
   - See detailed instructions: https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/

3. **Restart PowerShell** after modifying PATH

### "pip is not recognized"

- Pip comes with Python, so if Python works, pip should too
- Try using `python -m pip` instead:
  ```powershell
  python -m pip --version
  python -m pip install -r requirements.txt
  ```

### Permission Errors

If you get permission errors, try:

```powershell
python -m pip install --user -r requirements.txt
```

Or run PowerShell as Administrator.

## Quick Test

After installation, test everything works:

```powershell
python --version
pip --version
pip install requests
python -c "import requests; print('Success!')"
```

If all commands work, you're ready to use the map generator!
