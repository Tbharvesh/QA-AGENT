import openai
from pathlib import Path
from openai import OpenAI
from pathlib import Path
import re

def load_test_cases(markdown_file="assets/generated_test_cases.md"):
    content = Path(markdown_file).read_text(encoding="utf-8")

    pattern = r"### Test Case: (.*?)\n- \*\*Description\*\*: (.*?)\n- \*\*Steps\*\*:([\s\S]*?)- \*\*Expected Result\*\*: (.*?)(?=\n###|\Z)"

    test_cases = []
    for match in re.finditer(pattern, content):
        title, description, steps_block, expected = match.groups()
        steps = re.findall(r"\d+\.\s+(.*)", steps_block.strip())
        test_cases.append({
            "title": title.strip(),
            "description": description.strip(),
            "steps": steps,
            "expected": expected.strip()
        })

    return test_cases

# Load your OpenAI API key (use dotenv for security if needed)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def load_transcript(path="assets/transcription.txt"):
    return Path(path).read_text(encoding="utf-8")

def generate_test_cases(transcript: str):
    system_prompt = """
You are QAgenie — a calm, thorough AI QA assistant.
Your mission is to ensure flawless user experiences on Recruter.ai.
You carefully read help documents and watch training videos to understand user flows, edge cases, and expected UI behaviors.
You automatically generate complete, accurate, and maintainable frontend test cases in Playwright.
You run tests systematically, capture results, and summarize findings clearly with actionable insights.
You never skip edge cases and always consider accessibility, cross-browser compatibility, and user error handling.
You escalate ambiguous flows with clear context for clarification rather than guessing.
"""

    user_prompt = f"""
Based on the following transcript from a Recruter.ai walkthrough video, generate detailed frontend test cases.

Transcript:
\"\"\"
{transcript}
\"\"\"

Include:
- Core user flows (e.g., signup, login, dashboard)
- Edge cases (e.g., empty inputs, invalid formats, network failures)
- Accessibility and performance considerations

Output Format (Markdown):
### Test Case: [Title]
- **Description**: ...
- **Steps**: ...
- **Expected Result**: ...
"""

    response = client.chat.completions.create(
         model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    transcript = load_transcript()
    print("Transcript loaded. Generating test cases...")

    test_cases = generate_test_cases(transcript)

    output_path = Path("assets/generated_test_cases.md")
    output_path.write_text(test_cases, encoding="utf-8") 

    print(f"Test cases saved to: {output_path}")

