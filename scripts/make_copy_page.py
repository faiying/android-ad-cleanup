#!/usr/bin/env python3
"""李跳跳规则剪贴板搬运工: 下载规则 -> 生成本地复制页 -> 起HTTP服务。
用法: python make_copy_page.py [规则json路径]   (缺省自动下载社区规则库)
手机浏览器打开打印出的URL -> 点"复制到剪贴板" -> 页面显示 COPIED-OK 即成功。
之后在李跳跳导入框按 adb shell input keyevent 279 (PASTE) 粘贴。
"""
import http.server
import json
import socket
import socketserver
import sys
import urllib.request
from pathlib import Path

RULES_URL = "https://raw.githubusercontent.com/chloeeee72/LiTiaotiao/main/AllRules.json"
PORT = 8899
HERE = Path(__file__).resolve().parent


def get_rules() -> str:
    if len(sys.argv) > 1:
        raw = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        print("下载规则库 ...")
        raw = urllib.request.urlopen(RULES_URL, timeout=30).read().decode("utf-8")
    json.loads(raw)  # 校验 JSON
    return raw.strip()


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # 不实际发包，只为拿到本机局域网IP
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def build_html(rules: str) -> str:
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>规则复制页</title></head>"
        '<body style="font-family:sans-serif;padding:24px">'
        '<h3 id="st">规则已加载: <span id="len"></span> 字符</h3>'
        '<button id="cp" style="font-size:26px;padding:22px 44px">复制到剪贴板</button>'
        '<textarea id="ta" style="position:fixed;left:0;top:0;width:2px;height:2px;opacity:0.01"></textarea>'
        '<script id="r" type="application/json">' + rules.replace("</", "<\\/") + "</script><script>"
        "const R=document.getElementById('r').textContent.trim();"
        "document.getElementById('len').textContent=R.length;"
        "document.getElementById('cp').onclick=()=>{"
        "const ta=document.getElementById('ta');ta.value=R;ta.focus();"
        "ta.setSelectionRange(0,R.length);let ok=false;"
        "try{ok=document.execCommand('copy');}catch(e){}"
        "if(!ok&&navigator.clipboard){navigator.clipboard.writeText(R).then("
        "()=>{document.getElementById('st').textContent='COPIED-OK '+R.length;},"
        "(e)=>{document.getElementById('st').textContent='ERR '+e;});}"
        "else{document.getElementById('st').textContent=(ok?'COPIED-OK ':'COPY-FAIL ')+R.length;}};"
        "</script></body></html>"
    )


def main():
    rules = get_rules()
    html = build_html(rules)
    out = HERE / "copy-rules.html"
    out.write_text(html, encoding="utf-8")
    ip = lan_ip()
    print(f"规则 {len(rules)} 字符, 页面已生成: {out}")
    print(f">>> 手机浏览器打开: http://{ip}:{PORT}/copy-rules.html")
    print("Ctrl+C 结束服务")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
