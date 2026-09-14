
# Practice B: iperf によるスループット測定
## 想定動作環境
### OS
- Windows 11
- macOS 15 (Sequoia) or later ※推奨
- Linux (Ubuntu 24.04 or later) ※推奨

### ネットワーク接続
- KU WiFi, 有線 (LAN) 接続, スマホテザリング ※ データ通信量を消費します


## Experiment
- iperf3 を使って実験結果を取得し、ログデータとして保存する方法を説明します。

### iperf3 によるデータ取得（インターネット編）
- iperf3 により、インターネット上に存在するサーバと接続テストを行います。
```console
$ iperf3 -c speedtest.milkywan.fr -p 9200
Connecting to host speedtest.milkywan.fr, port 9200
[  7] local 172.28.93.150 port 49557 connected to 80.67.167.93 port 9200
[ ID] Interval           Transfer     Bitrate
[  7]   0.00-1.01   sec   256 KBytes  2.09 Mbits/sec                  
[  7]   1.01-2.01   sec  4.62 MBytes  38.8 Mbits/sec                  
[  7]   2.01-3.00   sec  12.4 MBytes   104 Mbits/sec                  
[  7]   3.00-4.00   sec  15.0 MBytes   125 Mbits/sec                  
[  7]   4.00-5.00   sec  14.9 MBytes   125 Mbits/sec                  
[  7]   5.00-6.01   sec  15.5 MBytes   130 Mbits/sec                  
[  7]   6.01-7.01   sec  11.0 MBytes  92.3 Mbits/sec                  
[  7]   7.01-8.00   sec  14.9 MBytes   125 Mbits/sec                  
[  7]   8.00-9.01   sec  10.1 MBytes  84.9 Mbits/sec                  
[  7]   9.01-10.01  sec  2.00 MBytes  16.8 Mbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  7]   0.00-10.01  sec   101 MBytes  84.4 Mbits/sec                  sender
[  7]   0.00-10.26  sec  98.8 MBytes  80.7 Mbits/sec                  receiver

iperf Done.
```
- ```speedtest.milkywan.fr``` の場合、9200~9240 のポート番号で待ち受けているので、好きなものを選択しましょう。
- ポート番号とは、アプリケーションプロセスが持つ固有の通信識別子です。IP アドレスと組み合わせて利用することで、ネットワークサービスを多重化（一つのIPアドレスで複数のアプリケーションを起動し通信）しています。
- ping の時と同様に、適宜オプションを設定し、結果をファイル出力しましょう。
```console
$ iperf3 -c speedtest.milkywan.fr -t 5 -p 9200 >iperf.txt 2>&1
```

### awk コマンドを用いたデータ系列の加工
- iperf の結果を awk で事前処理していきます。
```console
$ cat iperf.txt | grep "-" | awk '{print $3 " " $7}' | head -n 5
0.00-1.01 2.09
1.01-2.01 26.2
2.01-3.00 43.2
3.00-4.01 46.0
4.01-5.01 19.9
```
- ```grep``` は ```cat``` で出力する文字列の中から指定したものと一致する行を検索するコマンドで、こちらもよくデータ処理に使われます。
- 上記例では、```grep "-"``` とすることで、時間区間 "0.00-1.01" のような出力の部分を含む文字列を抽出できます。
- 前回の ```head/tail``` と組み合わせて、自分が欲しいデータの形式に整形していきましょう。
- この例では、第一項目が時間区間、第二項目が ```Bitrate```（スループット） 部分を抽出しています。上記は 5 s 間のサンプルですが、100 s など、統計情報として十分な結果になるように適宜オプションを指定して下さい。



