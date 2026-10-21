# Lab 5: Static Code Analysis — Issue Documentation

**Target File:** `expense_tracker.py`  
**Tools Used:** Bandit (v1.9.4), Pylint (v4.1.3), Flake8 (v7.4.1)  
**Initial Pylint Score:** 5.27 / 10  
**Final Pylint Score:** 10.00 / 10  
**Flake8 Violations:** Reduced from 4 to 0  
**Bandit Findings:** All High and Medium severity security issues resolved  

---

## 1. Summary of Issues Found and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|:---|:---:|:---:|:---|:---|
| **Command Injection via Shell** (`B605`) | Security (High) | 61 | `os.system("xdg-open " + path)` spawned an unquoted shell command, allowing arbitrary command execution if `path` is manipulated. | Replaced with `subprocess.run(["xdg-open", path], check=False)` passing argument list directly without a shell. |
| **Insecure Temporary File Creation** (`B306`) | Security (Med) | 55 | `tempfile.mktemp()` returns a path without creating the file, introducing a TOCTOU race condition for symlink / overwrite attacks. | Replaced with `tempfile.mkstemp()`, which atomically creates and opens the file with secure permissions (`0o600`), and closed the descriptor. |
| **Hardcoded Insecure `/tmp` Path** (`B108`) | Security (Med) | 8 | `REPORT_DIR = "/tmp/expense_reports"` uses a hardcoded Unix temp path vulnerable to symlink pre-creation and non-portable on Windows. | Replaced with `os.path.join(tempfile.gettempdir(), "expense_reports")` and created with `mode=0o700`. |
| **Hardcoded Secret / Credential** (`B105`) | Security (Low) | 5 | Plaintext password `"demo-sync-pass"` was embedded directly in the source code, vulnerable to leaks in version control. | Sourced credentials securely from environment variable: `os.environ.get("BANK_SYNC_PASSWORD")`. |
| **Timing Attack on Password Verification** | Security / Vulnerability | 49–50 | `password == BANK_SYNC_PASSWORD` used standard equality check that short-circuits, enabling byte-by-byte timing attacks. | Replaced with constant-time comparison using `hmac.compare_digest(password.encode(), ...)`. |
| **Catching Overly Broad Exception** (`W0718`) | Bug / Code Smell | 41 | `except Exception: return None` suppressed unexpected runtime exceptions (e.g. `KeyboardInterrupt`, memory errors), masking defects. | Refactored `biggest_expense()` to use Python's built-in `default=None` parameter in `max()` without requiring `try...except`. |
| **Global State Mutation** (`W0603`) | Code Quality | 29 | `global monthly_budget` created mutable global state, leading to hidden coupling and testing side effects. | Encapsulated configuration inside a dictionary structure `SETTINGS = {"monthly_budget": 20000}`. |
| **Unpythonic Loop with `range(len())`** (`C0200`) | Code Quality | 45 | `for i in range(len(expenses))` manually indexed the collection with `expenses[i]` instead of idiomatic Python iteration. | Refactored to `for i, expense in enumerate(EXPENSES, start=1):` for cleaner, faster traversal. |
| **Invalid Naming Conventions** (`C0103`) | PEP 8 / Convention | 7, 11, 20, 28, 33, 38, 44, 49, 53, 59 | Functions, variables, and constants used camelCase (`addExpense`, `totalByCategory`, `reportPath`) and uncapitalized globals (`monthly_budget`). | Converted all function/parameter names to `snake_case` and global constants to `UPPER_CASE_WITH_UNDERSCORES`. |
| **Missing Module & Function Docstrings** (`C0114`, `C0116`) | Maintainability | 1, 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 | Neither the module nor any of the defined functions provided docstrings documenting behavior, arguments, or returns. | Added descriptive, PEP 257 compliant docstrings to the module and each individual function. |
| **Whitespace Before Colon** (`E203`) | PEP 8 Style | 15 | Redundant whitespace before colon in dictionary key-value definition: `"amount" : amount`. | Removed whitespace to adhere to standard Python dictionary formatting: `"amount": amount`. |
| **Expected 2 Blank Lines Between Functions** (`E302`) | PEP 8 Style | 44 | Only 1 blank line separated top-level functions `biggestExpense` and `printLedger`. | Enforced standard 2 blank lines between all top-level functions. |
| **Inline Comment Spacing** (`E261`) | PEP 8 Style | 74 | Single space was placed before the inline comment: `... remainingBudget()) # after setBudget`. | Added two spaces before the `#` inline comment token. |
| **Line Length Exceeded (> 79 Chars)** (`E501`) | PEP 8 Style | 77 | Print summary statement was 93 characters long, violating PEP 8's 79-character limit. | Split long expressions and function calls across multiple lines with proper indentation. |
| **Missing Trailing Newline at End of File** (`W292`, `C0304`) | POSIX / PEP 8 | 80 | File ended abruptly on the last line without a POSIX-compliant trailing newline character (`\n`). | Ensured standard trailing newline at end of file. |

