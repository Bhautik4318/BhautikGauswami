# Image verification script
$imagePath = "e:\New folder (4)\static\images\bhautik.jpg"

Write-Host "=== Profile Image Verification ===" -ForegroundColor Green

# Check if file exists
if (Test-Path $imagePath) {
    $file = Get-Item $imagePath
    Write-Host "✅ File exists: $($file.Name)" -ForegroundColor Green
    Write-Host "📁 Size: $($file.Length) bytes" -ForegroundColor Yellow
    
    if ($file.Length -gt 50000) {
        Write-Host "✅ File size looks good (>50KB)" -ForegroundColor Green
    } else {
        Write-Host "❌ File is too small - might be corrupted" -ForegroundColor Red
    }
    
    # Check file header
    $bytes = [System.IO.File]::ReadAllBytes($imagePath)[0..3]
    $header = ($bytes | ForEach-Object { '{0:X2}' -f $_ }) -join ''
    
    if ($header.StartsWith('FFD8')) {
        Write-Host "✅ Valid JPEG file header" -ForegroundColor Green
    } else {
        Write-Host "❌ Invalid JPEG header: $header" -ForegroundColor Red
    }
    
} else {
    Write-Host "❌ File does not exist at: $imagePath" -ForegroundColor Red
    Write-Host "Please save your professional photo as 'bhautik.jpg' in the static/images folder" -ForegroundColor Yellow
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Green
Write-Host "1. If file is invalid, replace with your professional photo"
Write-Host "2. Run: collectstatic command"
Write-Host "3. Refresh browser"
Write-Host "4. Check: http://127.0.0.1:8000/static/images/bhautik.jpg"