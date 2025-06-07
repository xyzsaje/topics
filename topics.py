import streamlit as st
import pandas as pd
import google.generativeai as genai  # ✅ 正確匯入 Gemini 模組

st.set_page_config(page_title="AI 與資料集工具", page_icon="📊")
st.title("📊 資料集上傳與 Gemini AI 工具")

# 側邊欄選單
page = st.sidebar.radio("選擇頁面", ["資料集分析", "Gemini AI"])

# === 📁 資料集分析 ===
if page == "資料集分析":
    uploaded_file = st.file_uploader("請上傳 CSV 檔案", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ 檔案上傳成功！")
        st.dataframe(df)

# === 🤖 Gemini AI 助理 ===
else:
    st.title("🤖 Gemini AI 助理")

    # ✅ 設定 API 金鑰（記得改成你的）
    genai.configure(api_key="你的_API_金鑰")

    model = genai.GenerativeModel("gemini-pro")
    user_input = st.text_input("請輸入你的問題：")

    if user_input:
        response = model.generate_content(user_input)
        st.write("AI 回答：")
        st.success(response.text)
