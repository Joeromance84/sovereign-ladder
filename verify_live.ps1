$b = 'https://joeromance84.github.io/sovereign-ladder/'

Write-Output 'Waiting for Pages rebuild...'
for ($i = 1; $i -le 20; $i++) {
    try {
        $p = (Invoke-WebRequest -Uri ($b + 'assets/three-pillars-ai-primer.md') -UseBasicParsing -TimeoutSec 20).Content
        if ($p -match 'BEFORE YOU BEGIN') { break }
    } catch { }
    Start-Sleep -Seconds 15
}

$primer = (Invoke-WebRequest -Uri ($b + 'assets/three-pillars-ai-primer.md') -UseBasicParsing -TimeoutSec 25).Content
$psp    = (Invoke-WebRequest -Uri ($b + 'assets/psp-1-protocol-spec.md') -UseBasicParsing -TimeoutSec 25).Content

Write-Output ''
Write-Output '=== PRIMER ==='
Write-Output ("  reader block present     : " + ($primer -match 'BEFORE YOU BEGIN'))
Write-Output ("  AI storage warning       : " + ($primer -match 'can be subpoenaed'))
Write-Output ("  bounded disclosure       : " + ($primer -match 'never have to narrate your life'))
Write-Output ("  hesitation is a step     : " + ($primer -match 'Naming the hesitation is Rung 1 work'))
Write-Output ("  AI-side reciprocal rule  : " + ($primer -match 'stop asking'))
Write-Output ("  inversion prohibited     : " + ($primer -match 'reluctance to disclose is itself evidence'))

Write-Output ''
Write-Output '=== PSP-1 ==='
Write-Output ("  R5 strengthened          : " + ($psp -match 'primary control vector'))
Write-Output ("  withholding = boundary   : " + ($psp -match 'Withholding is a boundary'))
Write-Output ("  bounded invitation       : " + ($psp -match 'never as a precondition of help'))

Write-Output ''
Write-Output '=== SYNC ==='
Write-Output ("  primer bytes             : " + $primer.Length)
Write-Output ("  psp-1 bytes              : " + $psp.Length)
Write-Output '--- VERIFY COMPLETE ---'
