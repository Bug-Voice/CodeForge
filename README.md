# 🏗️ CodeForge AI Platform

CodeForge AI Platform is an advanced, multi-agent AI assistant designed to accelerate software development workflows. Powered by Google's Gemini/Gemma models, it provides autonomous code review, interactive DSA mentoring, and rigorous edge-case vulnerability testing.

## 🚀 Features

### 1. 🕵️‍♂️ Autonomous Code Review Pipeline
* **Architect Agent:** Analyzes business context, refactors variables, and improves layout readability.
* **Auditor Agent:** Scans code for security vulnerabilities, explaining potential exploits in clear, direct language.
* **Gatekeeper & QA Tester:** Executes a repair loop to fix identified issues and validates syntax before displaying the final output.

### 2. 📚 DSA Interactive Mentor
* Solves coding challenges by pasting a LeetCode/Codeforces link or raw text.
* Breaks down the problem into three stages: Core Concepts, Brute Force implementation, and Optimized solutions with complexity analysis.

### 3. 🎯 Edge-Case Hunter
* Stress-tests your code by identifying three severe hidden vulnerabilities (empty arrays, boundary limits, null pointers, integer overflows).

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Install Dependencies
Set up your virtual environment and install the required libraries:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Configure API Key
1. Duplicate `.env.example` and rename it to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and replace `your_api_key_here` with your actual Gemini API Key:
   ```env
   GEMINI_API_KEY="your-actual-api-key"
   ```

---

## 🖥️ Running the Application

### Method 1: Double-Click Launcher (Recommended for Windows)
Simply double-click the `run_app.bat` file in the root directory. It will automatically detect your virtual environment and start the app.

### Method 2: Command Line
Activate your virtual environment and run Streamlit:
```bash
venv\Scripts\activate
streamlit run app.py
```

---

## 📦 How to Upload to GitHub (Safely)

To publish this project to GitHub without leaking your private API keys or uploading heavy dependency folders:

1. **Verify your `.gitignore`:**
   Ensure `.env` and `venv/` are listed in your `.gitignore` file so they are never tracked by Git.
2. **Initialize Git Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: CodeForge AI Platform"
   ```
3. **Publish to GitHub:**
   * Create a new repository on [GitHub](https://github.com).
   * Run the following commands (replace with your repository link):
     ```bash
     git branch -M main
     git remote add origin https://github.com/your-username/your-repo-name.git
     git push -u origin main
     ```
