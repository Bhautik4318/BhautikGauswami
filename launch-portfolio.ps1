# Neural Pulse Net Portfolio Launcher
Write-Host "🧠 Starting Bhautik's Neural Pulse Net Portfolio..." -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location "d:\website\frontend"

# Check if npm is available
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "✅ NPM found. Starting development server..." -ForegroundColor Green
    Write-Host ""
    
    # Start the React development server
    npm start
} else {
    Write-Host "❌ NPM not found. Please install Node.js first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
