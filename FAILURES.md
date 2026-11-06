\# FAILURES.md

A log of things that went wrong, written as I go.



\## Template

\### \[date] error  - 2026-11-06 First git push failed with "Invalid username or token"

\- What I tried:   git push -u origin main to my new GitHub repo.

\- What went wrong:  Authentication failed and no login window appeared.

\- Why: No credential helper was set in my global Git config, so Git could not open the browser sign-in. GitHub does      not accept account passwords for Git

\- Fix: - et the credential helper with `git config --global credential.helper manager`, then pushed again. A browser sign-in opened and the push worked.



