# Bug Fixes

## Fix 1 — api/main.py line 6: Redis hardcoded to localhost
**Problem:** `redis.Redis(host="localhost")` fails inside Docker containers where services communicate by service name not localhost.
**Fix:** Changed to use `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD` environment variables.

## Fix 2 — api/main.py line 6: Redis password not used
**Problem:** A Redis password was defined in .env but never passed to the Redis client, meaning auth would fail against a password-protected Redis instance.
**Fix:** Added `password=os.getenv("REDIS_PASSWORD")` to the Redis client.

## Fix 3 — worker/worker.py line 6: Redis hardcoded to localhost
**Problem:** Same as Fix 1 — worker cannot reach Redis inside Docker via localhost.
**Fix:** Same environment variable pattern applied.

## Fix 4 — worker/worker.py line 6: Redis password not used
**Problem:** Same as Fix 2.
**Fix:** Same fix applied.

## Fix 5 — worker/worker.py: No graceful shutdown
**Problem:** Worker runs in infinite while True loop with no signal handling. SIGTERM from Docker is ignored, container gets force-killed after timeout, potentially losing a job mid-process.
**Fix:** Added signal.signal handlers for SIGTERM and SIGINT that set a running flag to False, allowing the current job to finish before exiting.

## Fix 6 — frontend/app.js line 5: API URL hardcoded to localhost
**Problem:** `const API_URL = "http://localhost:8000"` fails inside Docker — frontend container cannot reach API container via localhost.
**Fix:** Changed to `process.env.API_URL || "http://api:8000"`.

## Fix 7 — api/requirements.txt: No version pinning
**Problem:** Unpinned dependencies install random versions on each build, causing unpredictable behaviour in production.
**Fix:** Pinned all dependencies to specific versions.

## Fix 8 — api/.env: Real secret committed to repository
**Problem:** api/.env containing a real Redis password was committed to the repository. This is a critical security issue.
**Fix:** Removed from git tracking with `git rm --cached api/.env`, added to .gitignore, created .env.example with placeholder values.

## Fix 9 — api/main.py and worker/worker.py: Queue name mismatch
**Problem:** API pushed to queue named "job" but worker read from "jobs" (or vice versa depending on version).
**Fix:** Standardised both to use "jobs".
