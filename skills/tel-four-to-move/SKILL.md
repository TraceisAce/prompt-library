---
name: tel-four-to-move
description: "[OUTCOME]: Turns Tracey's list of priority matters into a weekly 'Four to Move' wall tracker: four A4 portrait pages, one per matter, in a bold flat-colour geometric design, each with the Monday first move, next moves, done-this-week, deadline, waiting-on, a Monday to Friday colour-in row and a Friday red/amber/green status. Output is a print-ready PDF plus a side-by-side preview. [TRIGGER]: Activates on '/four-to-move', 'four to move', 'help me prioritise', 'what should I focus on this week', 'wall tracker', 'keep me on track', 'priority board', 'plan my week', 'Friday reset', or a list of matters Tracey needs to move forward. [ANTI-TRIGGER]: Does NOT activate for Actionstep task set-up, calendar scheduling, firm-wide project plans, client-facing timelines, or the morning brief."
---

# Four to Move

A weekly prioritisation ritual with a printed output. Tracey names the matters that must move; Claude reduces them to at most four, sets one concrete first move for each, and produces four A4 pages to hang side by side on the wall.

## Principles

- Four is the limit. If Tracey gives more, propose which four to keep and why, and put the rest on a "next week" list in chat. Do not print more than four pages.
- The first move is the single smallest action that moves the file, startable in under 15 minutes. Verb first, one sentence, no more than about 90 characters. "Review the file" is not a first move; "Find the last thing sent and name who owes the next step" is.
- Next moves: up to three, verb first, no more than about 55 characters each. Leave a blank line rather than invent a step.
- Never guess matter facts. Where the status is unknown, use a neutral first move and leave the next moves blank.
- Legal steps printed on the page must be accurate (for example, s 21F independent advice and certification for a section 21 agreement under the Property (Relationships) Act 1976). The tracker is internal and gives no advice.
- Deadlines: calculate working days for Auckland, and check the agreement's own definition of "working day" first.

## Workflow

1. **Take the list.** Read everything Tracey provides first. For each matter capture: client or matter name, matter type, Actionstep matter number, and what needs to happen.
2. **Check status where tools allow.** If Outlook or SharePoint tools are available, search each matter (by name and matter number) for the latest correspondence, the other side's lawyer, and any dates. Read only; send nothing. If a search fails, say so once and carry on.
3. **Rank to four.** Order by: hard deadline or limitation risk, then consequence of slipping, then who is waiting (client, other side, court), then how quickly a single action unblocks it.
4. **Ask once.** Put every gap in one batch of questions: missing matter numbers, deadlines this week, current stage, who owes the next step. Build with blanks if Tracey wants the pages now; the blanks are for handwriting.
5. **Write the data file** in the scratchpad directory, never in a repository (it contains client names). Shape: `examples/example.json`. Fields per matter: `name`, `type`, `matter_no`, `first_move`, `next_moves` (list), optional `done_means` (string or two-item list), `deadline`, `waiting_on`, `since`. Top level: `week_start` (the Monday, ISO date) and `rule_time` (default `1pm`).
6. **Build and render:**
   ```bash
   python3 scripts/build.py <data.json> <out.html>
   NODE_PATH=$(npm root -g) node scripts/render.js <out.html> <Four-to-Move.pdf> <preview.png>
   ```
   Paths are relative to this skill's folder. The fonts are embedded from `assets/fonts`, so the file needs no network. If the render reports `OVERFLOW`, shorten the named page's first move or next moves and rebuild. Look at the preview before sending. If Playwright or Chromium is not available, deliver the HTML file instead: it prints correctly from Chrome or Edge (Print, A4, margins None, background graphics on).
7. **Deliver** the PDF and preview to Tracey. Printing note: A4, actual size, background graphics on.
8. **Friday reset (offer it).** On Friday, ask which files went green, carry anything amber or red forward, and rebuild for the next Monday.

## Design (do not drift)

- Cream page (#F6F1E9), deep ink text (#1C1530), TEL purple (#4B2A7B) for the page-number circle.
- Page colours in order: blue, orange, green, pink. Hero band of flat circles and pills on a 7 x 2 grid, a different arrangement per page, so the four read as one strip.
- Poppins 800 for names and numbers, 600 for labels, 400 for body.
- Circle motif throughout: check-off rings, M-T-W-T-F colour-in circles, R/A/G dots.

## Confidentiality

- The printed pages carry client names. Never commit the data file or PDF to a repository and never publish them as an artifact.
- The wall may be visible to visitors. Offer an initials-and-matter-number version (put the initials in the `name` field, for example "M.B.") whenever clients may see the office.
- Examples and templates use Client A / Matter 0000 placeholders only.
