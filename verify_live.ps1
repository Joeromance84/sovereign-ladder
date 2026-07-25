$base = 'https://joeromance84.github.io/sovereign-ladder/'
$paths = @(
  '',
  'assets/three-pillars-ai-primer.md',
  'assets/psp-1-protocol-spec.md',
  'assets/sovereign-ladder-protocol-v4.pdf',
  'assets/master-geometry-of-addiction-sovereignty.pdf',
  'assets/qr-code.png'
)

Write-Output 'Waiting for first Pages build...'
$ready = $false
for ($i = 1; $i -le 20; $i++) {
    try {
        $r = Invoke-WebRequest -Uri $base -UseBasicParsing -TimeoutSec 20
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
    Start-Sleep -Seconds 15
    Write-Output ("  attempt $i - not live yet")
}

if (-not $ready) { Write-Output 'TIMED OUT - build may still be running.'; exit 1 }

Write-Output ''
Write-Output '=== LIVE ASSET CHECK ==='
foreach ($p in $paths) {
    $u = $base + $p
    try {
        $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 25
        $label = if ($p -eq '') { '(landing page)' } else { $p }
        Write-Output ("  [{0}] {1,-48} {2} bytes" -f $r.StatusCode, $label, $r.RawContentLength)
    } catch {
        Write-Output ("  [FAIL] " + $p + " -> " + $_.Exception.Message)
    }
}

Write-Output ''
Write-Output '=== CONTENT SPOT CHECK ==='
$html = (Invoke-WebRequest -Uri $base -UseBasicParsing -TimeoutSec 25).Content
Write-Output ("  safety notice present : " + ($html -match '988'))
Write-Output ("  seven rungs present   : " + (([regex]::Matches($html,'class="step"')).Count -eq 7))
Write-Output ("  copy-primer button    : " + ($html -match 'copyPrimer'))
Write-Output ("  no token leaked       : " + (-not ($html -match 'ghp_')))
Write-Output '--- LIVE VERIFY COMPLETE ---'
