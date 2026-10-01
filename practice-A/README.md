
# Practice A: ping による RTT 測定
## 想定動作環境
### OS
- Windows 11
- macOS 15 (Sequoia) or later ※推奨
- Linux (Ubuntu 24.04 or later) ※推奨

### ネットワーク接続
- KU WiFi, 有線 (LAN) 接続, スマホテザリング（[注意] データ通信量を消費します）

## Installation & Test
### ping 
- ping は Windows, macOS, Linux で標準搭載のネットワークユーティリティなので、特段ライブラリなどのインストールは必要ありません。以下の手順に従い実行して下さい。
#### macOS/Ubuntu
- 「ターミナル」アプリを起動して、以下を入力して下さい。 ※ ターミナルとは、コンピュータを操作するコマンドを入力するためのアプリケーションを指し、これを利用してコンピュータに接続して操作やデータの入出力を行います。本PBLではメインで使用していきますので、基本的な[ターミナル操作コマンド](./terminal-tips.md)は覚えると作業の効率化に役立ちます。  
※ ```$``` の部分はプロンプト入力待ちを意味する記号ですので、実際は入力する必要は有りません
```console
$ ping google.com
PING google.com (172.217.209.138): 56 data bytes
64 bytes from 172.217.209.138: icmp_seq=0 ttl=110 time=5.846 ms
64 bytes from 172.217.209.138: icmp_seq=1 ttl=110 time=6.376 ms
64 bytes from 172.217.209.138: icmp_seq=2 ttl=110 time=6.369 ms
64 bytes from 172.217.209.138: icmp_seq=3 ttl=110 time=6.393 ms
64 bytes from 172.217.209.138: icmp_seq=4 ttl=110 time=6.117 ms
64 bytes from 172.217.209.138: icmp_seq=5 ttl=110 time=6.022 ms
64 bytes from 172.217.209.138: icmp_seq=6 ttl=110 time=8.176 ms
64 bytes from 172.217.209.138: icmp_seq=7 ttl=110 time=5.630 ms
64 bytes from 172.217.209.138: icmp_seq=8 ttl=110 time=5.922 ms
64 bytes from 172.217.209.138: icmp_seq=9 ttl=110 time=12.644 ms

--- google.com ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 5.630/6.950/12.644/2.012 ms
```
- 上記に示す通り、問題なく応答 (echo) が返って来て RTT (time) が測定できる場合、次の手順「iperf3」に進んでください。
- 以下に示すように echo が返ってこない（タイムアウトする）場合は、Wi-Fi/有線接続できているか、ネットワーク接続を確認してください。
```console
$ ping google.com
PING 172.217.209.138): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
...
```
- Wi-Fi/有線接続できていても echo を受信できない場合、IPアドレスの設定が正しく設定できているかを確認するため、以下のコマンドのどちらかを入力してください。
```console
$ ifconfig
$ ip addr
```
#### Windows 11
- Windows PowerShell を起動して、コマンドプロンプトに以下を入力して下さい  
※ ```$``` の部分はプロンプト入力待ちを意味する記号ですので、実際は入力する必要は有りません
```console
$ ping google.com
PING google.com (172.217.209.138): 56 data bytes
64 bytes from 172.217.209.138: icmp_seq=0 ttl=110 time=5.846 ms
64 bytes from 172.217.209.138: icmp_seq=1 ttl=110 time=6.376 ms
64 bytes from 172.217.209.138: icmp_seq=2 ttl=110 time=6.369 ms
64 bytes from 172.217.209.138: icmp_seq=3 ttl=110 time=6.393 ms
64 bytes from 172.217.209.138: icmp_seq=4 ttl=110 time=6.117 ms
64 bytes from 172.217.209.138: icmp_seq=5 ttl=110 time=6.022 ms
64 bytes from 172.217.209.138: icmp_seq=6 ttl=110 time=8.176 ms
64 bytes from 172.217.209.138: icmp_seq=7 ttl=110 time=5.630 ms
64 bytes from 172.217.209.138: icmp_seq=8 ttl=110 time=5.922 ms
64 bytes from 172.217.209.138: icmp_seq=9 ttl=110 time=12.644 ms

--- google.com ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 5.630/6.950/12.644/2.012 ms
```
- 上記に示す通り、問題なく応答 (echo) が返って来て RTT (time) が測定できる場合、次の手順「iperf3」に進んでください。
- 以下に示すように echo が返ってこない（タイムアウトする）場合は、Wi-Fi/有線接続できているか、ネットワーク接続を確認してください。
```console
$ ping google.com
PING 172.217.209.138): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
...
```
- Wi-Fi/有線接続できていても echo を受信できない場合、IPアドレスの設定が正しく設定できているかを確認するため、以下のコマンドを入力してください。
```console
$ ipconfig
```


