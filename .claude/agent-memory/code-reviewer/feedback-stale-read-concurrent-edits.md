---
name: feedback-stale-read-concurrent-edits
description: Re-read files immediately before reporting review status when another agent is concurrently editing them; line-number drift is the tell
metadata:
  type: feedback
---

When reviewing files that another agent is actively fixing, re-read immediately before
reporting which findings are "still open". Do not report status from a read taken earlier
in the session.

**Why:** In the cờ vua Phase 1 red-team, I reported 6 findings as still open; 5 had
already been fixed. The lead identified the cause from my citations being ~2-16 lines off
current — that offset is the signature of a pre-edit read. It cost the lead a round-trip
and briefly implied their fixes had failed.

**How to apply:** Before any "still open / now closed" claim, re-read the target file.
If my cited line numbers no longer match what is at those lines, treat every finding in
that report as unverified until re-checked. Applies to any review running in parallel with
an implementer.

Related: [[review-verify-fixes-independently]]
