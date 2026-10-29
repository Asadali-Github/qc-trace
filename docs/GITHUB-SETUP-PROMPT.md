# Prompt for a session that sets up the GitHub repo

Paste the block below into a new session. Connect the folder that contains `qctrace`
first (on this machine: `C:\Users\asadc\Desktop\micro1 Eval Papers\qctrace`).

---

```
I need you to put an existing local git repository onto GitHub as a PRIVATE repo.

CONTEXT
- The repo is the folder `qctrace`, which I've connected to this session. On my machine
  it is at C:\Users\asadc\Desktop\micro1 Eval Papers\qctrace
- It is already a git repository with 3 commits and no remote. Run `git log --oneline`
  to confirm you see 3 commits.
- My GitHub username is Asadali-Github.
- The repo name should be: qc-trace
- Description: "QC-Trace: an eval for AI agents doing clinical laboratory quality
  control, where the order of actions is the requirement, not a preference."
- It MUST be private. It is a competition entry and must not be public until after I
  submit.

WHAT TO DO, IN THIS ORDER

1. Confirm the local repo state first: `git log --oneline`, `git status`,
   `git remote -v`. Tell me what you see before doing anything else.

2. Try creating the remote repo with the GitHub REST API:
   gh api -X POST /user/repos -f name='qc-trace' -F private=true
   If that returns 403 with "sessions are bound to their configured repositories",
   that route is blocked — go to step 3. Do not keep retrying it.

3. If the API is blocked, use the browser to create it: open https://github.com/new,
   set Repository name to qc-trace, select Private, leave "Add a README file"
   UNCHECKED (the repo already has files), and click Create repository. Then confirm
   the empty repo page loaded.

4. Once the empty remote exists, give me the exact commands to run in MY OWN terminal
   to push, because my GitHub credentials live on my Windows machine and not in your
   environment:
     cd "C:\Users\asadc\Desktop\micro1 Eval Papers\qctrace"
     git remote add origin https://github.com/Asadali-Github/qc-trace.git
     git branch -M main
     git push -u origin main
   If you can push directly from your environment, try it — but check first whether
   you have credentials, and don't ask me for a token or paste one anywhere.

5. After I push, verify: confirm all 3 commits are on GitHub, confirm the repo shows
   as Private, and confirm the file list matches the local one.

HARD CONSTRAINTS
- Private only. If you cannot make it private, stop and tell me.
- Do NOT squash, amend or rewrite the commit history. The first commit is dated
  29 Oct 2026 and is my evidence of what existed before the hackathon opened on
  30 Oct — the rules require pre-existing work to be disclosed, and that history is
  the disclosure.
- Do NOT commit any API key, token or .env file. Check `git status` and the
  `.gitignore` before pushing.
- Do not change any project file. This task is only about the remote.
- Do not add a GitHub Actions workflow, licence file or README — they already exist or
  are handled elsewhere.

Report back: repo URL, visibility, and whether all 3 commits are present.
```