### iperf3
- iperf は TCP/UDP のカーネルスタックを利用するので、macOS/Linux ではライブラリをインストールするだけで利用できますが、Windows の場合は、OS (wsl) 設定を行った方が効率的です。以下にOS毎の手順を示します。
#### macOS
- macOS のパッケージ管理ツール、Homebrew (https://brew.sh/) を利用して iperf3 をインストールます。
- 「ターミナル」アプリを起動して、以下を入力して下さい。
```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- その後、Homebrew がインストールされたら、以下のコマンドで iperf3 をインストールします。
```console
$ brew update
$ brew install iperf3
```
- インストールが完了したら、以下の実測コマンドを実行してみて下さい。
```console
$ iperf3 -c ping.online.net
```
- 問題なくスループットの測定結果が出力された場合、次の手順「Experiment」に進んでください。
#### Windows 11
##### Setup WSL
- Windows で iperf を実行する手順はいくつか存在しますが、本授業では今後のために Windows Subsystem for Linux (WSL) を利用する方法を記述します。
1. Windows の検索（Windowsメニュー）で「機能の有効化」と入力し、「Windows の機能の有効化または無効化」を選択
1. 「Linux 用 Windows サブシステム」と「仮想マシンプラットフォーム」のチェックボックスをチェック後、再起動
1. Windows Update を実行（WSL の update がインストールされる）
1. PowerShell でコマンド ```wsl --install -d Ubuntu``` を入力
1. インストール完了後、一旦 Ubuntu を起動（「Installing, this may take a few minutes...」 と表示があり、しばらく待つ）
  - エラーが発生する場合、PowerShell を管理者権限で実行し、コマンド ```wsl --update``` を実行
  - 上記でも解決しない場合、BIOS設定の変更が必要な可能性（BIOS の Virtualization Technology を Enable に変更）
6. Ubuntu のユーザ作成の画面に遷移したら、Enter new UNIX username: では自分の名前を入力。基本的に自由に決めて良いが、半角英字で。Windows と同じが望ましい ※半角スペースは絶対に入れないこと
1. Enter password: は原則 Windows と同じパスワードにすること

##### Data Sync
- Windows <-> Ubuntu 間のファイルのやり取り（同期）は、以下の手順で行います。
1. エクスプローラのパス欄に \\wsl$ と入力、もしくは、エクスプローラの「ネットワーク」から「Ubuntu」を検索
1. Ubuntu をクリックし Ubuntu/home/ユーザー名 の順に辿る
- 今後、「Experiment」において結果を出力する際は、ここに出力されるので、適宜、windows 環境から参照する際は利用しましょう
##### Install iperf3 with apt
- 以下のコマンドを実行し、ライブラリの更新と iperf3 をインストール
```console
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install iperf3
```
- インストールが完了したら、以下の実測コマンドを実行してみて下さい。
```console
$ iperf3 -c iperf.he.net
Connecting to host iperf.he.net, port 5201
[  7] local 192.168.100.3 port 62205 connected to 216.218.207.42 port 5201
[ ID] Interval           Transfer     Bitrate
[  7]   0.00-1.00   sec  3.62 MBytes  30.3 Mbits/sec                  
[  7]   1.00-2.00   sec  25.2 MBytes   212 Mbits/sec                  
[  7]   2.00-3.00   sec  7.12 MBytes  59.8 Mbits/sec                  
[  7]   3.00-4.00   sec  15.8 MBytes   132 Mbits/sec                  
[  7]   4.00-5.00   sec  20.4 MBytes   172 Mbits/sec                  
[  7]   5.00-6.00   sec  23.2 MBytes   195 Mbits/sec                  
[  7]   6.00-7.00   sec  21.2 MBytes   178 Mbits/sec                  
[  7]   7.00-8.00   sec  12.0 MBytes   101 Mbits/sec                  
[  7]   8.00-9.01   sec  16.6 MBytes   139 Mbits/sec                  
[  7]   9.01-10.00  sec  18.9 MBytes   159 Mbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  7]   0.00-10.00  sec   164 MBytes   138 Mbits/sec                  sender
[  7]   0.00-10.12  sec   162 MBytes   135 Mbits/sec                  receiver

