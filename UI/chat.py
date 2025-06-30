import streamlit as st
import requests

st.set_page_config(page_title="Alpha Assistant", page_icon="🤖", layout="centered")

# --- Inject ChatGPT-style CSS ---
st.markdown("""
<style>
/* MAIN BACKGROUND */
body {
    background: linear-gradient(to bottom right, #b3e5fc, #81d4fa);
    color: #212121;
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}

/* CENTERED TITLE */
.centered-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    padding-top: 1rem;
    color: #003366;
}
.subtext {
    text-align: center;
    font-size: 1.1rem;
    color: #333;
    margin-bottom: 1.5rem;
}

/* CHAT HISTORY */
.chat-history {
    padding: 1rem 2rem;
    max-height: 70vh;
    overflow-y: auto;
    margin-bottom: 1rem;
}

/* CHAT BUBBLES */
.stChatMessage.user {
    background-color: #e1f5fe;
    border-radius: 16px 16px 0 16px;
    padding: 12px 16px;
    margin: 0.6rem 0;
    max-width: 70%;
    margin-left: auto;
    color: #01579b;
    text-align: left;
    animation: slideRight 0.3s ease-in-out;
}

.stChatMessage.assistant {
    background-color: #ffffff;
    border-radius: 16px 16px 16px 0;
    padding: 12px 16px;
    margin: 0.6rem 0;
    max-width: 70%;
    margin-right: auto;
    color: #1a237e;
    text-align: left;
    animation: slideLeft 0.3s ease-in-out;
}

@keyframes slideRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

/* FIX INPUT BAR TO BOTTOM */
form {
    position: fixed;
    bottom: 10px;
    left: 0;
    width: 100%;
    background-color: rgba(255,255,255,0.9);
    padding: 10px 20px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.15);
    backdrop-filter: blur(5px);
    z-index: 10;
}

/* TEXT AREA STYLE */
textarea {
    width: 100%;
    background-color: #e1f5fe !important;
    border: 1px solid #81d4fa !important;
    color: #003344 !important;
    padding: 12px !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    resize: none !important;
    height: 80px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

/* BUTTON STYLE */
button[kind="primary"] {
    background-color: #039be5 !important;
    color: white !important;
    border-radius: 8px;
    margin-top: 10px;
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
button[kind="primary"]:hover {
    background-color: #0288d1 !important;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 2rem;
    font-size: 0.9rem;
    color: #555;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='centered-title'>🤖 Alpha Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Your smart complaint buddy ✨</div>", unsafe_allow_html=True)

# --- PHONE LOGIN ---
if "authenticated" not in st.session_state:
    phone = st.text_input("📞 Enter your phone number", max_chars=15, placeholder="e.g. +919876543210")
    if not phone:
        st.warning("Please enter your phone number to start chatting.")
        st.stop()
    st.session_state.authenticated = True
    st.session_state.phone = phone
    st.rerun()

# --- Chat Setup ---
request_id = st.session_state.phone
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hey! How can I help you today? 🤖"}
    ]

# --- Chat History ---
for msg in st.session_state.messages:
    avatar = "🧠" if msg["role"] == "bot" else "🙋"
    label = "AI" if msg["role"] == "bot" else "You"
    with st.chat_message("assistant" if msg["role"] == "bot" else "user"):
        st.markdown(f"{avatar} **{label}:** {msg['content']}")

# --- Chat Input Form (Sticky at Bottom Style) ---
with st.form(key="chat_form", clear_on_submit=True):
    prompt = st.text_area("💬", height=100, max_chars=1000, placeholder="Type your message...")
    submitted = st.form_submit_button("Send")

if submitted and prompt:
    if len(prompt) > 1000:
        st.warning("🚫 Message too long. Keep under 1000 characters.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"🙋 **You:** {prompt}")

    # --- Call Backend API ---
    with st.chat_message("assistant"):
        with st.spinner("🧠 AI is thinking..."):
            try:
                res = requests.post(
                    f"http://mcp-agents.ddns.net:8000/communicate/?request_id={request_id}",
                    json={"query": prompt},
                    timeout=100
                )
                reply = res.json().get("response", "No response received.")
            except Exception:
                reply = "⚠️ Error contacting the server."

            st.session_state.messages.append({"role": "bot", "content": reply})
            st.markdown(f"🧠 **AI:** {reply}")

# --- FOOTER ---
st.divider()
st.markdown("""
    <div class="footer">
        🚀 Powered by <strong>M</strong> | Made with <span style='color:red;'>❤️</span> by <strong>Vaidik Pandey</strong>
    </div>
""", unsafe_allow_html=True)
