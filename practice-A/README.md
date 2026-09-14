
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
- 「ターミナル」アプリを起動して、以下を入力して下さい。
```console
$ ping google.com
```
- 問題なく echo が返って来て RTT が測定できる場合、次の手順「iperf3」に進んでください。
#### Windows 11
- Windows PowerShell を起動して、コマンドプロンプトに以下を入力して下さい
```console
$ ping google.com
```
- 問題なく echo が返って来て RTT が測定できる場合、次の手順「iperf3」に進んでください。
### iperf3
- iperf は TCP/UDP のカーネルスタックを利用するので、macOS/Linux ではライブラリをインストールするだけで利用できますが、Windows の場合は、OSの設定が必要です。以下にOS毎の手順を示します。
#### macOS
- macOS のパッケージ管理ツール、Homebrew (https://brew.sh/) を利用して iperf3 をインストールます。
- 「ターミナル」アプリを起動して、以下を入力して下さい。
```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- その後、Homebrew がインストールされたら以下のコマンドで iperf3 をインストールします。
```console
$ brew update
$ brew install iperf3
```
- インストールが完了したら、以下の実測コマンドを実行してみて下さい。
```console
$ iperf3 -c paris.bbr.iperf.bytel.fr
```
- 問題なくスループットの測定結果が出力された場合、次の手順「Experiment」に進んでください。
#### Windows 11
##### Setup WSL
- Windows で iperf を実行する手順はいくつか存在しますが、本授業では今後のためにも Windows Subsystem for Linux (WSL) を利用する方法を記述します。
1. Windows の検索で「機能の有効化」を入力し、「Windows の機能の有効化または無効化」を選択
1. 「Linux 用Windows サブシステムと「仮想マシンプラットフォーム」のチェックボックスをチェック
1. Windows Update を実行（WSLのupdateがインストールされる）
1. PowerShell でコマンド ```wsl --install -d Ubuntu``` を入力
1. インストール完了後、一旦 Ubuntu を起動（「Installing, this may take a few minutes...」 と表示があり、しばらく待つ）
1. エラーが発生する場合、PowerShell を管理者権限で実行し、コマンド ```wsl --update``` を実行
1. 上記でも解決しない場合、BIOS設定の変更が必要な可能性（BIOS の Virtualization Technology を Enable に変更）
1. Enter new UNIX username: では自分の名前を。自由に決めて良いが、半角英字で。Windows と同じが望ましい ※半角スペースは絶対に入れないこと
1. Enter password: は原則 Windows と同じパスワードにすること

- Windows <-> Ubuntu 間のファイルのやり取り（同期）は、以下の手順で行います。
1. エクスプローラのパス欄に \\wsl$ と入力
1. Ubuntu をクリックし Ubuntu/home/ユーザー名 の順に辿る
- 今後、「Experiment」において結果を出力する際は、ここに出力されるので、適宜、windows 環境から参照しましょう
##### Install iperf3 with apt
- 以下のコマンドを実行し、ライブラリの更新と iperf3 をインストール
```console
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install iperf3
```
- インストールが完了したら、以下の実測コマンドを実行してみて下さい。
```console
$ iperf3 -c paris.bbr.iperf.bytel.fr
```
- 問題なくスループットの測定結果が出力された場合、次の手順「Experiment」に進んでください

## Experiment
- ここからは、ping を使って実験結果をログデータとして保存する方法を説明します。

### ping によるデータ取得
- ターミナルなどのアプリケーションで実行した ping の結果は標準出力 (stdout) に表示されます。これは当該アプリケーションが起動している間は表示されていますが、アプリケーションを終了するとデータは消去されます。そのため、実験用の結果としてまとめる場合は、ファイル出力を行う必要があります。
- 標準出力からファイル出力に切り替える場合、以下のようにコマンドの末尾に文字列 "2>&1" を入力します。（ファイル出力する時のおまじないだと思って下さい）
```console
$ ping -n -c 7 -i 0.1 google.com >output.txt 2>&1
```
-  初めの ```>output.txt``` はファイル名 output.txt に出力するという意味です。
- 上記は上書き (overwrite) する場合で、追記 (append) する場合は、
- ```>>output.txt``` として下さい。
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
- ping などの出力結果データ系列から文字列から特定の文字列を抽出したい場合、 awk/print コマンドが使えます。
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
- このように、必要な部分だけを ```$5 $7``` のように、左から数えて何番目のブロック（半角スペース " " で囲まれた文字列のかたまり）かを指定することで欲しい情報のみを出力できます。
- これを更に応用すると、
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
- のようにして不要な部分を head/tail コマンドで削除できます。
- この出力を新たなファイルとして保存することで、次回以降に勉強する python での入力処理を軽量化できます。
```console
$ cat output.txt | awk '{print $5 " " $7}' | head -n 8 | tail -n 7 >output2.txt 2>&1
```
- Linux コマンドは非常に奥が深い強力なツールです。使いこなすことで、研究データの整理・統計を自動化・省力化できます。是非、色々調べて勉強してみましょう。

