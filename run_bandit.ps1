param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]
    $Args
)

# Run Bandit against the 'app' package by default and forward any extra arguments.
# Usage:
#   .\run_bandit.ps1                 -> scans the app/ folder
#   .\run_bandit.ps1 -q --severity-level high   -> passes -q and --severity-level high to bandit

Write-Host "Running: poetry run bandit -r app $($Args -join ' ')"
& poetry run bandit -r app @Args
