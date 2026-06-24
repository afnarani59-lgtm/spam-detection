param(
    [string]$Arguments,
    [string]$WorkingDir = "C:\Users\Lenovo\Documents\spam detection"
)

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "C:\Users\Lenovo\AppData\Local\Python\bin\python.exe"
$psi.Arguments = $Arguments
$psi.WorkingDirectory = $WorkingDir
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true

Write-Host "Running: python $Arguments"
$p = [System.Diagnostics.Process]::Start($psi)
$p.WaitForExit()
$out = $p.StandardOutput.ReadToEnd()
$err = $p.StandardError.ReadToEnd()

if ($out) {
    Write-Host "--- STDOUT ---"
    Write-Host $out
}
if ($err) {
    Write-Warning "--- STDERR ---"
    Write-Warning $err
}

exit $p.ExitCode
