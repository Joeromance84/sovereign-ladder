$b = 'https://joeromance84.github.io/sovereign-ladder/'

for ($i = 1; $i -le 20; $i++) {
    $idx = (Invoke-WebRequest -Uri $b -UseBasicParsing -TimeoutSec 20).Content
    if ($idx -match 'MD\s*.\s*17 KB') { break }
    Start-Sleep -Seconds 15
    Write-Output "  attempt $i - index still stale"
}

Write-Output ''
Write-Output '=== SIZE LABELS AS SERVED ==='
[regex]::Matches($idx, '(MD|PDF)\s*.\s*\d+ KB') | ForEach-Object { Write-Output ("  " + $_.Value) }

Write-Output ''
Write-Output '=== ACTUAL FILE SIZES ==='
foreach ($f in @('assets/three-pillars-ai-primer.md','assets/sovereign-ladder-protocol-v4.pdf','assets/master-geometry-of-addiction-sovereignty.pdf','assets/psp-1-protocol-spec.md')) {
    $r = Invoke-WebRequest -Uri ($b + $f) -UseBasicParsing -TimeoutSec 25
    Write-Output ("  {0,-52} {1} KB" -f $f, [math]::Round($r.RawContentLength / 1024))
}
Write-Output '--- COMPLETE ---'
