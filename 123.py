import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. 配置区域 ---
# 在此处填入你的 API KEY
API_KEY = "你的_GEMINI_API_KEY_粘贴在这里"
genai.configure(api_key=API_KEY)

# 初始化模型
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. 页面设置 ---
st.set_page_config(page_title="手机智能农技站", page_icon="🌾")

# 调整字体大小的简单样式
st.markdown("""
    <style>
    .main { font-size: 1.2rem; }
    .stButton>button { width: 100%; height: 3em; font-size: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 农作物病虫害专家")
st.write("农民伯伯您好！请拍下生病的叶片，我会帮您看病。")

# --- 3. 图片处理逻辑 ---
uploaded_file = st.file_uploader("点击下方按钮【拍照】或【选择图片】", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 读取图片
    raw_image = Image.open(uploaded_file)

    # 【核心优化】压缩图片以节省流量和提高识别速度
    # 限制最大宽度为 800px，质量 85%
    buffer = io.BytesIO()
    raw_image.thumbnail((800, 800))
    raw_image.save(buffer, format="JPEG", quality=85)
    compressed_image = Image.open(buffer)

    # 显示预览图
    st.image(compressed_image, caption="您拍的照片", use_container_width=True)

    # 诊断按钮
    if st.button("开始 AI 诊断"):
        with st.spinner("专家正在看诊，请稍候..."):
            try:
                # 提示词（针对农业场景优化）
                prompt = [
                    "你是一位接地气的农业专家。请分析图片并用通俗易懂的中文回答：",
                    "1. 这是什么植物？",
                    "2. 它得了什么病，或者是什么虫子害的？",
                    "3. 简单说一下防治办法（比如用什么药，或者怎么处理）。",
                    "如果图片不清晰或不是植物，请客气地提醒用户重新拍摄。"
                ]

                # 调用 API
                response = model.generate_content([*prompt, compressed_image])

                # 显示结果
                st.success("诊断报告如下：")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                st.info("提示：农药使用请严格遵守说明书，或咨询当地农资店。")

            except Exception as e:
                st.error(f"发生错误：{str(e)}")
                st.write("请检查网络链接或 API Key 是否正确。")

# --- 4. 底部说明 ---
st.caption("技术支持：Gemini 1.5 Flash 低成本助农方案")