$gh = 'C:\Program Files\GitHub CLI\gh.exe'

Write-Output '=== ACCOUNT ==='
$u = & $gh api user | ConvertFrom-Json
Write-Output ("  login        : " + $u.login)
Write-Output ("  id           : " + $u.id)
Write-Output ("  public repos : " + $u.public_repos)
Write-Output ("  created      : " + $u.created_at)

Write-Output ''
Write-Output '=== PUBLIC REPOS (these URLs would all move) ==='
$repos = & $gh api "users/Joeromance84/repos?per_page=100&type=owner" | ConvertFrom-Json
$pub = $repos | Where-Object { -not $_.private }
Write-Output ("  count: " + $pub.Count)
$pub | Select-Object -First 25 | ForEach-Object {
    $pages = if ($_.has_pages) { "  <-- HAS PAGES SITE" } else { "" }
    Write-Output ("  " + $_.name + $pages)
}

Write-Output ''
Write-Output '=== ORGS ALREADY OWNED ==='
$orgs = & $gh api user/orgs | ConvertFrom-Json
if ($orgs.Count -eq 0) { Write-Output '  none' }
else { $orgs | ForEach-Object { Write-Output ("  " + $_.login) } }
Write-Output '--- COMPLETE ---'
