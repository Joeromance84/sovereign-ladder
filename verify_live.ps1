$gh = 'C:\Program Files\GitHub CLI\gh.exe'
$r  = 'Joeromance84/sovereign-ladder'

Write-Output '=== BEFORE ==='
$b = & $gh api "repos/$r" | ConvertFrom-Json
Write-Output ("  topics : " + ($b.topics -join ', '))

Write-Output ''
Write-Output '=== SWAP: remove cbt, add psychology ==='
& $gh repo edit $r --remove-topic cbt --add-topic psychology 2>&1 | Out-String | Write-Output
Write-Output ("  exit code: " + $LASTEXITCODE)

Write-Output ''
Write-Output '=== AFTER ==='
Start-Sleep -Seconds 3
$a = & $gh api "repos/$r" | ConvertFrom-Json
Write-Output ("  topics : " + ($a.topics -join ', '))
Write-Output ("  count  : " + $a.topics.Count)
Write-Output ("  cbt removed  : " + (-not ($a.topics -contains 'cbt')))
Write-Output ("  psychology in: " + ($a.topics -contains 'psychology'))
Write-Output ("  homepage kept: " + $a.homepage)
Write-Output '--- COMPLETE ---'
