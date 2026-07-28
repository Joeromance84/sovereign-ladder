Set-Location 'C:\Users\logan\sovereign-ladder'
Write-Output '=== COMMITS ==='
git -c core.pager=cat log --oneline --reverse | ForEach-Object { Write-Output ("  " + $_) }
Write-Output ''
Write-Output '=== GROWTH ==='
git -c core.pager=cat log --reverse --format=%H | Select-Object -First 1 | ForEach-Object {
    $first = $_
    foreach ($f in @('assets/three-pillars-ai-primer.md','assets/psp-1-protocol-spec.md','index.html')) {
        $a = (git -c core.pager=cat show ($first + ':' + $f) 2>$null | Measure-Object -Character).Characters
        $b = (Get-Content $f -Raw).Length
        Write-Output ("  {0,-40} {1,6} -> {2,6} bytes" -f $f, $a, $b)
    }
}
Write-Output ''
Write-Output '=== HARD RULES NOW ==='
Select-String -Path 'assets\psp-1-protocol-spec.md' -Pattern '^R\d+\.' | ForEach-Object { Write-Output ("  " + $_.Line.Substring(0, [Math]::Min(72, $_.Line.Length))) }
Write-Output ''
Write-Output '=== TOOLS BUILT ==='
Get-ChildItem tools -File | ForEach-Object { Write-Output ("  " + $_.Name) }
