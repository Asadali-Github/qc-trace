# Main grid on the free models. Resumable: finished runs are skipped.
Set-Location $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"
foreach ($m in @("nvidia/nemotron-3.5-super-vl:free", "nvidia/nemotron-3-ultra-550b-a55b:free", "google/gemma-4-31b-it:free")) {
  python -u run_eval.py --mode live --model $m --families 1-9 --seeds 2 --trials 3 --temperature 0.7 *>> results\free_grid.log
}
"FREE GRID FINISHED $(Get-Date -Format s)" | Out-File -Append results\free_grid.log
