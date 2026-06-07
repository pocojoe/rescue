# Rescue

**Move the work of a chat that is running out of room into a fresh chat — without losing the thread.**

Rescue is a single-use, natural-language program that a chat *performs*. It rescues a long-running conversation that has started to degrade and carries its working state into a new chat, where the work continues from where it left off.  Rescue has been tested on Claude and ChatGPT.  It utilizes zip files that Gemini does not support.  Rescue has not been tested against Grok.

Source: [github.com/pocojoe/rescue](https://github.com/pocojoe/rescue) · MIT License · © 2026 Joseph M. Miller MD MPH

---

## The problem it solves

A chat that has been used for a long time becomes unreliable: context gets compacted, earlier decisions drift, and files loaded along the way fall out of reach. Rescue captures what matters before that happens and re-establishes it cleanly in a fresh chat.

## What's in `rescue.zip`

`rescue.zip` is the downloadable tool. It contains four files and nothing else:

| File | Purpose |
|------|---------|
| `rescue-v1.0.ci.txt` | The rescue program — natural-language instructions a chat performs. |
| `README-newchat.txt` | Operator-facing text shown on the recovery side. |
| `README-oldchat.txt` | Operator-facing text shown on the packing side. |
| `rescue-v1.0.ci.txt.sha256` | Drift-check hash of the program, computed at build time. |

No executable code ships in the capsule — the program is text the chat reads and acts on.

## How to use it

Rescue has two sides. It detects which one applies from context.

### Pack side — in the tired chat

1. Download `rescue.zip` and upload it into the chat you want to move out of.
2. Tell the chat: **"Read and follow directions."**
3. Rescue builds the state capsule, shows the Terms of Use and the list of saved work, and asks to continue.
4. On confirmation, it produces a timestamped capsule named `rescue-<datetime>.zip` for download.

### Recover side — in a fresh chat

1. Open a **new** chat and upload the `rescue-<datetime>.zip` capsule.
2. Tell the chat: **"Read and follow directions."**
3. Rescue confirms the chat is new, optionally lists or imports the saved files, loads the carried state, shows a short "Last Discussed" resumption snippet, and asks what to do next.

Work resumes from the transferred state whether or not the working files are re-imported.

## What rescue carries

Five axes of state, plus a resumption snippet and the working files:

- **goal** — what the operator is trying to do
- **rules** — things set and not to change
- **files** — the files and things the work uses
- **decisions** — choices made, not to redo
- **next_step** — the one thing to do next
- a ~50-word **Last Discussed** snippet, and a gzipped archive of the working directory

## Integrity

A SHA-256 over the capsule contents is computed when the capsule is built and re-checked on the recovery side. A mismatch produces a warning but is not fatal — recovery proceeds so work is never blocked by a checksum difference.

## Design principles

- **Single-use, loaded at performance.** Rescue is uploaded fresh each time, performed once in the chat it was uploaded into, then discarded with that chat.
- **No self-carriage.** Rescue never copies itself into the capsule it produces.
- **Text only in transit.** No run scripts or executables travel in the capsule.
- **No host assumptions.** The sandbox uses its own layout; rescue assumes no vendor or host directory structure.
- **State always loads.** Importing the working files is optional; the five-axis state always loads so work can continue from the transfer.
- **Fresh chat only.** Rescue moves work forward into a new chat; it does not rebuild the chat it came from.

## License

Released under the MIT License. Free to use, change, and share. Provided "as is", without warranty.
