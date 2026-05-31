# rescue

**rescue 1.0** &mdash; Copyright (c) 2026 Joseph M. Miller MD MPH &mdash; MIT License

When a long chat fills up, you lose the thread. rescue moves a working
chat session into a fresh one with zero install: a self-contained,
hash-verified zip carries session state and a staged workdir, and a
small Python bootstrap restores it on any machine with `python3`.
Cross-platform (Linux, macOS, WSL2). Currently in friends-beta &mdash;
bug reports welcome via Issues.

## This is the bare test build

`rescue-1.0-bare.zip` carries **no real session content** by design.
Its only job is to confirm the bootstrap runs and stages a workdir on
your platform. A real rescue capsule carries live state; this one does
not, so it is safe to share.

## What to do

1. Download `rescue-1.0-bare.zip` from the Releases page.
2. (Recommended) Verify it &mdash; see **Verifying your download** below.
3. Unzip it.
4. From a terminal in the unzipped folder, run:

   ```
   python3 run.py
   ```

5. You should see the banner, `VERIFIED: SHA256SUMS`, a `STAGED:` line,
   and the bare test state. If you reach `RECOVERY COMPLETE`, rescue
   ran correctly on your machine.

## Verifying your download

The zip ships with a `SHA256SUMS` file covering its contents, and
`run.py` re-checks every file against it at startup, aborting on any
mismatch. The expected SHA-256 of the release asset itself is published
on the Releases page &mdash; compare it against your downloaded copy:

- macOS / Linux: `shasum -a 256 rescue-1.0-bare.zip`
- Windows (PowerShell): `Get-FileHash rescue-1.0-bare.zip -Algorithm SHA256`

If the value does not match the one on the Releases page, do not run it.

## Requirements

`python3` (3.8+). No third-party packages. macOS ships python3; on
Windows use WSL2; Linux as-is.

## License

MIT &mdash; see [LICENSE](LICENSE). Provided "AS IS", without warranty.

## Feedback

Please open an **Issue** with your OS/version and what happened.
Bug reports only &mdash; please do not submit code in the beta.
