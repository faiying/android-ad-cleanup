# android-ad-cleanup（安卓手机广告清理技能）

[English](README.md) | **中文**

一个 [Agent Skill](https://agentskills.io)：通过 adb 清理安卓手机广告——**无需 root**。

适用于任何 AI 编程助手 / agent（Hermes、Claude Code、Codex、Cursor 等 20+ 工具），也适合人类照着手动执行。

## 能干什么

1. **禁用厂商预装广告/推送组件**（`pm disable-user`，随时可恢复，不卸载）
2. **私人 DNS 全局拦截开屏广告**（AdGuard DNS / 腾讯 DNSPod，免费）
3. **李跳跳（跳开屏广告 App）一条龙**：技能自带经过 MD5 校验的安装包 + 社区 300+ 条规则的自动导入方案（解决"60KB 规则没法用 adb 输入"的难题）

已在努比亚 Z60 Ultra（Android 14, MyOS）实测。其他品牌提供了广告包名的摸排方法；摇一摇跳转等传感器玩法为何免 root 走不通，也写在技能的"血泪坑"一节。

## 安装

```bash
npx skills add faiying/android-ad-cleanup
```

Hermes 用户：把本文件夹复制到 `<HERMES_HOME>/skills/` 下即可。

## 自带资源

| 文件 | 用途 |
|---|---|
| `assets/litiaotiao-pai2.2.apk` | 李跳跳"派大星2.2"安装包（官方停更前的最后主线版本）。**MD5：`ee2f4e1e7d92eb29a8b36267d7a7c79d`**，与原作者公告一致。安装前务必校验——李跳跳这类停更软件是挂马重灾区 |
| `scripts/make_copy_page.py` | 自动下载社区规则 → 生成本地"一键复制"网页 → 起局域网服务，手机浏览器打开点一下就把规则送进剪贴板 |
| `scripts/ui.sh` | adb 驱动手机界面的快捷命令（dump / tap / swipe / 截图） |

## 环境要求

- 电脑装有 adb（Google platform-tools）
- 手机已开启 USB 调试
- Python 3（运行 `make_copy_page.py` 用）

## 安全说明

- 所有改动**可逆**：组件用 `pm enable` 恢复，DNS 在设置里改回
- 技能内置"禁用前后截图验证系统正常"的流程，不会把手机搞砖
- 本技能不申请任何网络权限，不上传任何数据

## 许可

MIT
