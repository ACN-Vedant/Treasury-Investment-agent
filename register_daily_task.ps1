# Registers the daily Treasury market-rates fetch as a Windows Task Scheduler job.
# Run this once (as the signed-in user) to enable automatic daily updates:
#   powershell -ExecutionPolicy Bypass -File register_daily_task.ps1
#
# The task runs fetch_market_rates.py every day at 07:00 local time, which
# regenerates market_rates.js (consumed directly by treasury_agent.html) and
# writes that day's audit screenshots under rate_audit\.

$ErrorActionPreference = "Stop"

$ProjectDir = $PSScriptRoot
$PythonExe = (Get-Command python).Source
$ScriptPath = Join-Path $ProjectDir "fetch_market_rates.py"
$TaskName = "TreasuryAI_DailyMarketRates"

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`"" -WorkingDirectory $ProjectDir
$Trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Daily fetch of SOFR/SONIA/ESTR market rates for Treasury Investment AI" -Force

Write-Host "Registered scheduled task '$TaskName' to run daily at 07:00."
Write-Host "To remove it later: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
