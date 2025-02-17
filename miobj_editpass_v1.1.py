import streamlit as st
import json
import os
import datetime
import random
import string

# バージョン情報
ver = "v1.1 by yurie"

# ランダムな文字列を生成する関数
def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# worldフォルダパスとファイル名を更新する関数
def override_world_dir(data, folder_path):
    # JSTで現在時刻を取得
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)

    # フォルダパスを正規化して'/region'を付加
    normalized_path = os.path.normpath(folder_path).replace('\\', '/') + '/region'
    
    # JSONデータの更新
    for resource in data.get("resources", []):
        if "world_regions_dir" in resource:
            resource["world_regions_dir"] = normalized_path
        if "filename" in resource:
            resource["filename"] = "world_" + now.strftime('%Y%m%d%H%M%S.') + randomname(5)
    return data

st.title(".miobject: worldフォルダパス書換えツール")
st.caption("バージョン: " + ver)

# miobjectファイルのアップロード（.miobject拡張子のみ許可）
miobject_file = st.file_uploader("■ miobjectファイルを選択", type=["miobject"])
if miobject_file:
    st.success("ファイル選択済み: " + miobject_file.name)
else:
    st.info("miobjectファイルを選択してください。")

# worldフォルダパスの入力（ファイル選択に代わるテキスト入力）
folder_path = st.text_input("■ worldフォルダパスを入力", "")
if folder_path:
    st.success("フォルダ選択済み: " + os.path.basename(os.path.normpath(folder_path)))
else:
    st.info("worldフォルダパスを入力してください。")

if st.button("書換実行"):
    if not miobject_file or not folder_path:
        st.error("ファイルまたはフォルダパスが選択されていません。")
    else:
        try:
            miobject_file.seek(0)
            data = json.load(miobject_file)
            updated_data = override_world_dir(data, folder_path)
            result_json = json.dumps(updated_data, indent=2, ensure_ascii=True)
            st.success("書換えが完了しました。")
            st.download_button(
                label="変更後のファイルをダウンロード",
                data=result_json,
                file_name="modified.miobject",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"書換えに失敗しました: {e}")
            
