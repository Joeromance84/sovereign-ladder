$b = 'https://joeromance84.github.io/sovereign-ladder/'

Write-Output 'Waiting for Pages rebuild...'
for ($i = 1; $i -le 20; $i++) {
    try {
        $c = (Invoke-WebRequest -Uri $b -UseBasicParsing -TimeoutSec 20).Content
        if ($c -match 'id="start"') { break }
    } catch { }
    Start-Sleep -Seconds 15
}

$c = (Invoke-WebRequest -Uri $b -UseBasicParsing -TimeoutSec 25).Content
Write-Output ''
Write-Output '=== LIVE ==='
Write-Output ("  selector present : " + ($c -match 'id="start"'))
Write-Output ("  six states       : " + ([regex]::Matches($c, '<div class="state">')).Count)
Write-Output ("  six actions      : " + ([regex]::Matches($c, '<div class="do">')).Count)
Write-Output ("  seam row         : " + ($c -match 'calm day, not a hard moment'))
Write-Output ("  hero -> #start   : " + ($c -match 'href="#start"'))
Write-Output ("  988 still present: " + ($c -match '988'))
Write-Output ("  page size        : " + $c.Length + " bytes")
Write-Output '--- COMPLETE ---'
