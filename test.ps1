function Run-Proc {
    param(
        [string]$FileName,
        [string]$Arguments,
        [string]$WorkingDir = "C:\Users\Lenovo\Documents\spam detection"
    )
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $FileName
    $psi.Arguments = $Arguments
    $psi.WorkingDirectory = $WorkingDir
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    
    $p = [System.Diagnostics.Process]::Start($psi)
    $p.WaitForExit()
    $out = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    
    [PSCustomObject]@{
        ExitCode = $p.ExitCode
        Stdout   = $out
        Stderr   = $err
    }
}

$res = Run-Proc "C:\Users\Lenovo\AppData\Local\Python\bin\python.exe" "-c `"import numpy; print('numpy:', numpy.__version__)`""
Write-Output "numpy: $($res.Stdout) $($res.Stderr)"

$res = Run-Proc "C:\Users\Lenovo\AppData\Local\Python\bin\python.exe" "-c `"import pandas; print('pandas:', pandas.__version__)`""
Write-Output "pandas: $($res.Stdout) $($res.Stderr)"

$res = Run-Proc "C:\Users\Lenovo\AppData\Local\Python\bin\python.exe" "-c `"import joblib; print('joblib:', joblib.__version__)`""
Write-Output "joblib: $($res.Stdout) $($res.Stderr)"
