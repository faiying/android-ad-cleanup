# android-ad-cleanup

**English** | [中文](README.zh-CN.md)

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

## Bundled APK

LiTiaotiao (李跳跳) was discontinued in 2023 and is no longer on any app store. This repo ships a backup of the last official-line build (派大星 2.2) at `assets/litiaotiao-pai2.2.apk` — MD5 `ee2f4e1e7d92eb29a8b36267d7a7c79d` (matches the original author's published checksum). Verify before installing.

## Requirements

- adb (Google platform-tools) on the PC
- USB debugging enabled on the phone
- Python 3 (for `make_copy_page.py`)

## License

MIT

## Author

**faiying** — [GitHub](https://github.com/faiying) · more skills on [skills.sh](https://www.skills.sh/faiying)

Co-authored with [Hermes Agent](https://hermes-agent.nousresearch.com) (Nous Research) 🤝
