# -*- coding: utf-8 -*-
import io, re

# ========== A. 服务器：加 hashlib/json import + 目录列表 API ==========
sp = r"D:\相册管理\暂存站服务器.py"
with io.open(sp, "r", encoding="utf-8") as f:
    sc = f.read()

def srep(old, new):
    global sc
    assert sc.count(old) == 1, "srv pattern count=%d: %r" % (sc.count(old), old[:100])
    sc = sc.replace(old, new)

srep("""import os
import sys
import ssl
import socket
import datetime
import urllib.parse
import urllib.request
import urllib.error""",
"""import os
import sys
import ssl
import socket
import json
import hashlib
import datetime
import urllib.parse
import urllib.request
import urllib.error""")

srep("""        p = urllib.parse.urlparse(self.path).path.rstrip('/')
        if p == '/ca.crt':""",
"""        lp = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        # 水印·油画目录列表（含 sha1，供应用对账外部新增/删除）
        if lp.startswith('/美化成品+水印/list'):
            d = safe_path('/美化成品+水印')
            if d is None:
                self._headers(403)
                self.wfile.write(b'forbidden')
                return
            files = []
            try:
                for fn in os.listdir(d):
                    if fn.startswith('.'):
                        continue
                    fp = os.path.join(d, fn)
                    if not os.path.isfile(fp):
                        continue
                    h = hashlib.sha1()
                    with open(fp, 'rb') as f:
                        for chunk in iter(lambda: f.read(65536), b''):
                            h.update(chunk)
                    files.append({'name': fn, 'size': os.path.getsize(fp), 'hash': h.hexdigest()})
            except OSError:
                files = []
            data = json.dumps({'files': files}, ensure_ascii=False).encode('utf-8')
            self._headers(200, 'application/json', len(data))
            self.wfile.write(data)
            return
        p = urllib.parse.urlparse(self.path).path.rstrip('/')
        if p == '/ca.crt':""")

with io.open(sp, "w", encoding="utf-8", newline="") as f:
    f.write(sc)
print("server patched")
