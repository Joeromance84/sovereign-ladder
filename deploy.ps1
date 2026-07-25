# deploy.ps1 - publish the Sovereign Ladder to GitHub Pages.
# Run AFTER: gh auth login
# Idempotent; safe to re-run.
#
# Note: native commands (gh, git) write progress to stderr, which PowerShell
# turns into error records. We deliberately do NOT use $ErrorActionPreference
# = 'Stop' here, and we branch on $LASTEXITCODE instead.

$owner = 'Joeromance84'
$name  = 'sovereign-ladder'
$repo  = 'C:\Users\logan\sovereign-ladder'
$gh    = 'C:\Program Files\GitHub CLI\gh.exe'

Set-Location $repo
$ErrorActionPreference = 'Continue'

Write-Output '=== 1. AUTH CHECK ==='
& $gh auth status 2>&1 | Out-String | Write-Output
if ($LASTEXITCODE -ne 0) { Write-Output 'NOT AUTHENTICATED - run: gh auth login'; exit 1 }

Write-Output '=== 2. DOES REPO EXIST? ==='
& $gh repo view "$owner/$name" --json name 2>&1 | Out-Null
$repoExists = ($LASTEXITCODE -eq 0)
Write-Output "  exists: $repoExists"

Write-Output '=== 3. CREATE + PUSH ==='
if (-not $repoExists) {
    & $gh repo create "$owner/$name" --public --source=. --remote=origin --push --description "A free framework for understanding and changing recurring patterns." 2>&1 | Out-String | Write-Output
    Write-Output "  create exit code: $LASTEXITCODE"
} else {
    $hasOrigin = (& git remote 2>&1) -match 'origin'
    if (-not $hasOrigin) { & git remote add origin "https://github.com/$owner/$name.git" }
    & git push -u origin main 2>&1 | Out-String | Write-Output
    Write-Output "  push exit code: $LASTEXITCODE"
}

Write-Output '=== 4. ENABLE GITHUB PAGES ==='
& $gh api "repos/$owner/$name/pages" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    & $gh api -X POST "repos/$owner/$name/pages" -f "source[branch]=main" -f "source[path]=/" 2>&1 | Out-String | Write-Output
    Write-Output "  enable exit code: $LASTEXITCODE"
} else {
    Write-Output '  Pages already enabled.'
}

Write-Output '=== 5. RESULT ==='
Start-Sleep -Seconds 6
& $gh api "repos/$owner/$name/pages" --jq '.html_url, .status' 2>&1 | Out-String | Write-Output
Write-Output "  expected URL: https://$($owner.ToLower()).github.io/$name/"
Write-Output '--- DEPLOY SCRIPT COMPLETE ---'