iperf Done.
```
- 問題なくスループットの測定結果（Bitrate）が出力された場合、次の手順「Experiment」に進んでください。
- 以下のようなエラーが発生する場合、[公開サーバ](https://iperf.fr/iperf-servers.php)の中から別のものを選択するなどして、いくつかサーバをトライしてみてください。※ サーバを変更する際は、ポート番号（Port）の値を適切な値に変えることを忘れずに。
```console
iperf3: error - the server is busy running a test. try again later
```

## Experiment
- さて、ここからは、実際に ping を使って実験結果をログデータとして保存する方法を説明します。次週以降のデータ分析の Practice で使用していきますので、可能な限り色々なデータを取得できると良いです。

### ping によるデータ取得
- ターミナルなどのアプリケーションで実行した ping の結果はターミナルの標準出力 (stdout) に表示されます。これは当該アプリケーションが起動している間は表示されていますが、アプリケーションを終了するとデータは消去されます。そのため、実験用の結果としてまとめる場合は、特定のファイルに出力する必要があります。
- 標準出力からファイル出力に切り替える場合、以下のようにコマンドの末尾に文字列 "2>&1" を入力します。（ファイル出力する時のおまじないだと思って下さい）
```console
$ ping -n -c 7 -i 0.1 google.com >output.txt 2>&1
```
-  初めの ```>output.txt``` はファイル名 output.txt に出力するという意味です。
- 上記は上書き (overwrite) する場合で、追記 (append) する場合は、```>>output.txt``` として下さい。（```>```の数を一つ増やす）
```console
$ ping -n -c 7 -i 0.1 google.com >>output.txt 2>&1
```
- 取得したファイルを表示する場合、```cat``` コマンドを利用します。
```console
$ cat output.txt
PING google.com (142.251.118.113): 56 data bytes  
64 bytes from 142.251.118.113: icmp_seq=0 ttl=108 time=3.620 ms  
64 bytes from 142.251.118.113: icmp_seq=1 ttl=108 time=3.582 ms  
64 bytes from 142.251.118.113: icmp_seq=2 ttl=108 time=3.420 ms  
64 bytes from 142.251.118.113: icmp_seq=3 ttl=108 time=3.265 ms  
64 bytes from 142.251.118.113: icmp_seq=4 ttl=108 time=3.434 ms  
64 bytes from 142.251.118.113: icmp_seq=5 ttl=108 time=3.271 ms  
64 bytes from 142.251.118.113: icmp_seq=6 ttl=108 time=3.383 ms  
  
--- google.com ping statistics ---  
7 packets transmitted, 7 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 3.265/3.425/3.620/0.128 ms
```

### awk コマンドを用いたデータ系列の加工
- 次回以降説明する python での文字列処理を行っても良いですが、Linux 標準のコマンドラインを使ったデータの整理方法を紹介します。
- ping などの出力結果データ系列から文字列から特定の文字列を抽出したい場合、 awk/print コマンドが役に立ちます。
```console
$ cat output.txt | awk '{print $5 " " $7}'
data
icmp_seq=0 time=3.620
icmp_seq=1 time=3.582
icmp_seq=2 time=3.420
icmp_seq=3 time=3.265
icmp_seq=4 time=3.434
icmp_seq=5 time=3.271
icmp_seq=6 time=3.383
 
