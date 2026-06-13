# DevSentry: Autonomous AI Dev Pipeline

An autonomous code optimization, refactoring, and security auditing pipeline powered by Gemma & Gemini models. DevSentry runs code through an elite virtual development team—Architect, Auditor, Gatekeeper, and QA—to analyze, patch, and verify scripts.

## 🚀 How it Works

1. **Architect**: Analyzes the raw code and refactors it for readability and structure.
2. **Auditor (Red Team)**: Conducts a security critique on the refactored code.
3. **Gatekeeper (Lead Engineer)**: Synthesizes a patched version implementing the Auditor's feedback.
4. **QA**: Validates the syntax of the final code block before writing it to a `*_SECURED` file.

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set Up a Virtual Environment (Recommended)
On Windows:
```bash
py -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy the template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your Gemini API key:
   ```env
   GEMINI_API_KEY="your-actual-api-key-here"
   ```

---

## 💻 Running the Pipeline

To run the pipeline on any code file, use:
```bash
py main.py <path_to_target_file>
```

### Example:
```bash
py main.py example.js
```
This will produce a secured file named `example_SECURED.js` in the same directory.

---

## ⚡ Windows Convenience Launcher

For Windows users, a launcher batch file `run_app.bat` is available.
- **Option 1**: Drag and drop any source file (e.g., `example.js`) directly onto `run_app.bat`.
- **Option 2**: Double-click `run_app.bat` and type or paste the file path when prompted.
