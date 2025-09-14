# Image verification script
$imagePath = "e:\New folder (4)\static\images\bhautik.jpg"

Write-Host "=== Profile Image Verification ===" -ForegroundColor Green

# Check if file exists
if (Test-Path $imagePath) {
    $file = Get-Item $imagePath
    Write-Host "File exists: $($file.Name)" -ForegroundColor Green
    Write-Host "Size: $($file.Length) bytes" -ForegroundColor Yellow
    
    if ($file.Length -gt 50000) {
        Write-Host "File size looks good" -ForegroundColor Green
    } else {
        Write-Host "File is too small - might be corrupted" -ForegroundColor Red
    }
} else {
    Write-Host "File does not exist" -ForegroundColor Red
}

Write-Host "Next: Replace with your professional photo" -ForegroundColor Yellow