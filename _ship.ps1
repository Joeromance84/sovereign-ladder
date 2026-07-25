$repo = 'C:\Users\logan\sovereign-ladder'
Set-Location $repo

Write-Output '=== STRUCTURE CHECK ==='
python -X utf8 "$repo\tools\check_html.py"

Write-Output ''
Write-Output '=== COMMIT + PUSH ==='
python -X utf8 "$repo\tools\make_checksums.py" | Select-Object -Last 1
git add -A
git -c core.pager=cat commit -q -m "Add 'How to use this' section: scope, disclosure guidance, AI privacy reality, activation handling, R8 boundary" 2>&1 | Select-Object -First 2
git push 2>&1 | Select-Object -Last 1
Write-Output ('HEAD: ' + (git rev-parse --short HEAD))
