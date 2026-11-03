"""Build the hackathon zip: dist/qc-trace-submission.zip.
Includes code, SOP, tasks, graders, tests, raw results, transcripts and docs a judge
needs. Excludes .env (API key), caches, logs and internal planning notes.
Run: python make_submission.py"""
import os, re, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dist", "qc-trace-submission.zip")
INCLUDE_DIRS = ["prompts", "tests", "audit", "results", "transcripts"]
INCLUDE_ROOT_EXT = (".py", ".md", ".txt", ".ps1")
INCLUDE_ROOT_NAMES = {".env.example", "LICENSE"}
SKIP = re.compile(r"(__pycache__|\.pyc$|\.log$|^\.env$|keep_awake\.ps1$|^dist)")

def wanted(rel):
    parts = rel.replace("\\", "/").split("/")
    if any(SKIP.search(p) for p in parts):
        return False
    if len(parts) == 1:
        return parts[0] in INCLUDE_ROOT_NAMES or parts[0].endswith(INCLUDE_ROOT_EXT)
    return parts[0] in INCLUDE_DIRS

os.makedirs(os.path.dirname(OUT), exist_ok=True)
n = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in (".git", "dist", "__pycache__", ".pytest_cache", "docs")]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, HERE)
            if wanted(rel):
                z.write(full, rel.replace("\\", "/")); n += 1
# safety checks
with zipfile.ZipFile(OUT) as z:
    names = z.namelist()
    assert "README.md" in names, "README.md must be at the zip root"
    assert not any(n == ".env" or n.endswith("/.env") for n in names), ".env must not be packaged"
    for nm in names:
        if nm.endswith((".py", ".md", ".jsonl", ".txt", ".ps1", ".example")):
            body = z.read(nm).decode("utf-8", "ignore")
            assert not re.search(r"sk-or-v1-[0-9a-f]{20,}", body), f"key-like string in {nm}"
size = os.path.getsize(OUT) / 1e6
assert size < 50, f"zip is {size:.1f} MB"
print(f"wrote {OUT}: {n} files, {size:.2f} MB, no .env, no key strings")
