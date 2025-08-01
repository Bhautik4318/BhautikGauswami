@echo off
echo Starting Neural Pulse Portfolio on port 3001...
cd /d "%~dp0\frontend"
set PORT=3001
npm start
pause
