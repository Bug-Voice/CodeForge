import os
import sys
import time
import re
import subprocess
from dotenv import load_dotenv
from google import genai

# --- GMAX STUDIOS BRAND COLORS ---
MINT = '\033[96m'         
FOREST_GREEN = '\033[32m' 
YELLOW = '\033[93m'       
RED = '\033[91m'          
RESET = '\033[0m'         
MAGENTA = '\033[95m'      

load_dotenv()
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemma-4-26b-a4b-it"

def generate_with_retry(prompt, agent_name):
    for attempt in range(5):
        try:
            return ai_client.models.generate_content(model=MODEL_NAME, contents=prompt).text
        except Exception:
            time.sleep(5)
    sys.exit(1)

def extract_code(text):
    md_marker = "`" * 3
    regex = rf'{md_marker}(?:[a-zA-Z0-9_-]+)?\n(.*?){md_marker}'
    match = re.search(regex, text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def run_autonomous_pipeline():
    if len(sys.argv) < 2:
        print(f"{RED}❌ Usage: python main.py <target_file>{RESET}")
        sys.exit(1)

    target_file = sys.argv[1]
    file_name, ext = os.path.splitext(target_file)
    with open(target_file, "r", encoding="utf-8") as f: raw_code = f.read()

    print(f"{MINT}🏗️ [1/3] Target acquired: {target_file}. Booting AI Dev Team...{RESET}")

    # --- AGENT 1: THE ARCHITECT ---
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

    # --- AGENT 2: THE AUDITOR ---
    auditor_prompt = f"""
    You are a sharp Red Team Security QA. Review the Architect's refactor.
    Attack the code based on its specific context.
    
    CRITICAL INSTRUCTION: Explain the 'why' and 'how' of any exploit using simple, easy-to-understand language. Provide your explanation in 2 to 3 short paragraphs (where each paragraph is just 2-3 lines long) to give enough detail without being overwhelming. Speak directly to the engineering team. 
    EXCEPTION: If the code follows industry-standard secure practices (e.g., uses parameterized queries, basic password hashing, or strict type conversions), DO NOT nitpick for highly advanced theoretical attacks (like timing attacks). Just output a single short sentence confirming the code is secure and production-ready.
    
    Original: {raw_code}
    Architect Version: {author_version}
    """
    auditor_critique = generate_with_retry(auditor_prompt, "Auditor")
    print(f"\n{YELLOW}--- AUDITOR ---{RESET}\n{auditor_critique.strip()}")

    # --- AGENT 3 & 4: AUTONOMOUS REPAIR LOOP ---
    max_loops = 3
    feedback = ""
    
    for loop in range(1, max_loops + 1):
        print(f"\n{MAGENTA}⚖️ [Gatekeeper] Synthesis/Repair Loop {loop}/{max_loops}...{RESET}")
        
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
        
        final_patch = generate_with_retry(gatekeeper_prompt, "Gatekeeper")
        clean_code = extract_code(final_patch)
        
        # --- AGENT 4: EXTREMELY LENIENT SYNTAX VALIDATOR ---
        print(f"{MAGENTA}🧪 [Agent 4: QA] Running lightweight syntax check...{RESET}")
        
        # This prompt is now super simple. If it's not broken, it's 'SUCCESS'.
        qa_prompt = f"Does the following code have any major syntax errors that would prevent it from compiling? If it is valid code, output ONLY 'SUCCESS'. If it has a critical syntax error, output 'ERROR'.\nCode:\n{clean_code}"
        
        result_text = generate_with_retry(qa_prompt, "QA").strip()
        
        if "SUCCESS" in result_text:
            print(f"{FOREST_GREEN}✅ Code is syntactically valid!{RESET}")
            with open(f"{file_name}_SECURED{ext}", "w", encoding="utf-8") as f: f.write(clean_code)
            # Display only the final code
            print(f"\n{clean_code}")
            return
        else:
            feedback = "The code has syntax errors. Please fix."
            print(f"{RED}⚠️ Syntax error detected. Feedback sent to Gatekeeper.{RESET}")

if __name__ == "__main__":
    run_autonomous_pipeline()