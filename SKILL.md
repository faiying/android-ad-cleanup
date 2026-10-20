---
name: android-ad-cleanup
description: Use when cleaning ads on an Android phone via adb (splash ads, OEM push ads, LiTiaotiao rule import, no root).
---

# Android ad cleanup (no root, adb-driven)

Cleans splash/launch ads, OEM push ads, and imports LiTiaotiao skip-rules on any Android phone. Field-tested on nubia Z60 Ultra (Android 14, MyOS).

## Step 0 — Environment
- If the PC has no adb, download Google's official platform-tools (`https://dl.google.com/android/repository/platform-tools-latest-windows.zip`) and unzip. No install needed.
- Have the user enable: Settings → About phone → tap build number 7× → Developer options → USB debugging. Then `adb devices -l` must list the device. If Windows Device Manager sees the phone but adb does not = USB debugging off or the "Allow debugging?" prompt on the phone was never accepted.
- Bundled helpers: `scripts/ui.sh` (dump/tap/swipe/screenshot shortcuts — set `ADB=` to your adb path) and `scripts/make_copy_page.py` (clipboard bridge for LiTiaotiao rules, see Step 3).

## Step 1 — Disable preinstalled OEM ad components (reversible)
1. Inventory candidates: `adb shell pm list packages -s | sed 's/package://' | grep -i -E "ad|push|recommend|suggest|browser|market|theme|search"`, then inspect each with `pm list packages -f <pkg>` (APK path/name reveals whether it is an ad source). Ask the user before touching stores/browsers they may still use.
2. Disable one by one: `adb shell pm disable-user --user 0 <pkg>`. Revert anytime: `pm enable <pkg>`. Never uninstall — disable-user is safe and reversible.
3. nubia / ZTE / MyOS field-tested list (all verified safe to disable): `com.zte.recommend com.zte.analytics com.zte.mifavor.suggest com.zte.mifavor.miboard com.zte.superwallpaper.planet com.zte.intellitext cn.nubia.gamepi cn.nubia.nbgame com.ume.browser com.zte.halo.app`. After disabling `com.zte.halo.app`, re-point TTS: `settings put secure tts_default_synth <Google TTS component>`.
4. Other brands — typical ad-package patterns: `*.recommend`, `*.ads`, `mzpush`/`upush` push services, per-brand "smart services / negative-one screen / global search". Screenshot the home screen and Settings before and after every batch.
5. Mute push notifications without disabling the component: `cmd appops set <pkg> POST_NOTIFICATION ignore`.

## Step 2 — Private DNS as a global ad blocker (biggest single win against splash ads)
- Enable: `adb shell settings put global private_dns_mode hostname && adb shell settings put global private_dns_spec dns.adguard.com` (AdGuard public DNS — permanently free; servers abroad). Domestic-friendly alternative: `dot.pub` (DNSPod). Revert: set mode back to `off`.
- Always verify the network still works afterwards: `adb shell ping -c2 www.baidu.com`.
- Pitfall: shell `ping`/`curl` do NOT go through DoT, so you cannot verify blocking from the shell. The user reporting "splash ads are mostly gone in several apps" is the real evidence.

## Step 3 — Import community rules into LiTiaotiao (hello.litiaotiao.app)
1. Rule source: `https://raw.githubusercontent.com/chloeeee72/LiTiaotiao/main/AllRules.json` (community-maintained, 300+ rules; the official repo stopped updating in 2023, and the Snoopy1866 repo is also frozen).
2. Prerequisite: LiTiaotiao installed with its accessibility service on (`settings get secure enabled_accessibility_services` contains `hello.litiaotiao.app/.LttService`). adb cannot enable accessibility for you — guide the user to Settings → Accessibility.
3. A ~60 KB rules file cannot be typed via `input text`, and there is no root/clipboard command. Solution: run `python scripts/make_copy_page.py` (downloads rules, generates a local copy-page, serves it over LAN HTTP). Open the printed URL in the phone's browser, tap "复制到剪贴板"; the page turning `COPIED-OK` confirms the clipboard write.
4. In LiTiaotiao: main screen → 更多 → ⋮ (top-right) → 导入规则 → tap the input box → `adb shell input keyevent 279` (KEYCODE_PASTE pastes directly; long-press context menus are unreliable here — don't waste time). → 保存.
5. Verify end-to-end: 更多 → ⋮ → 导出规则 → a toast saying "已导出到剪贴板" proves rules are stored. Note: uiautomator cannot read that EditText's text — confirm via screenshot. Also `adb push` a copy of the rules JSON to `/sdcard/Download/` for the user's records.
6. Tell the user: don't kill LiTiaotiao's background process; most splash ads get skipped, a few hardened apps are unskippable.

## Hard-won pitfalls
- Big Chinese apps (e.g. Taobao) run anti-automation: `uiautomator dump` gets killed (rc=137). Fall back to `screencap` + vision analysis for coordinates.
- If the browser is already running in background, `am start -a VIEW -d <url>` only brings it to front without loading the URL: `am force-stop <browser pkg>` first.
- ZTE/nubia firmware strips the `cmd sensor` service and renumbers appops op codes (48 = WRITE_WALLPAPER there), so **sensor-level shake-to-open blocking is impossible without root** — don't chase it; shake gestures must be disabled per-app in each app's own settings.
- After every disable batch: `pidof <launcher pkg>` + screenshot to prove the system UI is healthy before finishing.
- Every change is reversible (components: `pm enable`; DNS: reset settings). Leave the user this "regret list".
