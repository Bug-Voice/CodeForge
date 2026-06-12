import streamlit as st
import os
import time
import re
from dotenv import load_dotenv
from google import genai

# Load environment variables securely
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and "your_api_key" not in API_KEY:
    ai_client = genai.Client(api_key=API_KEY)
else:
    ai_client = None

# Using your specific Gemma model
MODEL_NAME = "models/gemma-4-26b-a4b-it"

def generate_with_retry(prompt, agent_name):
    if not ai_client:
        return f"⚠️ Error: [{agent_name}] API Key missing."
    
    last_error = "Unknown Error"
    
    for attempt in range(3):
        try:
            response = ai_client.models.generate_content(
                model=MODEL_NAME, 
                contents=prompt
            )
            if not response.text:
                 return f"⚠️ [{agent_name}] Google API blocked the response (likely a safety filter on the prompt)."
            return response.text
            
        except Exception as e:
            last_error = str(e)  
            time.sleep(2)
            
    return f"❌ [{agent_name}] Failed after 3 attempts. Error: {last_error}"

def extract_code(text):
    md_marker = "`" * 3
    regex = rf'{md_marker}(?:[a-zA-Z0-9_-]+)?\n(.*?){md_marker}'
    match = re.search(regex, text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

st.set_page_config(page_title="CodeForge AI", layout="wide")
st.title("🏗️ CodeForge AI Platform")

with st.sidebar:
    st.header("⚡ System Status")
    st.success("API: Connected") if ai_client else st.error("API: Disconnected")

tab1, tab2, tab3 = st.tabs(["🔍 Code Reviewer", "📚 DSA Mentor", "🎯 Edge-Case Hunter"])

# --- TAB 1: CODE REVIEWER ---
with tab1:
    st.header("🕵️‍♂️ Autonomous Code Review Pipeline")
    
    input_method = st.radio("Input Method:", ["Upload File", "Paste Code"], horizontal=True)
    raw_code = ""
    target_language = "auto"
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload code file")
        if uploaded_file:
            raw_code = uploaded_file.read().decode("utf-8")
            target_language = uploaded_file.name.split(".")[-1]
    else:
        # Auto-Detect restored as the default option
        lang_choice = st.selectbox("Language:", ["Auto-Detect via AI", "cpp", "java", "py", "js", "ts", "c"])
        raw_code = st.text_area("Paste code:", height=200)
        target_language = "auto" if lang_choice == "Auto-Detect via AI" else lang_choice

    if st.button("🚀 Execute Pipeline", type="primary") and raw_code:
        
        # Detect language via AI if Auto was selected
        if target_language == "auto":
            with st.spinner("🧠 Detecting language structure..."):
                detect_prompt = f"Identify only the programming language name of this code snippet. Output exactly the language string name, lowercase, with nothing else: \n\n{raw_code}"
                target_language = generate_with_retry(detect_prompt, "Language Detector").strip().lower()
            st.info(f"✨ Language classified as: **{target_language}**")

        status_box = st.status("🏗️ Spinning up AI Matrix...", expanded=True)
        
        # AGENT 1: ARCHITECT
        status_box.write("1️⃣ Processing through [Architect]...")
        architect_prompt = f"""
        You are an elite Software Architect. Analyze this raw code. 
        1. Define its core business context.
        2. Refactor variables and clean the layout for readability. DO NOT fix core logic bugs yet.
        
        CRITICAL: DO NOT TRANSLATE THE LANGUAGE. The output code block MUST be in the exact same programming language as the input. 
        Provide a 2-3 sentence technical explanation BEFORE outputting the markdown code block. Keep it conversational.
        EXCEPTION: If the code is already beautifully formatted, optimized, and named correctly, just provide a 1-sentence compliment and output the original unchanged code block.
        
        Raw Code ({target_language}):
        {raw_code}
        """
        author_version = generate_with_retry(architect_prompt, "Architect")
        
        # AGENT 2: AUDITOR
        status_box.write("2️⃣ Running threat scan via [Auditor]...")
        auditor_prompt = f"""
        You are a sharp Red Team Security QA. Review the Architect's refactor.
        Attack the code based on its specific context.
        
        CRITICAL INSTRUCTION: Explain the 'why' and 'how' of any exploit using simple, easy-to-understand language. Provide your explanation in 2 to 3 short paragraphs (where each paragraph is just 2-3 lines long) to give enough detail without being overwhelming. Speak directly to the engineering team. 
        EXCEPTION: If the code follows industry-standard secure practices (e.g., uses parameterized queries, basic password hashing, or strict type conversions), DO NOT nitpick for highly advanced theoretical attacks. Just output a single short sentence confirming the code is secure and production-ready.
        
        Original: {raw_code}
        Architect Version: {author_version}
        """
        auditor_critique = generate_with_retry(auditor_prompt, "Auditor")
        
        # AGENT 3 & 4: REPAIR LOOP
        max_loops = 3
        feedback = ""
        clean_patched_code = ""
        
        for loop in range(1, max_loops + 1):
            status_box.write(f"⚖️ [Gatekeeper] Repair Loop {loop}/{max_loops}...")
            gatekeeper_prompt = f"""
            You are the Lead Engineer. Synthesize a production-ready patch based on the Auditor's critique.
            
            CRITICAL RULES:
            1. If the Auditor confirms the code is already secure/production-ready, DO NOT change a single character. Return the EXACT code provided by the Architect.
            2. Only make changes if the Auditor identifies a specific security vulnerability or bug.
            3. Keep the patched code in the EXACT SAME programming language as the Architect's version. 
            4. Write EXACTLY 2-3 short, clear sentences explaining the specific fix you applied (if no fix, state 'No changes required').
            5. Output the final patched code block.
            
            {feedback}
            Architect Version: {author_version}
            Auditor Critique: {auditor_critique}
            """
            
            gatekeeper_output = generate_with_retry(gatekeeper_prompt, "Gatekeeper")
            clean_patched_code = extract_code(gatekeeper_output)
            
            # AGENT 4: QA VALIDATOR
            status_box.write(f"🧪 [QA Tester] Validating syntax...")
            qa_prompt = f"Does the following code have any major syntax errors that would prevent it from compiling? If it is valid code, output ONLY 'SUCCESS'. If it has a critical syntax error, output 'ERROR'.\nCode:\n{clean_patched_code}"
            qa_result = generate_with_retry(qa_prompt, "QA").strip()
            
            if "SUCCESS" in qa_result:
                status_box.write("✅ Syntax Validated!")
                break
            else:
                feedback = "The code has syntax errors. Please fix."
                status_box.write("⚠️ Syntax error detected. Retrying...")

        status_box.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        st.markdown("---")
        
        # --- UI CHANGE: CODE COMPARISON MOVED TO TOP ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("❌ Original Input")
            st.code(raw_code, language=target_language)
        with col2:
            st.subheader("🛡️ Secured & Optimized Patch")
            st.code(clean_patched_code, language=target_language)
            
        st.markdown("---")
        
        # --- UI CHANGE: AGENT DIAGNOSTICS MOVED TO BOTTOM ---
        st.subheader("🤖 AI Agent Diagnostics")
        st.info(f"**🏗️ Architect's Analysis:**\n\n{author_version}")
        st.warning(f"**🛡️ Auditor's Threat Scan:**\n\n{auditor_critique}")
        st.success(f"**⚖️ Gatekeeper's Patch Notes:**\n\n{gatekeeper_output}")


# --- TAB 2: DSA MENTOR ---
with tab2:
    st.header("📚 DSA Interactive Mentor")
    st.write("Paste a LeetCode/Codeforces link OR the raw problem text. The mentor will break down the concept, build a brute-force approach, and guide you to the optimal solution.")
    
    col_dsa1, col_dsa2 = st.columns([3, 1])
    with col_dsa1:
        problem_input = st.text_area("Paste Problem Link OR Statement here:", height=150, placeholder="e.g., https://leetcode.com/problems/valid-parentheses/ ...")
    with col_dsa2:
        dsa_lang = st.selectbox("Target Language:", ["cpp", "python", "java", "js"])
        dsa_submit = st.button("🧠 Analyze Problem", use_container_width=True, type="primary")

    if dsa_submit and problem_input:
        with st.spinner("Analyzing problem constraints and optimal data structures..."):
            dsa_prompt = f"""
            You are an elite Data Structures and Algorithms Mentor. A student has asked for help with this problem. 
            If the input below is a URL, use your internal knowledge to retrieve the exact problem details. If it is raw text, analyze the text directly.
            
            Input:
            {problem_input}
            
            Do not just give the final answer. Break it down into three distinct sections using Markdown:
            1. **The Core Concept:** Explain the underlying pattern (e.g., Sliding Window, DP, Graph Traversal) in plain English.
            2. **Brute Force Approach:** Explain the naive solution, its Time/Space complexity, and provide a short snippet in {dsa_lang}.
            3. **Optimized Approach:** Explain how to optimize it, the new Time/Space complexity, and provide the clean, production-ready code in {dsa_lang}.
            """
            dsa_response = generate_with_retry(dsa_prompt, "DSA Mentor")
            
            st.markdown("---")
            st.markdown(dsa_response)

# --- TAB 3: EDGE-CASE HUNTER ---
with tab3:
    st.header("🎯 Edge-Case Hunter")
    st.write("Think your code is perfect? Paste it here. The Hunter will attempt to find edge cases, memory leaks, or execution limits that will break your logic.")
    
    hunter_code = st.text_area("Paste your solution code here to test its resilience:", height=200)
    
    if st.button("🏹 Hunt for Vulnerabilities", type="primary"):
        if hunter_code:
            with st.spinner("Simulating edge cases and stress testing boundaries..."):
                hunter_prompt = f"""
                You are a ruthless Red Team software tester. Your goal is to break the logic of the provided code.
                Analyze the code and generate 3 severe edge cases that the developer likely missed (e.g., null inputs, extreme integer overflows, empty arrays, negative values, concurrency limits).
                
                Format your response as:
                * **Vulnerability 1:** [Description] -> Example Input: [Input]
                * **Vulnerability 2:** [Description] -> Example Input: [Input]
                * **Vulnerability 3:** [Description] -> Example Input: [Input]
                
                Code to attack:
                {hunter_code}
                """
                hunter_response = generate_with_retry(hunter_prompt, "Edge-Case Hunter")
                
                st.markdown("---")
                st.error("### ⚠️ Vulnerabilities Detected")
                st.markdown(hunter_response)
        else:
            st.warning("Please paste some code for the Hunter to attack.")