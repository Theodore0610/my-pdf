import streamlit as st
from zhipuai import ZhipuAI
import base64

# 1. 页面配置：设置为宽屏模式
st.set_page_config(layout="wide", page_title="AI PDF 阅读助手")

st.title("📚 我的 AI PDF 电子书助手")

# 2. 侧边栏配置 API Key (上线后建议填入 Secrets)
with st.sidebar:
    api_key = st.text_input("请输入智谱 API Key", type="password")
    uploaded_file = st.file_uploader("上传 PDF 电子书", type="pdf")

# 3. 主界面布局：左边 PDF，右边 AI
col1, col2 = st.columns(2)

# 左半部分：显示 PDF
with col1:
    st.subheader("PDF 文档预览")
    if uploaded_file is not None:
        # 将 PDF 转换为 base64 以便在 iframe 中显示
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info("请在左侧上传 PDF 文件")

# 右半部分：AI 对话框
with col2:
    st.subheader("🤖 AI 问答")
    
    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 聊天输入
    if prompt := st.chat_input("针对电子书提问..."):
        if not api_key:
            st.error("请先在左侧输入 API Key")
        else:
            # 用户发言
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 调用智谱 API
            client = ZhipuAI(api_key=api_key)
            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model="glm-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
            
            # 存入历史
            st.session_state.messages.append({"role": "assistant", "content": answer})
