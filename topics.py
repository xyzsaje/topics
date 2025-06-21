import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import matplotlib
import matplotlib.font_manager as fm

# 下載一個開源中文字型（只需做一次）
font_path = "./NotoSansTC-Regular.otf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False



# 頁面設定：標題與圖示
st.set_page_config(page_title="AI 與資料集工具", page_icon="📊")
st.title("📊 資料集上傳與 Gemini AI 工具")

# 側邊欄頁面切換選單
page = st.sidebar.radio("選擇頁面", ["資料集分析", "Gemini AI"])

# ✅ 資料集分析頁面
if page == "資料集分析":
    uploaded_file = st.file_uploader("📁 請上傳 CSV 檔案", type="csv")

    if uploaded_file:
        try:
            # 讀取 CSV 資料
            df = pd.read_csv(uploaded_file)
            st.success("✅ 檔案上傳成功！")

            # 顯示原始資料表格
            st.subheader("🔍 原始資料")
            st.dataframe(df)

            # 圖表產生器介面
            st.subheader("📊 選擇欄位並產生圖表")
            column = st.selectbox("請選擇要分析的欄位", df.columns)

            # 使用者可選擇不同圖表類型
            chart_type = st.radio(
                "📌 選擇圖表類型",
                ["長條圖 Bar", "折線圖 Line", "圓餅圖 Pie", "直方圖 Histogram", "區域圖 Area"],
                horizontal=True
            )

            # 畫出對應圖表
            st.subheader("📈 圖表")
            fig, ax = plt.subplots()

            if chart_type == "長條圖 Bar":
                df[column].value_counts().plot(kind="bar", ax=ax)
                ax.set_xlabel(column)
                ax.set_ylabel("數量")

            elif chart_type == "折線圖 Line":
                df[column].plot(kind="line", ax=ax)
                ax.set_xlabel("索引")
                ax.set_ylabel(column)

            elif chart_type == "圓餅圖 Pie":
                df[column].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")  # 圓餅圖通常不顯示 Y 軸

            elif chart_type == "直方圖 Histogram":
                df[column].plot(kind="hist", bins=20, ax=ax)
                ax.set_xlabel(column)
                ax.set_ylabel("頻數")

            elif chart_type == "區域圖 Area":
                df[column].plot(kind="area", ax=ax)
                ax.set_xlabel("索引")
                ax.set_ylabel(column)

            # 顯示圖表
            st.pyplot(fig)

            # ✅ 加入 Gemini AI 協助說明此圖表的意義
            with st.expander("🧠 使用 Gemini AI 解釋此圖表"):
                try:
                    genai.configure(api_key=st.secrets["gemini"]["api_key"])
                    model = genai.GenerativeModel("models/gemini-2.0-flash")

                    # 設計 prompt，請 AI 分析圖表
                    prompt = f"""
你是一位資料分析助理。根據以下資訊，請用繁體中文解釋這張圖表的內容與可能意義：
- 資料欄位：{column}
- 圖表類型：{chart_type}
- 前五個值：{df[column].dropna().unique()[:5].tolist()}
請簡明扼要說明此圖表可能呈現什麼趨勢或重點。
"""

                    if st.button("🔍 生成圖表解釋"):
                        with st.spinner("Gemini 正在分析中..."):
                            response = model.generate_content(prompt)
                            st.write(response.text)

                except Exception as e:
                    st.error(f"⚠️ AI 解釋失敗：{e}")

        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
    else:
        st.info("📂 請先上傳一份 CSV 檔案")

# ✅ Gemini AI 聊天頁面
else:
    st.header("🤖 Gemini AI 助理")

    try:
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        user_input = st.text_input("請輸入你的問題：")
        if st.button("送出問題") and user_input.strip():
            with st.spinner("AI 回覆中，請稍候..."):
                try:
                    response = model.generate_content(user_input)
                    st.success("AI 回答：")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"⚠️ 發生錯誤：{e}")
    except Exception as e:
        st.error(f"❌ 無法載入 Gemini 模型：{e}")
