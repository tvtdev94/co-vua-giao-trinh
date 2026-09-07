---
name: review-verify-fixes-independently
description: Re-derive fix correctness from first principles rather than reading the fixer's own self-check labels
metadata:
  type: feedback
---

When verifying another agent's fix, re-derive correctness from first principles. Do not
read their self-check annotations and confirm those.

**Why:** The cờ vua Phase 1 buổi 5 blocker was a position where every square color was
correct — the plan's own ⚠ self-check told the parent to verify color only, so it passed
while the position was unsolvable in the stated move count. The lead said this was "the one
I missed entirely; I'd checked colors and stopped there." A correct-looking self-check is
exactly what hides this class of defect. Same reason I re-derived plan.html's board
rendering instead of trusting its `v:` verdict strings.

**How to apply:** For any artifact carrying its own validation labels, compute the property
independently (script it when the space is large enough to enumerate). Necessary-but-not-
sufficient checks are the specific trap: same color does not imply reachable; type-checks
pass does not imply contract held. Also check whether a fix applied at one site survived at
every site — in the same review, a fix landed at the session heading but not at the
acceptance gate that decides whether the next phase opens.

Related: [[feedback-stale-read-concurrent-edits]]
