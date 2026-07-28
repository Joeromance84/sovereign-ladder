Set-Location 'C:\Users\logan\sovereign-ladder'
Write-Output '### TEST 1 - vague opener, safety QUESTION instead of INFORMATION'
Write-Output '### this is the failure the other thread found; harness must catch it'
python -X utf8 tools\psp1_audit.py tools\samples\transcript_vague_opener.txt
$e1 = $LASTEXITCODE
Write-Output ''
Write-Output '### TEST 2 - known-bad urge transcript, regression check'
python -X utf8 tools\psp1_audit.py tools\samples\transcript_urge.txt | Select-Object -Last 12
Write-Output ''
Write-Output ('TEST 1 exit code: ' + $e1 + '   (1 = violations found, correct)')
