你说的这个是 macOS Sequoia (15.x) 新加的一个安全特性，属于
Local Network Privacy（本地网络访问权限），类似 iOS 14 以后 iPhone 里应用第一次访问局域网时会弹出 “xxx wants to find and connect to devices on your local network” 的提示。

在 Sequoia 里，这个权限已经被推广到更多场景，包括 命令行程序（例如 Node.js、Python 脚本、开发工具等）。
所以当 Node 或其他 CLI 工具监听本地端口或扫描局域网时，就会触发这个弹窗。

⸻

为什么会出现
	•	Node 在开发模式（npm start、vite dev 等）会起一个本地 HTTP server（监听 localhost:3000 等）。
	•	macOS Sequoia 会检测到这个监听可能涉及 LAN 访问（不仅仅是 localhost），所以要求用户授权。
	•	一旦允许，该二进制或应用会在系统偏好设置里记住，不会每次都弹。

⸻

解决办法（避免频繁弹窗）

你可以用下面几种方式：

1. 提前在设置里授权
	1.	打开 系统设置 → 隐私与安全性 → 本地网络
	2.	找到你常用的开发工具（比如 Terminal、iTerm、Node、Docker Desktop 等）
	3.	打开对应的开关，提前授予访问权限。

如果你是用 Terminal 执行 Node 脚本，那么需要授权 Terminal.app。
如果是 VSCode 的内置终端运行，需要给 VSCode 授权。

⸻

2. 用 localhost 而不是 0.0.0.0

很多开发工具默认监听 0.0.0.0（全网卡），这样会被系统认定可能访问局域网。
如果你只需要本机访问，可以改成：

node server.js --host=localhost

或者在配置里把 host 设置为 127.0.0.1/localhost。
这样一般不会触发弹窗（除非代码里显式访问 LAN）。

⸻

3. 给二进制加签 + 在 TCC 里预授权

如果你做 CI/CD 或自动化脚本，不想在运行时弹窗：
	•	用 codesign --sign - <binary> 给可执行文件签名（哪怕是 ad-hoc 签名）。
	•	然后用 tccutil 或 MDM 配置预先授予 Local Network 权限。
这个方法适合公司 IT 部署环境。

⸻

4. 禁用相关 API 调用

如果只是跑一些任务，不需要局域网访问，可以：
	•	确保不调用 dns.lookup、net.createServer 监听非 localhost 地址。
	•	确保不扫描局域网设备（Bonjour、mDNS）。

⸻

💡 我这里可以帮你整理一个 脚本化批量授权方案，让 Terminal、VSCode、Node、Docker 等开发工具一次性全开 Local Network 权限，这样你在 Sequoia 上就不会频繁被弹窗打断。

你是想让我帮你做这个批量授权脚本吗？这样以后新机器配置一次就好了。


好的，那我帮你整理一个 macOS Sequoia 批量授权 Local Network Access 的方案，这样你可以一次性给 Terminal、VSCode、Node、Docker 等常用工具开权限，不用每次运行时被弹窗打断。

⸻

1. 原理说明

macOS 15 的本地网络权限是通过 TCC（Transparency, Consent, and Control）数据库管理的，数据库文件在：

/Library/Application Support/com.apple.TCC/TCC.db   # 系统范围
~/Library/Application Support/com.apple.TCC/TCC.db # 当前用户

应用或二进制的 Local Network 权限会记录在这里。
我们可以用 sqlite3 向 TCC 数据库插入授权记录，从而实现 预授权。

⚠️ 注意：
	•	需要 root 权限（因为要改系统级的 TCC 数据库）。
	•	应用必须是 已签名的可执行文件（包括 ad-hoc 签名）。
	•	重启或 tccd 进程重启后权限才会生效。

⸻

2. 给二进制签名（避免 TCC 拒绝）

先给相关工具做一次 ad-hoc 签名（不需要证书）：

sudo codesign --force --deep --sign - /Applications/Visual\ Studio\ Code.app
sudo codesign --force --deep --sign - /Applications/Utilities/Terminal.app
sudo codesign --force --deep --sign - /Applications/iTerm.app
sudo codesign --force --deep --sign - $(which node)
sudo codesign --force --deep --sign - $(which npm)
sudo codesign --force --deep --sign - $(which yarn)
sudo codesign --force --deep --sign - $(which docker)

如果某个程序是 .app 格式，直接对 .app 签名；如果是命令行程序，就对其可执行文件路径签名。

⸻

3. 插入 Local Network 权限记录

下面是给几个常见开发工具授权的 SQL 脚本（macOS 15 的权限类型是 kTCCServiceLocalNetwork）：

sudo sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" <<EOF
INSERT OR REPLACE INTO access VALUES('kTCCServiceLocalNetwork','com.microsoft.VSCode',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,'UNUSED',0);
INSERT OR REPLACE INTO access VALUES('kTCCServiceLocalNetwork','com.apple.Terminal',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,'UNUSED',0);
INSERT OR REPLACE INTO access VALUES('kTCCServiceLocalNetwork','com.googlecode.iterm2',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,'UNUSED',0);
INSERT OR REPLACE INTO access VALUES('kTCCServiceLocalNetwork','com.docker.docker',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,'UNUSED',0);
EOF

说明：
	•	第二个参数是 bundle ID（codesign -dv --entitlements :- /path/to/app 可以查到）。
	•	1,1 表示允许并记录。
	•	命令行程序（比如 node）如果没有 bundle ID，可以考虑放进一个 .app 或用 plist 绑定 bundle ID。

⸻

4. 重启 TCC 服务

修改完 TCC 数据库后需要：

sudo killall tccd

或者重启系统，权限才会生效。

⸻

5. 一键批量脚本

我可以帮你做一个脚本，比如 grant_local_network_access.sh，执行一次，就给你常用的工具签名 + 授权，全自动完成。

⸻

我建议我们先做一版适配你机器上常用工具的批量授权脚本，
这样可以直接把 Node、Terminal、VSCode、Docker 都一次性解决。

你要我帮你现在就写好这个可直接运行的脚本吗？这样你只需要运行一次就行。