# Linux 基本ファイル操作コマンドまとめ（初心者向け）
Linux で頻繁に使うファイル操作関連の基本コマンドを用途別にまとめます。

---

## 1. ファイル・ディレクトリの確認

### 一覧表示（ls）
```bash
ls
ls -l      # 詳細表示
ls -a      # 隠しファイルも表示
ls -lh     # サイズを人が読みやすく表示 (h は human-readable の略)
```

### カレントディレクトリまでのパスを表示（pwd）
```bash
pwd
```

### ファイルの詳細情報（stat）
```bash
stat file.txt   # あまり使わない（ ls -laなどで詳細情報を表示するほうが多い）
```

---

## 2. 作成系コマンド

### 空ファイル作成（touch）
```bash
touch file.txt
```

### ディレクトリ作成（mkdir）
```bash
mkdir dir
mkdir -p dir/subdir    # 親ディレクトリもまとめて作成
```

---

## 3. コピー・移動・削除

### コピー（cp）
```bash
cp src.txt dest.txt
cp -r dir1 dir2        # ディレクトリのコピー、シミュレーション結果などの実験結果をバックアップする際などよく使用する
```

### 移動／名前変更（mv）
```bash
mv old.txt new.txt
mv file.txt dir/
```

### 削除（rm）
```bash
rm file.txt
rm -r dir
rm -rf dir             # ⚠ 強制削除（注意）
```

---

## 4. ファイル内容の表示

### 全表示（cat）
```bash
cat file.txt    # ファイルの中身（比較的小さいファイル）をひとまず見たい場合
```

### ページ表示（less）
```bash
less file.txt   # 長い文章など、大きなファイルを表示する場合
```

### 先頭／末尾表示（head / tail）
```bash
head -n 10 file.txt
tail -n 10 file.txt
tail -f log.txt        # ログ監視
```
### 差分の表示（diff/cmp）
```bash
diff fileA.txt fileB.txt # fileA.txt と fileB.txt の違い（差分）を表示（プログラムの変更箇所のみを表示したりする際に使用する）
cmp a.out b.out # 実行ファイルなどのバイナリファイルの差（全く同じものかそうでないか）を比較する際に利用する
```

---

## 5. 検索系コマンド

### ファイル検索（find）
```bash
find . -name "*.txt"
find /var -type f -size +10M
```

### 内容検索（grep）
```bash
grep "keyword" file.txt
grep -r "keyword" dir/
```

### ファイル出力と検索の組み合わせ
```bash
cat file.txt | grep "TCP" # file.txt を表示しつつ、TCP の記載がある行のみを選択的に表示
```


---

## 6. 権限・所有者

### 権限変更（chmod）
```bash
chmod 644 file.txt
chmod +x script.sh
```

### 所有者変更（chown）
```bash
chown user:group file.txt
```

---

## 7. リンク

### リンク作成（ln）
```bash
ln file.txt hardlink.txt
ln -s file.txt symlink.txt
```

---

## 8. 容量確認

### 使用量（du）
```bash
du -h file.txt
du -sh dir/
```

### ディスク容量（df）
```bash
df -h
```

---

## 9. 圧縮・解凍

### tar コマンド
```bash
tar cf archive.tar dir/
tar xf archive.tar

tar czf archive.tar.gz dir/
tar xzf archive.tar.gz
```

---