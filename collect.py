import instaloader
import json
import os
from datetime import datetime

# 監視対象のID
TARGET = "mais0on"  # ←ここを監視したいIDに変える

def main():
    # セッションIDの読み込み
    session_id = os.environ.get('SESSION_ID')
    
    L = instaloader.Instaloader()
    
    # ログイン（セッションIDを使用）
    try:
        if session_id:
            print("セッションIDを使ってログインします...")
            L.context._session.cookies.set('sessionid', session_id, domain='.instagram.com')
            L.context._session.cookies.set('ig_nrcb', '1', domain='.instagram.com')
            # ログイン確認（失敗したらエラーになる）
            user = L.test_login()
            print(f"ログイン成功: {user}")
        else:
            print("警告: SESSION_IDが設定されていません。公開データのみ取得を試みますが、ブロックされる可能性があります。")

        # データ取得
        profile = instaloader.Profile.from_username(L.context, TARGET)
        
        new_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount
        }
        print(f"取得データ: {new_data}")

        # JSONファイルの読み書き
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(new_data)

        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1) # エラーとして終了させる

if __name__ == "__main__":
    main()
