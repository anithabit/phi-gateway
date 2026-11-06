# FAILURES.md
A log of things that went wrong, written as I go.

## Template
## [date] Short title
- **What I tried:**
- **What went wrong:**
- **Why:**
- **Fix:**
- **Lesson:**

---

## 2026-11-06 First git push failed with "Invalid username or token"
- **What I tried:** git push -u origin main to my new GitHub repo.
- **What went wrong:** Authentication failed and no login window appeared.
- **Why:** No credential helper was set in my global Git config, so Git could not open the browser sign-in. GitHub does not accept account passwords for Git.
- **Fix:** Set the credential helper with `git config --global credential.helper manager`, then pushed again. A browser sign-in opened and the push worked.
- **Lesson:** If git push fails with a login error, check the credential helper first.

## 2026-11-06 Groq returned 404 Not Found
- **What I tried:** Sent a test prompt to Groq using the model llama-3.3-70b-versatile.
- **What went wrong:** HTTPError 404 Not Found.
- **Why:** Groq shut down that model on 16 August 2026. The model name I was given was out of date.
- **Fix:** Changed MODEL to openai/gpt-oss-120b, Groq's recommended replacement.
- **Lesson:** Check the provider's current model list before using a model name.

### 2026-11-06 Phone numbers without dashes were not masked
- **What I tried:** I wanted to check if my system can mask phone numbers written without dashes. So I added "Backup: 5551234567" to my test note and ran the round trip.
- **What went wrong:** The number was not masked. The real number was sent to the LLM. This is a leak.
- **Why:** My phone regex needed a dash, dot or space before the last 4 digits. This number had no dash, so the regex did not find it.
- **Fix:** I made that dash optional by adding "?" in the regex. Now 5551234567 becomes [PHONE_3]. I also checked that "120/80" is still not masked.
- **Lesson:** Test each pattern with different formats, not only the normal one.