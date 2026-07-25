$b = 'https://joeromance84.github.io/sovereign-ladder/'

Write-Output 'Waiting for Pages rebuild...'
for ($i = 1; $i -le 15; $i++) {
    try {
        $r = Invoke-WebRequest -Uri ($b + 'print-cards.html') -UseBasicParsing -TimeoutSec 20
        if ($r.StatusCode -eq 200) { break }
    } catch { }
    Start-Sleep -Seconds 15
}

Write-Output ''
Write-Output '=== LIVE CHECK ==='
foreach ($t in @('print-cards.html', 'assets/qr-code.svg', 'CHECKSUMS.md')) {
    try {
        $r = Invoke-WebRequest -Uri ($b + $t) -UseBasicParsing -TimeoutSec 25
        Write-Output ("  [{0}] {1,-22} {2} bytes" -f $r.StatusCode, $t, $r.RawContentLength)
    } catch {
        Write-Output ("  [FAIL] " + $t)
    }
}

Write-Output ''
Write-Output '=== DEPENDENCY AUDIT ==='
$c = (Invoke-WebRequest -Uri ($b + 'print-cards.html') -UseBasicParsing -TimeoutSec 25).Content
Write-Output ("  external QR service refs : " + ($c -match 'qrserver|chart\.googleapis|api\.qrcode'))
Write-Output ("  local SVG references     : " + ([regex]::Matches($c, 'assets/qr-code\.svg')).Count)
Write-Output ("  cards on sheet           : " + ([regex]::Matches($c, 'class="card"')).Count)
Write-Output '--- VERIFY COMPLETE ---'
