# Requires elevated PowerShell
Write-Host "Installing dependencies via Chocolatey/Winget (where available)..."

# Install Chocolatey if missing
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
  Set-ExecutionPolicy Bypass -Scope Process -Force
  [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
  Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

choco install -y git python wireshark
Write-Host "For SDR drivers (RTL-SDR/HackRF), install respective Windows drivers and tools manually."
Write-Host "Python usage:"
Write-Host "  py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip -r requirements.txt; pip install -e ."
