import streamlit as st
from openai import OpenAI

# ==========================================
# 1. 页面配置 (专为长辈适配的极致 App 质感)
# ==========================================
st.set_page_config(
    page_title="爹妈专用小 AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 注入超级字体 CSS
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #F0F8FF; }
    header, footer, .stDeployButton { visibility: hidden !important; height: 0 !important; }
    .stChatFloatingInputContainer { bottom: 20px; }

    [data-testid="stChatMessage"] p, [data-testid="stChatMessageAssistant"] p {
        color: #333333 !important;
        font-size: 24px !important; 
        line-height: 1.8 !important; 
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    }

    [data-testid="stChatMessageUser"] {
        background-color: #DCF8C6 !important;
        border-radius: 20px 20px 0px 20px !important;
        padding: 20px !important; 
        margin-left: 10% !important; 
        margin-bottom: 30px !important; 
        border: 1px solid #C5E1A5;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    [data-testid="stChatMessageAssistant"] {
        background-color: white !important;
        border-radius: 20px 20px 20px 0px !important;
        padding: 20px !important;
        margin-right: 10% !important;
        margin-bottom: 30px !important; 
        border: 1px solid #E0E0E0;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }

    .native-app-header {
        background-color: white;
        padding: 15px;
        text-align: center;
        border-bottom: 1px solid #E0E0E0;
        position: fixed;
        top: 0; left: 0; width: 100%;
        z-index: 1000;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .native-app-title {
        color: #1E88E5 !important;
        font-size: 26px !important;
        font-weight: bold;
        margin: 0;
    }
    .native-app-subtitle {
        color: #777; font-size: 18px; margin: 5px 0 0 0;
    }

    .stChat { padding-top: 100px; padding-bottom: 80px; }
    .stChatInputContainer textarea { font-size: 22px !important; line-height: 1.6 !important; }

    .quick-guide-col .stButton > button {
        background-color: white; color: #555;
        border: 1px solid #E0E0E0; border-radius: 12px;
        font-size: 18px; margin-bottom: 10px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
    }
    .quick-guide-col .stButton > button:hover {
        background-color: #F0F8FF; border-color: #1E88E5; color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 虚拟 App 顶部栏
# ==========================================
st.markdown("""
<div class='native-app-header'>
    <p class='native-app-title'>🤖 爹妈专用小 AI</p>
    <p class='native-app-subtitle'>随时随地，陪您聊天，帮您解忧</p>
</div>
<br>
""", unsafe_allow_html=True)

# ==========================================
# 4. 接入 DeepSeek AI
# ==========================================
DEEPSEEK_API_KEY = "sk-f7ca32665ab74a6a94feb2314e8f3c30"

try:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
except Exception as e:
    st.error("AI 客户端初始化失败，请检查设置。")

# ==========================================
# 5. 系统状态管理
# ==========================================
if "show_guide_buttons" not in st.session_state:
    st.session_state.show_guide_buttons = True

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "system",
        "content": "你是一个专门为中国长辈设计的贴心AI助手。你的回答必须极其通俗易懂、语气温和、耐心，像家人一样聊。绝对不要使用任何表情符号，绝对避免任何英文术语。字体要大，语气要暖。请保持回答简短、干净，分步骤回答。"
    })

if len(st.session_state.messages) == 1:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "爸/妈，您好！我是您的专属智能小助手。今天有什么新鲜事想和我说说，或者需要我帮忙查查、写点什么的吗？请在下方直接告诉我。"
    })

# ==========================================
# 6. 界面渲染逻辑
# ==========================================
if st.session_state.show_guide_buttons and len(st.session_state.messages) <= 2:
    st.markdown("<h3>💡 您可以试试问我这些：</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>直接点击按钮，我也能回答您哦！</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍳 推荐个简单的菜谱", use_container_width=True):
            st.session_state.show_guide_buttons = False
            st.session_state.quick_prompt = "给我推荐一个简单、食材好买的适合长辈吃的土豆丝菜谱，步骤不要太多。"
    with col2:
        if st.button("🌦️ 查查天气", use_container_width=True):
            st.session_state.show_guide_buttons = False
            st.session_state.quick_prompt = "帮我查一下近期的天气，然后用长辈口吻提醒我出门注意事项。"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✉️ 写写新年祝福语", use_container_width=True):
            st.session_state.show_guide_buttons = False
            st.session_state.quick_prompt = "给我的家人写一段发在微信群里的新年祝福语，要带点正能量，字数不要太多。"
    with col4:
        if st.button("📖 陪我聊聊天", use_container_width=True):
            st.session_state.show_guide_buttons = False
            st.session_state.quick_prompt = "最近我都不知道该做什么好，你能陪我聊聊天，给我些日常生活的建议吗？"
    st.divider()

# 显示聊天历史 (彻底删除了 avatar 参数，使用原生安全图标)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("在这里写下您想说的话...")

if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    # 彻底删除了 avatar 参数
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("您稍等，我想想..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=st.session_state.messages,
                    stream=False
                )
                ai_reply = response.choices[0].message.content
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"抱歉，网络似乎开了个小差，请稍后再试一次。代码说：{e}")