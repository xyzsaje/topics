import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI 與資料集工具", page_icon="📊")
st.title("📊 資料集上傳與 Gemini AI 工具")

page = st.sidebar.radio("選擇頁面", ["資料集分析", "Gemini AI"])

if page == "資料集分析":
    uploaded_file = st.file_uploader("請上傳 CSV 檔案", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ 檔案上傳成功！")
        st.dataframe(df)

else:
    st.title("🤖 Gemini AI 助理")

    # ✅ 使用 secrets 管理金鑰
    genai.configure(api_key=st.secrets["gemini"]["api_key"])

    model = genai.GenerativeModel('gemini-1.0-pro')
    user_input = st.text_input("請輸入你的問題：")

    if user_input:
        response = model.generate_content(user_input)
        st.write("AI 回答：")
        st.success(response.text)
