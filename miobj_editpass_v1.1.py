import tkinter as tk
from tkinter import filedialog
import json
import os
import datetime
import random, string

# バージョン情報
ver = "v1.1 by yurie"
file_entry_status = "未選択"
folder_entry_status = "未選択"

# ランダムな文字列を生成する関数
def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# ファイルエントリをチェックする関数
def check_file_entry():
    file_path = file_entry.get()
    if not file_path:
        file_result_label.config(text="未選択", fg="red")
    elif file_path.endswith(".miobject"):
        file_result_label.config(text=os.path.basename(file_path), fg="green")
    else:
        file_result_label.config(text="無効なファイル形式", fg="red")

# フォルダエントリをチェックする関数
def check_folder_entry():
    folder_path = folder_entry.get()
    if not folder_path:
        folder_result_label.config(text="未選択", fg="red")
    else:
        folder_result_label.config(text=os.path.basename(folder_path), fg="green")

# .miobjectファイルを選択する関数
def select_file():
    edit_status_label.config(text="")  # ステータスをクリア
    file_path = filedialog.askopenfilename(filetypes=[("miobjectファイル", "*.miobject")])
    if file_path:
        file_entry.configure(state='normal')
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_entry.configure(state='readonly')
        check_file_entry()

# フォルダを選択する関数
def select_folder():
    edit_status_label.config(text="")  # ステータスをクリア
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.configure(state='normal')
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        folder_entry.configure(state='readonly')
        check_folder_entry()

# worldフォルダパスとファイル名を更新する関数
def override_world_dir():
    file_path = file_entry.get()
    folder_path = folder_entry.get()
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)

    if not file_path or not folder_path:
        edit_status_label.config(text="ファイルまたはフォルダが選択されていません。", fg="red")
        return

    try:
        # JSONファイルを読み込む
        with open(file_path, 'r', encoding='utf-8') as js:
            data = json.load(js)

        # フォルダパスを正規化してUnicodeに変換
        unicode_path = os.path.normpath(folder_path)  # 正規化
        folder_path = unicode_path.replace('\\', '/') + '/region'

        # フォルダパスの更新
        for resource in data.get("resources", []):
            if "world_regions_dir" in resource:
                resource["world_regions_dir"] = folder_path
            if "filename" in resource:
                resource["filename"] = "world_" + now.strftime('%Y%m%d%H%M%S.') + randomname(5)

        # JSONファイルを上書き保存
        with open(file_path, 'w', encoding='utf-8') as js:
            json.dump(data, js, indent=2, ensure_ascii=True)

        edit_status_label.config(text="書換えが完了しました。", fg="green")
    except Exception as e:
        edit_status_label.config(text=f"書換えに失敗しました: {e}", fg="red")

# メインウィンドウを作成
root = tk.Tk()
root.title(".miobject: worldフォルダパス書換えツール")
root.geometry("500x300")

# .miobjectファイル選択セクション
file_label = tk.Label(root, text="■ miobjectファイル", font=('MSGothic', 15, "bold"))
file_label.pack(anchor=tk.W)
file_result_label = tk.Label(root, text="", font=('MSGothic', 11, "bold"))
file_result_label.pack(anchor=tk.W)
file_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
file_frame.pack(anchor=tk.W, fill=tk.X, ipadx=2, ipady=2)
file_button = tk.Button(file_frame, text="選択", command=select_file)
file_button.pack(side=tk.LEFT)
file_entry = tk.Entry(file_frame, width=80, state='readonly', relief=tk.FLAT)
file_entry.pack(side=tk.LEFT, fill=tk.X)

# フォルダ選択セクション
folder_label = tk.Label(root, text="■ worldフォルダ", font=('MSGothic', 15, "bold"))
folder_label.pack(anchor=tk.W)
folder_result_label = tk.Label(root, text="", font=('MSGothic', 11, "bold"))
folder_result_label.pack(anchor=tk.W)
folder_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
folder_frame.pack(anchor=tk.W, fill=tk.X, ipadx=2, ipady=2)
folder_button = tk.Button(folder_frame, text="選択", command=select_folder)
folder_button.pack(side=tk.LEFT)
folder_entry = tk.Entry(folder_frame, width=80, state='readonly', relief=tk.FLAT)
folder_entry.pack(side=tk.LEFT, fill=tk.X)

# 書換え実行セクション
edit_button = tk.Button(root, text="書換実行", command=override_world_dir)
edit_button.pack(padx=2, pady=2)
edit_status_label = tk.Label(root, text="", font=('MSGothic', 12))
edit_status_label.pack(padx=2, pady=2)

# バージョン表示
version_label = tk.Label(root, text=f"バージョン: {ver}", font=('MSGothic', 10))
version_label.pack(side=tk.BOTTOM)

# Tkinterメインループ開始
root.mainloop()
