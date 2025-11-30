"""
株式投資分析アプリケーション
日本の主要銘柄の株価データを取得・分析し、投資判断をサポートするStreamlitアプリ
"""

import streamlit as st
import yfinance as yf
import pandas as pd

# 銘柄コード辞書
STOCK_SYMBOLS = {
    # 5万円以下で100株購入可能な銘柄
    "1301.T": "極洋",
    "4004.T": "昭和電工",
    "7270.T": "富士通テン",
    "9439.T": "東京通信グループ",
    "8410.T": "セブン銀行",
    # 主要銘柄（参考用）
    "7203.T": "トヨタ自動車",
    "8306.T": "三菱UFJフィナンシャル・グループ",
    "9984.T": "ソフトバンクグループ",
    "6758.T": "ソニーグループ",
    "9433.T": "KDDI",
    "9434.T": "ソフトバンク"
}

@st.cache_data(ttl=3600)  # 1時間キャッシュしてAPI負荷を軽減
def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    指定された銘柄の株価データを取得
    
    Parameters:
        symbol: 銘柄コード (例: "7203.T")
        period: 取得期間 (デフォルト: "1y")
    
    Returns:
        株価データを含むDataFrame (Date, Open, High, Low, Close, Volume)
    
    Raises:
        Exception: データ取得に失敗した場合
    """
    try:
        # yfinanceを使用してデータを取得
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        
        # データが空でないことを確認
        if data.empty:
            raise ValueError(f"銘柄コード {symbol} のデータを取得できませんでした。銘柄コードが正しいか、またはインターネット接続を確認してください。")
        
        # データポイントが十分にあるか確認
        if len(data) < 25:
            raise ValueError(f"取得したデータが不十分です（{len(data)}日分）。移動平均の計算には最低25日分のデータが必要です。")
        
        return data
    
    except ValueError as ve:
        # データ検証エラーはそのまま再スロー
        raise ve
    except Exception as e:
        # その他のエラー（ネットワークエラーなど）
        raise Exception(f"株価データの取得に失敗しました: {str(e)}\nインターネット接続を確認するか、しばらく時間をおいて再度お試しください。")

def calculate_moving_average(data: pd.DataFrame, window: int = 25) -> pd.Series:
    """
    移動平均を計算
    
    Parameters:
        data: 株価データ
        window: 移動平均の期間（日数）
    
    Returns:
        移動平均値のSeries
    
    Raises:
        ValueError: データが不十分な場合
    """
    if len(data) < window:
        raise ValueError(f"移動平均の計算にはデータが不足しています。{window}日分のデータが必要ですが、{len(data)}日分しかありません。")
    
    if 'Close' not in data.columns:
        raise ValueError("株価データに'Close'カラムが存在しません。")
    
    return data['Close'].rolling(window=window).mean()

def calculate_purchase_cost(current_price: float, shares: int = 100) -> float:
    """
    購入コストを計算
    
    Parameters:
        current_price: 現在の株価
        shares: 購入株数
    
    Returns:
        総購入コスト
    """
    return current_price * shares

def determine_affordability(cost: float, budget: float = 50000) -> bool:
    """
    予算内で購入可能かを判定
    
    Parameters:
        cost: 購入コスト
        budget: 予算（デフォルト: 50000円）
    
    Returns:
        購入可能な場合True
    """
    return cost <= budget

def determine_trend(current_price: float, moving_average: float) -> str:
    """
    トレンドを判定
    
    Parameters:
        current_price: 現在の株価
        moving_average: 移動平均値
    
    Returns:
        "上昇" または "下降"
    """
    if current_price > moving_average:
        return "上昇"
    else:
        return "下降"

def main():
    """メインアプリケーション"""
    # ページ設定でレイアウトをワイドに
    st.set_page_config(page_title="株式投資分析", layout="wide")
    
    st.title("📊 株式投資分析")
    
    # サイドバー: 銘柄選択
    st.sidebar.header("銘柄選択")
    
    # 銘柄リストをカテゴリ別に分ける
    affordable_symbols = {
        "1301.T": "極洋",
        "4004.T": "昭和電工",
        "7270.T": "富士通テン",
        "9439.T": "東京通信グループ",
        "8410.T": "セブン銀行",
        "9434.T": "ソフトバンク"
    }
    
    premium_symbols = {
        "7203.T": "トヨタ自動車",
        "8306.T": "三菱UFJフィナンシャル・グループ",
        "9984.T": "ソフトバンクグループ",
        "6758.T": "ソニーグループ",
        "9433.T": "KDDI"
    }
    
    # セッション状態の初期化
    if 'selected_symbol' not in st.session_state:
        st.session_state.selected_symbol = list(affordable_symbols.keys())[0]
    if 'category' not in st.session_state:
        st.session_state.category = "affordable"
    
    # カテゴリ選択
    category = st.sidebar.radio(
        "カテゴリを選択",
        options=["✅ 50,000円以下", "💎 50,000円超"],
        index=0 if st.session_state.category == "affordable" else 1
    )
    
    # カテゴリに応じて銘柄リストを切り替え
    if category == "✅ 50,000円以下":
        st.session_state.category = "affordable"
        current_symbols = affordable_symbols
    else:
        st.session_state.category = "premium"
        current_symbols = premium_symbols
    
    # 選択されたカテゴリの銘柄オプションを作成
    stock_options = {f"{code}: {name}": code for code, name in current_symbols.items()}
    
    # 現在の選択が現在のカテゴリに存在するか確認
    if st.session_state.selected_symbol not in current_symbols:
        st.session_state.selected_symbol = list(current_symbols.keys())[0]
    
    # ドロップダウンで銘柄を選択
    selected_option = st.sidebar.selectbox(
        "銘柄を選択",
        options=list(stock_options.keys()),
        index=list(stock_options.values()).index(st.session_state.selected_symbol)
    )
    
    # 選択された銘柄コードをセッション状態に保存
    st.session_state.selected_symbol = stock_options[selected_option]
    
    # 選択された銘柄の会社名を取得
    selected_company_name = STOCK_SYMBOLS[st.session_state.selected_symbol]
    
    # サイドバー: 使い方ガイド
    st.sidebar.markdown("---")
    st.sidebar.header("📖 使い方")
    
    with st.sidebar.expander("このアプリについて"):
        st.markdown("""
        日本株の分析と少額投資（5万円以下）の判断をサポートします。
        
        **機能:**
        - 過去1年間の株価チャート
        - 25日移動平均線
        - 100株購入の可否判定
        - トレンド分析
        """)
    
    with st.sidebar.expander("画面の見方"):
        st.markdown("""
        **チャート（左側）**
        - 青線：株価の推移
        - オレンジ線：25日移動平均
        
        **分析情報（右側）**
        - 💰 購入判定：100株の金額
        - ✅/❌：50,000円以下か
        - 📈 トレンド：上昇/下降
        """)
    
    with st.sidebar.expander("判定の見方"):
        st.markdown("""
        **購入判定**
        - ✅ 購入可能：50,000円以下
        - ❌ 予算超過：50,000円超
        
        **トレンド**
        - ↗ 上昇：株価 > 移動平均
        - ↘ 下降：株価 < 移動平均
        """)
    
    with st.sidebar.expander("対応銘柄"):
        st.markdown("""
        **5万円以下で購入可能**
        - 極洋、昭和電工
        - 富士通テン
        - 東京通信グループ
        - セブン銀行
        - ソフトバンク
        
        **主要銘柄（50,000円超）**
        - トヨタ、三菱UFJ
        - ソフトバンクG、ソニーG
        - KDDI
        """)
    
    with st.sidebar.expander("⚠️ 免責事項"):
        st.markdown("""
        **重要な注意事項**
        
        - このアプリは情報提供のみを目的としています
        - 投資助言や推奨ではありません
        - 実際の投資判断は自己責任で行ってください
        - 過去のデータは将来の結果を保証しません
        - 投資にはリスクが伴います
        - データの正確性を保証するものではありません
        - 金融商品取引業の登録はありません
        """)
    
    # メインエリア: 2カラムレイアウト
    try:
        # 株価データを取得
        with st.spinner(f"{selected_company_name}のデータを取得中..."):
            stock_data = get_stock_data(st.session_state.selected_symbol)
        
        # データ取得成功を確認
        if stock_data is None or stock_data.empty:
            st.error("❌ データ取得失敗")
            st.stop()
        
        # 25日移動平均を計算
        stock_data['MA_25'] = calculate_moving_average(stock_data, window=25)
        
        # 現在の株価と移動平均を取得
        current_price = stock_data['Close'].iloc[-1]
        current_ma = stock_data['MA_25'].iloc[-1]
        
        # 株価が有効な値かチェック
        if pd.isna(current_price) or current_price <= 0 or pd.isna(current_ma):
            st.warning("⚠️ データが無効です")
            st.stop()
        
        # 購入コストとトレンドを計算
        purchase_cost = calculate_purchase_cost(current_price, shares=100)
        is_affordable = determine_affordability(purchase_cost, budget=50000)
        trend = determine_trend(current_price, current_ma)
        
        # ヘッダー情報を1行で表示
        st.markdown(f"### {selected_company_name} ({st.session_state.selected_symbol})")
        
        # 2カラムレイアウト: 左側にチャート、右側に分析情報
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # チャート用のデータを準備
            chart_data = pd.DataFrame({
                '株価': stock_data['Close'],
                '25日移動平均': stock_data['MA_25']
            })
            
            # チャートを表示（高さを制限）
            st.line_chart(chart_data, height=400)
            st.caption(f"{stock_data.index[0].strftime('%Y/%m/%d')} ～ {stock_data.index[-1].strftime('%Y/%m/%d')}")
        
        with col2:
            # 現在の株価
            st.metric("現在の株価", f"¥{current_price:,.2f}")
            
            # 購入判定
            st.markdown("#### 💰 購入判定")
            st.metric("100株購入", f"¥{purchase_cost:,.0f}")
            
            if is_affordable:
                st.success("✅ 購入可能")
                st.markdown("<p style='text-align: center; font-size: 24px; color: green; font-weight: bold;'>50,000円以下</p>", unsafe_allow_html=True)
            else:
                st.warning("❌ 予算超過")
                st.markdown("<p style='text-align: center; font-size: 24px; color: orange; font-weight: bold;'>50,000円超</p>", unsafe_allow_html=True)
            
            # トレンド分析
            st.markdown("#### 📈 トレンド")
            
            if trend == "上昇":
                st.success("上昇トレンド")
                st.markdown("<p style='text-align: center; font-size: 28px; color: green; font-weight: bold;'>↗ 上昇</p>", unsafe_allow_html=True)
            else:
                st.info("下降トレンド")
                st.markdown("<p style='text-align: center; font-size: 28px; color: blue; font-weight: bold;'>↘ 下降</p>", unsafe_allow_html=True)
            
            st.caption(f"株価: ¥{current_price:,.2f}")
            st.caption(f"25日MA: ¥{current_ma:,.2f}")
        
    except ValueError as ve:
        st.error(f"❌ {str(ve)}")
    except Exception as e:
        st.error(f"❌ エラー: {str(e)}")
        st.info("💡 インターネット接続を確認してください")

if __name__ == "__main__":
    main()
