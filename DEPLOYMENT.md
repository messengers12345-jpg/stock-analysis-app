# Streamlit Cloudデプロイメントガイド

## 📋 必要なもの

- GitHubアカウント
- このプロジェクトのファイル
  - `app.py`
  - `requirements.txt`
  - `README.md`

## 🚀 デプロイ手順

### 1. GitHubリポジトリを作成

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ名を入力（例: `stock-analysis-app`）
4. 「Public」を選択（無料プランの場合）
5. 「Create repository」をクリック

### 2. プロジェクトをGitHubにアップロード

#### 方法A: GitHub Desktopを使用（初心者向け）

1. [GitHub Desktop](https://desktop.github.com/)をダウンロード・インストール
2. GitHub Desktopを開く
3. 「File」→「Add Local Repository」
4. このプロジェクトフォルダを選択
5. 「Publish repository」をクリック

#### 方法B: コマンドラインを使用

```bash
# プロジェクトフォルダで実行
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/あなたのユーザー名/stock-analysis-app.git
git push -u origin main
```

### 3. Streamlit Cloudにデプロイ

1. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
2. 「Sign up」→「Continue with GitHub」でログイン
3. 「New app」をクリック
4. 以下を入力：
   - **Repository**: `あなたのユーザー名/stock-analysis-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 「Deploy!」をクリック

### 4. デプロイ完了！

数分待つと、アプリが公開されます。
URLは `https://あなたのユーザー名-stock-analysis-app-xxxxx.streamlit.app` のような形式になります。

## 🔧 トラブルシューティング

### エラー: "ModuleNotFoundError"
- `requirements.txt`が正しくアップロードされているか確認
- 依存関係が正しく記載されているか確認

### エラー: "App failed to load"
- Streamlit Cloudのログを確認
- `app.py`の構文エラーをチェック

### デプロイが遅い
- 初回デプロイは5-10分かかることがあります
- 依存関係のインストールに時間がかかります

## 📝 更新方法

アプリを更新する場合：

1. ローカルでコードを修正
2. GitHubにプッシュ
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. Streamlit Cloudが自動的に再デプロイ

## 🔒 セキュリティ設定

### プライベートリポジトリの場合
- Streamlit Cloudの有料プラン（$20/月）が必要

### アクセス制限
1. Streamlit Cloudのダッシュボードでアプリを選択
2. 「Settings」→「Sharing」
3. アクセス権限を設定

## 💡 ヒント

- **カスタムドメイン**: 有料プランでカスタムドメインを設定可能
- **リソース制限**: 無料プランは1GB RAM、1 CPU
- **スリープ**: 7日間アクセスがないとスリープ状態に

## 📊 モニタリング

Streamlit Cloudのダッシュボードで以下を確認できます：
- アクセス数
- エラーログ
- リソース使用状況

## 🆘 サポート

問題が発生した場合：
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**公開URL例**: https://your-username-stock-analysis-app.streamlit.app
