# Practice C: Python によるデータ分析
## 想定動作環境
### OS
- Windows 11
- Linux (Ubuntu 24.04) ※推奨
- macOS 15 (Sequoia) or later ※推奨

### ネットワーク接続
- KU WiFi, 有線 (LAN) 接続, スマホテザリング ※ データ通信量を消費します

### Python
- version 3.12

## Install
### Windows(WSL/Ubuntu)
- Ubuntu のターミナル上で ```apt``` を用いてライブラリをインストール
```console
$ sudo apt update
$ sudo apt install python3
```
- インストールされた python のバージョンを確認
```console
$ python3 --version
```



### macOS
### 
```console
brew install python@3.12

```


- python に必要なライブラリをインストールします。
```console
$ pip3 install numpy pandas scipy ruptures scikit-learn matplotlib
```
