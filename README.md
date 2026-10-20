# android-ad-cleanup

An [Agent Skill](https://agentskills.io) for cleaning ads on Android phones via adb — **no root required**.

Covers three jobs:

1. **Disable preinstalled OEM ad/push components** (`pm disable-user`, fully reversible)
2. **Private DNS as a global splash-ad blocker** (AdGuard DNS / DNSPod)
3. **Import community skip-rules into LiTiaotiao (李跳跳)** — including a clipboard bridge script that solves the "60 KB rules can't be typed via adb" problem

Field-tested on nubia Z60 Ultra (Android 14, MyOS). Works on any Android phone; brand-specific package lists are provided for nubia/ZTE plus patterns for discovering them on other brands.

## Install

```bash
npx skills add <your-username>/android-ad-cleanup
```

Or in Hermes: copy this folder into `<HERMES_HOME>/skills/devops/`.

## Bundled scripts

| Script | Purpose |
|---|---|
| `scripts/make_copy_page.py` | Downloads the community LiTiaotiao rules, generates a local copy-page, serves it over LAN so the phone's browser can put the rules into its clipboard |
| `scripts/ui.sh` | `dump` / `tap` / `swipe` / `shot` shortcuts for driving the phone UI over adb |

## Requirements

- adb (Google platform-tools) on the PC
- USB debugging enabled on the phone
- Python 3 (for `make_copy_page.py`)

## License

MIT
