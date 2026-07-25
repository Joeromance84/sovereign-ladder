$b = 'https://joeromance84.github.io/sovereign-ladder/'

Write-Output 'Waiting for Pages rebuild...'
for ($i = 1; $i -le 20; $i++) {
    try {
        $c = (Invoke-WebRequest -Uri $b -UseBasicParsing -TimeoutSec 20).Content
        if ($c -match 'id="how"') { break }
    } catch { }
    Start-Sleep -Seconds 15
}

$c = (Invoke-WebRequest -Uri $b -UseBasicParsing -TimeoutSec 25).Content
Write-Output ''
Write-Output '=== LIVE CONTENT CHECK ==='
Write-Output ("  how-to-use section    : " + ($c -match 'id="how"'))
Write-Output ("  AI storage warning    : " + ($c -match "company's servers"))
Write-Output ("  disclosure guidance   : " + ($c -match 'never have to narrate your life'))
Write-Output ("  R8 boundary           : " + ($c -match 'stand in for human connection'))
Write-Output ("  Rung 0 when activated : " + ($c -match 'ground you, not analyze you'))
Write-Output ("  crisis line 988       : " + ($c -match '988'))
Write-Output ("  no false 'no data'    : " + (-not ($c -match 'No data stored')))
Write-Output ("  page size             : " + $c.Length + " bytes")
Write-Output '--- LIVE VERIFY COMPLETE ---'
