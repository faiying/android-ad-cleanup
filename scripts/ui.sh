#!/bin/bash
# 手机UI辅助: ./ui.sh dump [关键词] | tap X Y | swipe x1 y1 x2 y2 | shot 名字
# 需与 platform-tools/ 同级目录使用(或改 A= 指向 adb)
cd "$(dirname "$0")"
A=${ADB:-./platform-tools/adb.exe}
case "$1" in
  dump)
    $A shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1
    $A exec-out cat /sdcard/ui.xml 2>/dev/null > ui.xml
    if [ -n "$2" ]; then
      grep -o "text=\"[^\"]*$2[^\"]*\"[^>]*bounds=\"\[[0-9,]*\]\[[0-9,]*\]\"" ui.xml | head -20
    else
      wc -c ui.xml
    fi
    ;;
  tap)   $A shell input tap "$2" "$3" ;;
  swipe) $A shell input swipe "$2" "$3" "$4" "$5" 400 ;;
  shot)  $A exec-out screencap -p > "shot-${2:-now}.png"; echo "shot-${2:-now}.png" ;;
esac
