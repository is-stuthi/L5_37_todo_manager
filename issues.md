# Issues Found (Pylint, Bandit, Flake8)

Before: Pylint 5.09/10, Bandit 1 High / 1 Medium / 2 Low, Flake8 4 issues.
After: Pylint 10.00/10, Bandit 0 High / 0 Medium / 3 Low (informational), Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605, High) | Security | 57 | `os.system("mail ... " + address + ...)` builds a shell string from user input, so an address like `x; rm -rf ~` runs arbitrary commands. | Use `subprocess.run([...], stdin=file, check=True)` with an argument list (no shell) and validate the address. |
| Unsafe pickle deserialization (B301 Medium, B403 Low) | Security | 3, 47 | `pickle.load` can execute arbitrary code from a tampered `tasks.pkl`. | Replace pickle with `json` for `save_tasks` and `load_tasks`. |
| Mutable default argument (W0102) | Bug | 11 | `labels=[]` is shared across calls, so labels accumulate between tasks. Labels were also never stored. | Default to `None`, create a new list inside the function, store it in the task. |
| Inconsistent return (R1710) | Bug | 33-36 | `findTask` returns an id on a match but falls off the end otherwise. | Add an explicit `return None`. |
| `random.choice` on an empty list | Bug | 70 | Raises `IndexError` if no tasks are pending. | Check `pending` is non-empty first. |
| `random.choice` for non-security use (B311, Low) | Security | 70 | Bandit warns the PRNG is not cryptographically secure. | False positive: only picks a suggestion. Marked `# nosec B311` with a comment. |
| Missing encoding in `open` (W1514) | Bug | 51 | Platform-default encoding can differ between systems. | Pass `encoding="utf-8"`. |
| Naming not snake_case (C0103, 15 hits) | Style | 11-55 | `addTask`, `taskId`, `fileName` etc. violate PEP 8. | Rename to `add_task`, `task_id`, `file_name` and update all callers. |
| Missing docstrings (C0114, C0116) | Style | 1, many | Module and every function lack docstrings. | Add short docstrings. |
| `main()` runs on import | Design | 79 | Importing the module executes the demo. | Add `if __name__ == "__main__":` guard. |
| Missing whitespace around operator (E225) | Style | 12 | `taskId=len(...)` | Add spaces (`task_id = ...`). |
| Too many blank lines (E303) | Style | 40 | Three blank lines before `saveTasks`. | Reduce to two. |
| Inline comment spacing (E261) | Style | 69 | Only one space before `#`. | Use two spaces. |
| Missing whitespace after comma (E231) | Style | 74 | `"...:",len(restored)` | Add a space after the comma. |

## Remaining Bandit findings (all Low, accepted)

- B404 (import subprocess), B603 and B607 (subprocess call with a partial path `mail`): informational. No shell is used, arguments are a list, and the address is validated. `remind_by_email` is not called by the demo.
