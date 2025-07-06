import re
from pathlib import Path


def rule_based_code_generator(step: str) -> list:
    step = step.lower().strip()
    code_lines = []

    # Navigation
    if "navigate to" in step or "go to" in step:
        url = "https://recruter.ai"
        if "login" in step:
            url = "https://www.app.recruter.ai/"
        elif "signup" in step or "sign up" in step:
            url = "https://www.recruter.ai/onboarding/Signup"
        code_lines.append(f'page.goto("{url}")')

    # Fill fields
    elif "enter" in step or "fill" in step:
        if "email" in step or "username" in step:
            value = "user@example.com"
            selector = "input[name='email']" if "email" in step else "input[name='username']"
            code_lines.append(f'page.get_by_role("{selector}", "{value}")')
        if "password" in step:
            code_lines.append('page.get_by_role("input[name=\'password\']", "StrongPass123")')
        if "name" in step:
            code_lines.append('page.get_by_role("input[name=\'name\']", "Tanisha Bharvesh")')

    # Click buttons
    elif "click" in step:
        if "login" in step:
            code_lines.append('page.get_by_role("button:has-text(\'Log in\')")')
        elif "sign up" in step:
            code_lines.append('page.get_by_role("button:has-text(\'Sign Up\')")')
        else:
            code_lines.append('page.get_by_role("button")')

    # Expectations
    elif "should see" in step or "redirected" in step or "expect" in step:
        if "dashboard" in step:
            code_lines.append('expect(page).to_have_url("https://recruter.ai/dashboard")')
        elif "error message" in step:
            code_lines.append('expect(page.locator("text=Email already exists")).to_be_visible()')
        elif "welcome" in step:
            code_lines.append('expect(page.locator("text=Welcome")).to_be_visible()')

    # Unknown step
    else:
        code_lines.append(f'# TODO: Unrecognized step - "{step}"')
    # Return the generated code lines (as a list)
    return code_lines


def load_test_cases(markdown_file="D:\\QA AGENT\\assets\\generated_test_cases.md"):
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


def to_safe_func_name(name: str):
    return "test_" + re.sub(r'\W|^(?=\d)', '_', name.lower())


def generate_playwright_test_code(test_cases, output_dir="executor/tests"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "test_recruter_ai.py"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("import pytest\nfrom playwright.sync_api import Page, expect\n\n")

        for case in test_cases:
            func_name = to_safe_func_name(case["title"])
            f.write(f"def {func_name}(page: Page):\n")
            f.write(f"    '''{case['description']}'''\n")
            for step in case["steps"]:
                f.write(f"    # Step: {step}\n")
                code = rule_based_code_generator(step)
                f.write(f"    {code}\n")


            # for step in case["steps"]:
            #     f.write(f"  {step.strip()}\n")  # Directly write real Playwright code

            f.write(f"    # Expected: {case['expected']}\n\n\n")

    print(f" Test code written to: {file_path}")

if __name__ == "__main__":
    test_cases = load_test_cases()
    generate_playwright_test_code(test_cases)

