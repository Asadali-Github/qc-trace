# HYPOTHESES amendments 6-7: one tool call per turn (parallel_tool_calls=false). Resumable.
# Gemini Argon and Nemotron Super were stopped after their first run: their providers
# ignored the setting (more than one call in a turn), as amendment 7 requires.
Set-Location $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"
$env:QCTRACE_RUNS = "$PSScriptRoot\results\serial_runs.jsonl"
$cap = "17.9"   # cumulative recorded spend
python -u run_eval.py --mode live --model "anthropic/claude-haiku-5.5" --families 1,4,5,7,8 --seeds 2 --trials 3 --temperature 0.7 --prompt-variant serial --budget-usd $cap *>> results\serial.log
python -u run_eval.py --mode live --model "anthropic/claude-sonnet-5.5" --families 1,4,8 --seeds 2 --trials 3 --temperature 0.7 --prompt-variant serial --budget-usd $cap *>> results\serial.log
python -u run_eval.py --mode live --model "anthropic/claude-opus-5.5" --families 1,4,8 --seeds 1 --trials 3 --temperature 0.7 --prompt-variant serial --budget-usd $cap *>> results\serial.log
"SERIAL FINISHED $(Get-Date -Format s)" | Out-File -Append results\serial.log