### iperf3/ping によるデータ取得（ラズパイ編）
- [Raspberry Pi (ラズベリーパイ)](https://www.mext.go.jp/miraino_manabi/content/396.html) は、イギリスで誕生した教育用コンピュータで、コンピュータネットワーク分野では、IoT (Internet of Things: 物のインターネット)分野で、センサーとしても広く利用されています。（過去に、私が寄稿した [CQ interface の特設記事](https://interface.cqpub.co.jp/magazine/202402/) でもラズパイを使ったチュートリアルを行いました。本講義では、通信・ネットワーク分野で広く利用される教育用デバイスと捉えて下さい）

- 前節ではインターネット経由でのフランスに存在する公開 iperf サーバとの通信実験でしたが、インターネットを介することで、ボトルネックリンク（トラヒックが集中していて混雑しているリンク）を経由する可能性が増えますし、ISP (Internet Service Provider) などのネットワークセキュリティのポリシーで、ファイアウォールで通信が遮断される可能性も有ります。

- そこで、上記制約に囚われずに、ローカル環境での通信テストを実施するため、ラズパイを用いた WiFi 通信速度の測定方法を紹介します。一言で説明すると、**「ラズパイを Wi-Fi AP 化し、iperf3 server を立てて Wi-Fi 接続した client から、送受信速度の測定を実施する」**です。
- 以下に具体的な手順を示します。

#### ラズパイとの Wi-Fi 接続
- ラズパイのWi-Fi AP化については、既にこちらで設定しております。SSID ```pi0``` に接続して下さい。
- パスワードは ```********``` です。

#### iperf3 server 側の設定（教員/TA）
- ラズパイにおいて、iperf3 の server プロセスを立ち上げます。学生のみなさんは実施する必要はありません。LAN なのでポート番号はデフォルトでも構いませんが、オプションで適宜変更してみて下さい
```console
$ iperf3 -s 1 -p 9000
```
- 上記は port#=9000 で iperf3 server を 1 プロセス立ち上げるためのコマンドです。参加者が多い場合は参加者ごとに、プロセスを割り当てる必要があります。例えば以下のようなコマンドで起動するプロセスを同時並列化できます。
```console
$ for port in {9000..9009}; do iperf3 -s -p $port &; done
```
- 9000-9009 番まで、計10個の iperf3 server プロセスを実行するコマンドです。参加する学生数に応じて、適宜上限値を変更して下さい。また、学生毎に一つ固有のポート番号を割り当て、自分の番号以外は指定しないようにして下さい。
- 上記複数実行したプロセスは ```&``` でバックグラウンド実行されるようになっているので、プロセスを終了する時は、以下のコマンドでプロセスを終了すること。
```console
$ pkill iperf3
``` 
- 当該プロセスが実行中かどうかは、以下のコマンド等で確認できる。
```console
$ pgrep iperf3 
$ ps aux | grep iperf
$ netstat -anlt | grep LISTEN
```


#### iperf client での実験（学生）
- ラズパイのIPアドレスを指定して、iperf3 でスループットを計測してみましょう。
```console
$ iperf3 -c <ラズパイのIPアドレス> -t 5 -p <自分のポート番号> >iperf-pi.txt 2>&1
```
- ラズパイの IP アドレスの調べ方は、ターミナルにて ```ifconfig``` もしくは、```ip addr``` で確認できます。デフォルトを ```10.0.0.1``` に設定しています。
- また、LAN であれば local で名前解決できるので、```hostname``` を利用して、以下でも指定することが可能です。
```console
$ iperf3 -c pi0.local -t 5 -p <自分のポート番号> >iperf-pi.txt 2>&1
```
#### ping でのRTT測定
- ping についても同様で SSID ```pi0``` に Wi-Fi 接続した後、
```console
$ ping pi0.local 
```
- もしくは、
```console
$ ping 10.0.0.1 
```
- で通信遅延（RTT）が測定可能です。適宜、オプションを変更してデータを取得しましょう。
- iperf/ping どちらの実験にしても、KU Wi-Fi 経由でインターネットと接続する場合と、Wi-Fi 接続で無線LAN 経由でラズパイと接続する場合でどのように差があるかを分析・考察しましょう。
- 一概に、Wi-Fi 接続と言っても、Wi-Fi のMAC/PHY 層の規格（IEEE 802.11 ax なのか ac なのか、はたまた a なのか）で大きく性能は変わります。インターネットと接続する場合は Wi-Fi の先にボトルネックリンクが存在し、輻輳すると性能はTCPなどの輻輳制御により支配的になります。
- 得られた結果から、"目に見えない"ネットワークで何が起きているのか？これらの情報をもとに想像してみましょう！


## iperf3 オプション一覧（参考）
### 基本・接続

| オプション | 長形式 | 説明 | 使用例 |
|---|---|---|---|
| `-c <host>` | `--client <host>` | クライアントとして指定サーバーへ接続 | `-c ping.online.net` |
| `-p <port>` | `--port <port>` | 接続先ポートを指定 | `-p 5201` |
| `-4` | `--version4` | IPv4のみ使用 | `-4` |
| `-6` | `--version6` | IPv6のみ使用 | `-6` |
| `-B <address>` | `--bind <address>` | 送信元IPやインターフェースを指定 | `-B 192.0.2.10` |
| ― | `--connect-timeout <ms>` | 接続タイムアウトを指定 | `--connect-timeout 5000` |

### 測定条件

| オプション | 長形式 | 説明 | 使用例 |
|---|---|---|---|
| `-t <秒>` | `--time <秒>` | 測定時間を指定（既定10秒） | `-t 10` |
| `-n <量>` | `--bytes <量>` | 時間ではなく送信量で終了 | `-n 100M` |
| `-O <秒>` | `--omit <秒>` | 測定開始直後の統計を除外 | `-O 2` |
| `-i <秒>` | `--interval <秒>` | 途中経過の表示間隔 | `-i 1` |
| `-P <本数>` | `--parallel <本数>` | 並列ストリーム数を指定 | `-P 4` |
| `-R` | `--reverse` | サーバーからクライアントへ送信 | `-R` |
| ― | `--bidir` | 双方向を同時に測定 | `--bidir` |
| `-l <量>` | `--length <量>` | 送受信バッファ長を指定 | `-l 128K` |
| `-F <file>` | `--file <file>` | 指定ファイルを送受信 | `-F test.dat` |

### TCP関連

| オプション | 長形式 | 説明 | 使用例 |
|---|---|---|---|
| `-w <量>` | `--window <量>` | ソケットバッファサイズを指定 | `-w 4M` |
| `-M <bytes>` | `--set-mss <bytes>` | TCP MSSを指定 | `-M 1440` |

### UDP関連

| オプション | 長形式 | 説明 | 使用例 |
|---|---|---|---|
| `-u` | `--udp` | UDPで測定 | `-u` |
| `-b <速度>` | `--bitrate <速度>` | 目標ビットレートを指定 | `-b 10M` |
| `-l <量>` | `--length <量>` | UDPデータグラム長を指定 | `-l 1200` |
| ― | `--udp-counters-64bit` | UDPカウンターを64bit化 | `--udp-counters-64bit` |

### 出力・ログ

| オプション | 長形式 | 説明 | 使用例 |
|---|---|---|---|
| `-f <単位>` | `--format <単位>` | 結果の表示単位を指定 | `-f m` |
| `-J` | `--json` | JSON形式で出力 | `-J` |
| ― | `--json-stream` | 1行ごとのJSON形式で出力 | `--json-stream` |
| ― | `--logfile <file>` | 結果をログファイルへ保存 | `--logfile result.log` |
| ― | `--timestamps` | 各出力行に日時を付加 | `--timestamps` |
| ― | `--forceflush` | 測定間隔ごとに出力をフラッシュ | `--forceflush` |
| `-V` | `--verbose` | 詳細情報を表示 | `-V` |
| `-T <文字列>` | `--title <文字列>` | 各行に識別用文字列を付加 | `-T tokyo-test` |
| ― | `--get-server-output` | サーバー側の結果も取得 | `--get-server-output` |

## 実行例

| 目的 | コマンド |
|---|---|
| TCP送信（上り）テスト | `iperf3 -c <server> -p <port> -t 10 -i 1` |
| TCP受信（下り）テスト | `iperf3 -c <server> -p <port> -R -t 10 -O 2` |
| テキストログを保存 | `iperf3 -c <server> -p <port> -t 10 --timestamps --logfile result.log` |
| UDP 10 Mbps | `iperf3 -c <server> -p <port> -u -b 10M -t 10` |
| IPv6で測定 | `iperf3 -6 -c <server> -p <port> -t 10` |
| 接続タイムアウトを設定 | `iperf3 -c <server> -p <port> --connect-timeout 5000 -t 10` |

> セキュリティの観点から、一般的に公開サーバでは iperf のデフォルトポート 5201番とは異なるポート番号で待ち受けているので、サーバ一覧に記載されたポートを `-p` で指定する必要がある。
> インターネットを利用する際に必要なエチケットである「ネチケット」を意識して、高い並列数、長時間テスト、帯域無制限 の UDP テストは避けること。


# [TODO] Practice C: wireshark によるパケットキャプチャ入門