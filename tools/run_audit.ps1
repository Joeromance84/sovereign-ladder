Set-Location 'C:\Users\logan\sovereign-ladder'
python -X utf8 tools\psp1_audit.py tools\samples\transcript_urge.txt
Write-Output ""
Write-Output ("EXIT CODE: " + $LASTEXITCODE + "   (0 = clean, 1 = violations found)")