--- 
packets 0.0%
ms 
```
- ```awk '{print $5 " " $7}'```は左から数えて何番目のブロック（半角スペース " " で囲まれた文字列のかたまり）を print で表示するか指定することで、出力形式を指定できます。  
※ この ```" "```部分はコンピュータ用語でデリミタ (delimiter) と呼びます
- 一方で、使用したい行（icmp_seq, time の値がある行）以外である、```data```, ```---```, ```packets 0.0%```, ```ms``` などは不要な部分ですので、後にグラフ化する際に邪魔になりそうです。
- これを以下のように更に応用すると、不要な部分を head/tail コマンドで削除できます。
```console
$ cat output.txt | awk '{print $5 " " $7}' | head -n 8 | tail -n 7
icmp_seq=0 time=3.620
icmp_seq=1 time=3.582
icmp_seq=2 time=3.420
icmp_seq=3 time=3.265
icmp_seq=4 time=3.434
icmp_seq=5 time=3.271
icmp_seq=6 time=3.383
```
- 具体的には、```head -n 8 | tail -n 7``` の部分で，output.txt ファイルの2行目から8行目までの7行分を抜き出しています。まず、```head -n 8```で先頭8行に絞り、```tail -n 7``` で末尾から7行を残すという処理をしています。
- この出力を新たなファイルとして保存することで、次回以降に勉強する python での入力処理を軽量化できます。
```console
$ cat output.txt | awk '{print $5 " " $7}' | head -n 8 | tail -n 7 >output2.txt 2>&1
```
- Linux コマンドは非常に奥が深い強力なツールです。使いこなすことで、研究データの整理・統計を自動化・省力化できます。是非、「Linux, コマンド, bash」などのキーワードで色々調べて勉強し、使ってみましょう。


### インターネットにおける遅延 (RTT) の計測
- 上記の ping コマンド ```ping -n -c 7 -i 0.1 aaa.com >ping2aaa.com.log 2>&1``` を利用して、複数のサーバを宛先として選択し、複数箇所の統計情報を取得しましょう。最低3つ以上のサーバに対して計測すること、及び、標本（サンプル）数はそれぞれ 2000 以上とすること。
- 宛先となるサーバはインターネット上のノード（サーバやルータを含む総称）であればどこでも構いませんが、サンプルとして以下のリンストを表示しておきますが、以下に限りません。上記コマンドの```aaa.com```の部分を置き換える形で実行して下さい。
- ping 宛先サーバ候補リスト

| # | 代表地域 | 団体名 | 種別 | ホスト名/ドメイン名 |
|---:|---|---|---|---|
| 1 | 日本・東京 | NICT | 国立研究所 | `ntp.nict.go.jp` |
| 2 | 日本・東京 | IIJ | 通信企業 | `iij.ad.jp` |
| 3 | 日本・東京 | NTT | 通信企業 | `ntt.com` |
| 4 | 韓国 | LG | 半導体企業 | `lg.com` |
| 5 | シンガポール | NUS | 大学 | `nus.edu.sg` |
| 6 | アラブ首長国連邦 | ADNEC | 会議場 | `www.adnec.ae` |
| 7 | オーストラリア | シドニー大学 | 大学 | `sydney.edu.au ` |
| 8 | ニュージーランド | University of Auckland | 大学 | `auckland.ac.nz` |
| 9 | 米国東部 | MIT | 大学 | `mit.edu` |
| 10 | 米国西部 | Stanford University | 大学 | `stanford.edu` |
| 11 | 米国西部 | UCLA | 大学 | `ucla.edu` |
| 12 | カナダ | University of Toronto | 大学 | `utoronto.ca` |
| 13 | ブラジル | University of São Paulo | 大学 | `www.usp.br` |
| 14 | チリ | University of Chile | 大学 | `www.uchile.cl` |
| 15 | 英国 | University of Cambridge  | 大学 | `cam.ac.uk ` |
| 16 | スイス | ETH Zürich | 大学 | `ethz.ch` |
| 17 | ドイツ | Deutsche Telekom | 通信企業 | `telekom.com` |
| 18 | フランス | Orange | 通信企業 | `orange.fr` |
| 19 | 南アフリカ | CapeTown Web Hosting | 通信企業 | `capetown-web-hosting.co.za` |
| 20 | ケニア | University of Nairobi | 大学 | `uonbi.ac.ke` |