---

## 2. Detailed Tool-by-Tool Breakdown

### A. Bandit (Security Analysis)

1. **`B605` (High Severity, High Confidence) — Starting a process with a shell:**
   - **Vulnerability:** Calling `os.system("xdg-open " + path)` invokes the system shell (`/bin/sh` or `cmd.exe`). If `path` is ever derived from user input or contains metacharacters such as `;`, `&&`, or `|`, arbitrary shell commands can be executed.
   - **Remediation:** Migrated to `subprocess.run(["xdg-open", path], check=False)` which directly passes argument vectors to the OS exec system call without invoking a command interpreter.

2. **`B306` (Medium Severity, High Confidence) — Deprecated and insecure `tempfile.mktemp()`:**
   - **Vulnerability:** `mktemp()` returns a filepath string without actually creating the file. Between the time the path is generated and when it is opened, an attacker can create a symbolic link at that location, redirecting file writes to overwrite sensitive system files (Time-of-Check to Time-of-Use race condition).
   - **Remediation:** Switched to `tempfile.mkstemp(suffix=".txt", dir=REPORT_DIR)`, which atomically creates and opens the temporary file using exclusive creation flags (`O_CREAT | O_EXCL`) and restrictive permissions (`0o600`). The opened file descriptor is safely closed with `os.close(file_descriptor)`.

3. **`B108` (Medium Severity, Medium Confidence) — Hardcoded temp directory:**
   - **Vulnerability:** Storing files in `/tmp/expense_reports` assumes a Unix layout and poses a risk on shared multi-user systems where any user can manipulate `/tmp`.
   - **Remediation:** Used `os.path.join(tempfile.gettempdir(), "expense_reports")` to retrieve the OS-specific secure temporary folder and created it with secure directory permissions (`mode=0o700`).

4. **`B105` (Low Severity, Medium Confidence) — Hardcoded password string:**
   - **Vulnerability:** Committing secrets like `"demo-sync-pass"` into source code exposes credentials to version control logs and unauthorized viewers.
   - **Remediation:** Replaced hardcoded string with environment variable lookup: `os.environ.get("BANK_SYNC_PASSWORD")`.

---

### B. Pylint (Code Quality & Logical Defects)

1. **`W0718` — Catching overly broad exception:**
   - **Defect:** `except Exception:` catches every subclass of `Exception`, masking logic bugs and runtime exceptions.
   - **Remediation:** Replaced the defensive `try/except` with `max(EXPENSES, key=lambda expense: expense["amount"], default=None)`, utilizing Python's built-in `default` argument for empty sequences.

2. **`W0603` — Using the `global` statement:**
   - **Defect:** Mutating `monthly_budget` globally makes unit testing difficult and causes state collisions across modules.
   - **Remediation:** Grouped mutable application state into a clean dictionary data structure (`SETTINGS = {"monthly_budget": 20000}`).

3. **`C0200` — `consider-using-enumerate`:**
   - **Defect:** `range(len(expenses))` is unidiomatic and slow.
   - **Remediation:** Refactored to `for i, expense in enumerate(EXPENSES, start=1):`.

4. **`C0103` & `C0114`/`C0116` — Naming conventions & docstrings:**
   - **Defect:** Functions were named using Java-style camelCase (`addExpense`, `totalByCategory`), constants were lowercase, and docstrings were completely absent.
   - **Remediation:** Standardized on PEP 8 snake_case, uppercase constants, and descriptive docstrings for the module and all functions.
   - **Result:** Pylint score jumped from **5.27/10** to a **perfect 10.00/10**.

---

### C. Flake8 (Style & Formatting)

1. **`E203` (Whitespace before `:`):** Fixed whitespace in dictionary literal `{"amount": amount}`.
2. **`E302` (Expected 2 blank lines):** Added proper two-line separation between top-level functions.
3. **`E261` (At least two spaces before inline comment):** Formatted comments according to PEP 8 standards.
4. **`E501` (Line too long):** Wrapped print summary and function arguments within 79 characters.
5. **`W292` (No newline at end of file):** Appended standard POSIX trailing newline.
   - **Result:** Flake8 reports **0 errors**.

---

## 3. Verification & Metrics Summary

| Metric | Before Cleanup | After Cleanup | Target | Status |
|:---|:---:|:---:|:---:|:---:|
| **Pylint Score** | 5.27 / 10 | **10.00 / 10** | > 9.5 / 10 | **PASSED** (Exceeded) |
| **Flake8 Errors** | 4 | **0** | 0 | **PASSED** |
| **Bandit High Severity** | 1 (`B605`) | **0** | 0 | **PASSED** |
| **Bandit Medium Severity** | 2 (`B306`, `B108`) | **0** | 0 | **PASSED** |
| **Functional Equivalence** | Normal output | Exactly identical output | Identical | **PASSED** |
