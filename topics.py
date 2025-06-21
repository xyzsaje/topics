import streamlit as st
import pandas as pd
import google.generativeai as genai

# 設定頁面標題與圖示
st.set_page_config(page_title="AI 與資料集工具", page_icon="📊")
st.title("📊 資料集上傳與 Gemini AI 工具")

# 側邊欄功能切換
page = st.sidebar.radio("選擇頁面", ["資料集分析", "Gemini AI"])

# ✅ 資料集分析頁面
if page == "資料集分析":
    uploaded_file = st.file_uploader("請上傳 CSV 檔案", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ 檔案上傳成功！")

            # 顯示資料表
            st.subheader("🔍 原始資料")
            st.dataframe(df)

            # 顯示統計摘要
            st.subheader("📈 數值欄位摘要")
            st.write(df.describe())

            # 新增圖表產生器
            st.subheader("📊 圖表產生")
            column = st.selectbox("請選擇欄位進行圖表分析", df.columns)

            if pd.api.types.is_numeric_dtype(df[column]):
                st.line_chart(df[column])
            else:
                st.bar_chart(df[column].value_counts())

        except Exception as e:
            st.error(f"❌ 讀取資料時發生錯誤：{e}")
    else:
        st.info("📁 請上傳一份 CSV 檔案以開始分析。")

# ✅ Gemini AI 頁面
else:
    st.header("🤖 Gemini AI 助理")

    # 設定 API 金鑰
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
