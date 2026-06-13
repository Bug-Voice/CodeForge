import os
import sys
import time
import re
from dotenv import load_dotenv
from google import genai
from harbor_sdk import HarborClient

# --- GMAX STUDIOS BRAND COLORS ---
MINT = '\033[96m'         
FOREST_GREEN = '\033[32m' 
YELLOW = '\033[93m'       
RED = '\033[91m'          
RESET = '\033[0m'         

load_dotenv()
REQUIRED_KEYS = ["HARBOR_WORKSPACE_ID", "HARBOR_API_KEY", "GEMINI_API_KEY"]
missing_keys = [key for key in REQUIRED_KEYS if not os.getenv(key)]
if missing_keys:
    print(f"{RED}❌ Setup Error: Missing .env keys for: {', '.join(missing_keys)}{RESET}")
    sys.exit(1)

harbor = HarborClient(workspace_id=os.getenv("HARBOR_WORKSPACE_ID"), api_key=os.getenv("HARBOR_API_KEY"))
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemma-4-26b-a4b-it"

def generate_with_retry(prompt, agent_name):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return ai_client.models.generate_content(model=MODEL_NAME, contents=prompt).text
        except Exception as e:
            if "503" in str(e) or "429" in str(e):
                print(f"{YELLOW}   ⏳ [{agent_name}] Network busy. Retrying...{RESET}")
                time.sleep(5)
            else:
                raise e
    print(f"{RED}❌ Critical Failure: API timeout.{RESET}")
    sys.exit(1)

def run_universal_pipeline():
    if len(sys.argv) < 2:
        print(f"{RED}❌ Usage: python main.py <target_file.extension>{RESET}")
        sys.exit(1)
        
    target_file = sys.argv[1]
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            raw_code = f.read()
    except FileNotFoundError:
        print(f"{RED}❌ Error: Could not find '{target_file}'{RESET}")
        sys.exit(1)

    print(f"{MINT}🏗️ [1/3] Target acquired: {target_file}. Booting AI Dev Team...{RESET}")
    print("=" * 70)

    # ==========================================================
    # AGENT 1: THE ARCHITECT
    # ==========================================================
    print(f"{MINT}🤖 [Architect] Analyzing file context and refactoring layout...{RESET}")
    author_prompt = f"""
    You are an elite Software Architect. Analyze this raw code. 
    1. Define its core business context.
    2. Refactor variables and clean the layout for readability. DO NOT fix core logic bugs yet.
    
    CRITICAL: DO NOT TRANSLATE THE LANGUAGE. The output code block MUST be in the exact same programming language as the input. 
    Provide a 2-3 sentence technical explanation BEFORE outputting the markdown code block. Keep it conversational.
    EXCEPTION: If the code is already beautifully formatted, optimized, and named correctly, just provide a 1-sentence compliment and output the original unchanged code block.
    
    Raw Code:
    {raw_code}
    """
    author_version = generate_with_retry(author_prompt, "Architect")
    print(f"\n{MINT}--- ARCHITECT ---{RESET}\n{author_version.strip()}")
    
    time.sleep(10)

    # ==========================================================
    # AGENT 2: THE AUDITOR
    # ==========================================================
    print(f"\n{YELLOW}🔍 [Auditor] Red-teaming the code based on context...{RESET}")
    auditor_prompt = f"""
    You are a sharp Red Team Security QA. Review the Architect's refactor.
    Attack the code based on its specific context.
    
    CRITICAL INSTRUCTION: Explain the 'why' and 'how' of any exploit using simple, easy-to-understand language. Provide your explanation in 2 to 3 short paragraphs (where each paragraph is just 2-3 lines long) to give enough detail without being overwhelming. Speak directly to the engineering team. 
    EXCEPTION: If the code is perfectly secure and requires no fixes, do not write a long explanation. Just output a single short sentence confirming it is secure.
    
    Original: {raw_code}
    Architect Version: {author_version}
    """
    auditor_critique = generate_with_retry(auditor_prompt, "Auditor")
    print(f"\n{YELLOW}--- AUDITOR ---{RESET}\n{auditor_critique.strip()}")
    
    time.sleep(10)

    # ==========================================================
    # AGENT 3: THE GATEKEEPER
    # ==========================================================
    print(f"\n{FOREST_GREEN}⚖️ [Gatekeeper] Synthesizing final production patch...{RESET}")
    gatekeeper_prompt = f"""
    You are the Lead Engineer. Synthesize a production-ready patch based on the Auditor's critique.
    
    CRITICAL RULES:
    1. Keep the patched code in the EXACT SAME programming language as the Architect's version. 
    2. Write EXACTLY 2-3 short, clear sentences explaining the specific fix you applied. 
    3. Output the final patched code block.
    4. OPTIONAL: If a different language is better suited, leave a blank line after the code block and write one brief "Language Suggestion" sentence.
    EXCEPTION: If the Auditor confirms the code is already perfectly secure, DO NOT change the code. Provide a 1-sentence sign-off approving it for production, and output the original secure code block untouched.
    
    Architect Version: {author_version}
    Auditor Critique: {auditor_critique}
    """
    final_secure_patch = generate_with_retry(gatekeeper_prompt, "Gatekeeper")
    print(f"\n{FOREST_GREEN}--- LEAD ENGINEER ---{RESET}\n{final_secure_patch.strip()}")
    print("=" * 70)

    # ==========================================================
    # WORKFLOW RUNTIME: SECURE FILE EXPORT
    # ==========================================================
    # Safely handle any file extension (.js, .py, .cpp, etc)
    file_name, file_extension = os.path.splitext(target_file)
    secured_filename = f"{file_name}_SECURED{file_extension}"
    
    print(f"\n💾 [3/3] Exporting production-ready asset to: {secured_filename}...")
    
    # FIX: Dynamically build the markdown backticks so it doesn't break the UI parser
    md_marker = "`" * 3
    regex_pattern = rf'{md_marker}(?:[a-zA-Z0-9_-]+)?\n(.*?){md_marker}'
    
    # Use Regex to perfectly extract the raw code inside the markdown blocks
    match = re.search(regex_pattern, final_secure_patch, re.DOTALL)
    if match:
        clean_code_payload = match.group(1).strip()
    else:
        # Fallback if the AI forgets markdown formatting
        clean_code_payload = final_secure_patch.strip()
    
    with open(secured_filename, "w", encoding="utf-8") as f:
        f.write(clean_code_payload)

    print(f"{FOREST_GREEN}🏁 [System] Universal Code Review Completed Successfully.{RESET}")

if __name__ == "__main__":
    run_universal_pipeline()