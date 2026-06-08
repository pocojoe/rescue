# Rescue

**Move the work of a chat that is running out of room into a fresh chat -- without losing the thread.**

Rescue is a single-use, natural-language program a chat *performs*. It carries a degrading conversation's working state into a new chat, where the work continues. Separate versions per platform: Claude and GPT are cross-compatible (zip); Gemini is text-only (no zip). Not tested against Grok.

Source: [github.com/pocojoe/rescue](https://github.com/pocojoe/rescue) -- MIT License -- (c) 2026 Joseph M. Miller MD MPH

---

## The problem it solves

A chat used for a long time becomes unreliable: context gets compacted, earlier decisions drift, and files loaded along the way fall out of reach. Rescue captures what matters before that happens and re-establishes it cleanly in a fresh chat.

## How to use it

Rescue has two sides. It detects which one applies from context.

**Pack side -- in the tired chat.** Download the version for your platform, upload it into the chat you want to move out of, and tell that chat: **"Read and follow directions."**

**Recover side -- in a fresh chat.** Open a new chat, upload the capsule the pack side produced, and tell that chat: **"Read and follow directions."**

## License

Released under the MIT License. Free to use, change, and share. Provided "as is", without warranty.
