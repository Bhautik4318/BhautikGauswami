# Neural Pulse Portfolio Launcher
Write-Host "Starting Neural Pulse Portfolio on port 3001..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot\frontend"
$env:PORT = "3001"
npm start
