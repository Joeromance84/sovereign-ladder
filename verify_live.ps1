$base = 'https://joeromance84.github.io/sovereign-ladder/'
$targets = @('', 'terms.html', 'CHECKSUMS.md')

Write-Output 'Waiting for Pages rebuild...'
for ($i = 1; $i -le 20; $i++) {
    try {
        $r = Invoke-WebRequest -Uri ($base + 'terms.html') -UseBasicParsing -TimeoutSec 20
        if ($r.StatusCode -eq 200) { break }
    } catch { }
    Start-Sleep -Seconds 15
    Write-Output ("  attempt $i - not live yet")
}

Write-Output ''
Write-Output '=== LIVE CHECK ==='
foreach ($t in $targets) {
    try {
        $r = Invoke-WebRequest -Uri ($base + $t) -UseBasicParsing -TimeoutSec 25
        $label = if ($t -eq '') { '(landing page)' } else { $t }
        Write-Output ("  [{0}] {1,-20} {2} bytes" -f $r.StatusCode, $label, $r.RawContentLength)
    } catch {
        Write-Output ("  [FAIL] " + $t + " -> " + $_.Exception.Message)
    }
}

Write-Output ''
Write-Output '=== CONTENT SPOT CHECK ==='
$terms = (Invoke-WebRequest -Uri ($base + 'terms.html') -UseBasicParsing -TimeoutSec 25).Content
$index = (Invoke-WebRequest -Uri $base -UseBasicParsing -TimeoutSec 25).Content
Write-Output ("  terms: misuse section     : " + ($terms -match 'being used against you'))
Write-Output ("  terms: crisis line 988    : " + ($terms -match '988'))
Write-Output ("  terms: no-warranty clause : " + ($terms -match 'No warranty'))
Write-Output ("  index: links to terms     : " + ($index -match 'terms\.html'))
Write-Output '--- VERIFY COMPLETE ---'
