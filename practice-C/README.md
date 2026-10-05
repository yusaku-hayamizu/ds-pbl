# Practice C: Python によるデータ分析
## 想定動作環境
### OS
- Windows 11
- Linux (Ubuntu 24.04) ※推奨
- macOS 15 (Sequoia) or later ※推奨

### ネットワーク接続
- KU WiFi, 有線 (LAN) 接続, スマホテザリング ※ データ通信量を消費します

### Python
- version 3.14 を想定

## Install
### Windows(WSL/Ubuntu)
- WSL を起動し、Ubuntu ターミナル上で ```apt``` を用いてライブラリをインストール
```console
$ sudo apt update
$ sudo apt install python3 python3-pip
```
- インストールされた python のバージョンを確認
```console
$ python3 --version
Python 3.14.4
```
<<<<<<< HEAD
- となればインストール完了（一番右のマイナーバージョンが違ってもOK）
- python に必要なライブラリをインストール
```console
$ sudo apt install python3-numpy python3-pandas python3-scipy python3-matplotlib
```
<!-- ```console
$ pip3 install numpy pandas scipy ruptures scikit-learn matplotlib
``` -->
=======

>>>>>>> f63ea5b74b0a8058c529e49a3ef938d8ab984102

### macOS
```console
brew install python@3.14
```
