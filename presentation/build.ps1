# Build the slides with XeLaTeX into build/.
# Three passes: the TikZ overlays (title page, section dividers) use page
# positions recorded in the previous pass.
#   .\build.ps1                 audience PDF  (build\main.pdf)
#   .\build.ps1 speaker-notes   notes PDF     (build\speaker-notes.pdf)
param([string]$Target = 'main')
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Force build | Out-Null
    foreach ($pass in 1..3) {
        # MiKTeX prints an update reminder on stderr; only the exit code matters.
        $null = cmd /c "xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build $Target.tex 2>nul"
        if ($LASTEXITCODE -ne 0) {
            Get-Content "build\$Target.log" -Tail 40
            throw "xelatex failed on pass $pass"
        }
    }
    $issues = @(Select-String -Path "build\$Target.log" -Pattern 'Overfull|Missing character|undefined on input')
    $issues | ForEach-Object { $_.Line }
    "build\$Target.pdf: {0:N0} bytes, {1} layout warning(s)" -f (Get-Item "build\$Target.pdf").Length, $issues.Count
}
finally { Pop-Location }
