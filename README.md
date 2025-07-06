#  QA Agent — AI-Powered Frontend Test Generator

QA Agent is a smart testing assistant designed to automatically generate and run end-to-end test cases for frontend applications. It can parse documentation, videos, or instructions, convert them into test scripts (e.g., Playwright), execute them, and report results — helping streamline the QA process with minimal manual effort.

---

##  Features

-  **AI-Powered Parsing**: Extracts test steps from how-to docs or videos
-  **Playwright Integration**: Generates and runs browser-based test scripts
-  **Markdown to Test**: Converts structured instructions into executable tests
-  **Result Logging**: Logs test execution results in a structured format
-  **Modular Architecture**: Easily extendable and customizable

---

## 📦 Tech Stack

| Category              | Tools Used                                                                 |
|-----------------------|----------------------------------------------------------------------------|
| **Language**          | Python 3.12+                                                               |
| **Test Frameworks**   | [Playwright (sync API)](https://playwright.dev/python/docs/intro), [Pytest](https://docs.pytest.org/) |
| **Test Runner Module**| `QuickTestRunner` – Custom test execution pipeline                         |
| **Browser Automation**| Microsoft Playwright (Sync API for Chromium, Firefox, WebKit)              |
| **Video Processing**  | [FFmpeg](https://ffmpeg.org/) – For recording/processing test session videos |
| **UI Layer (optional)**| [Streamlit](https://streamlit.io/) – To visualize and trigger tests       |
| **Version Control**   | Git & GitHub                                                               |
| **Environment**       | Python virtual environment (`.venv`)                                       |

