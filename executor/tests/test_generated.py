#!/usr/bin/env python3
"""
Quick Test Execution Tool for Recruter.ai
Fixed version with all imports and ready to run
"""

import re
import json
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QuickTestRunner:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.setup_directories()
        logger.info(f"🚀 Test Runner initialized with base URL: {base_url}")

    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            "executor/tests",
            "executor/results", 
            "executor/screenshots",
            "executor/videos",
            "executor/traces"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create conftest.py for pytest
        self.create_conftest()
        logger.info("✅ Test environment setup complete")

    def create_conftest(self):
        """Create conftest.py for pytest configuration"""
        conftest_content = '''import pytest
from playwright.sync_api import Page, Browser
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for all tests"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "executor/videos/",
        "record_video_size": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Take screenshot on test failure"""
    yield
    
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = Path(f"executor/screenshots/{request.node.name}_{timestamp}.png")
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            page.screenshot(path=str(screenshot_path))
            logger.info(f"📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
'''
        

        with open("executor/conftest.py", "w", encoding="utf-8") as f:
            f.write(conftest_content)

    def generate_code_from_step(self, step: str) -> List[str]:
        """Convert natural language step to Playwright code"""
        step = step.lower().strip()
        code_lines = []

        if "navigate to" in step or "go to" in step:
            url = self.base_url
            if "login" in step:
                url = f"{self.base_url}/login"
            elif "signup" in step or "sign up" in step:
                url = f"{self.base_url}/signup"
            code_lines.extend([
                f'page.goto("{url}")',
                'page.wait_for_load_state("networkidle")'
            ])

        elif "enter" in step or "fill" in step:
            if "email" in step:
                code_lines.extend([
                    'page.get_by_role("textbox", name="Enter your Email ID").fill("test@example.com")',
                    'page.wait_for_timeout(500)'  # Small delay for stability
                ])
            if "password" in step:
                code_lines.extend([
                    'page.get_by_role("textbox", name="Enter your Password").fill("TestPassword123")',
                    'page.wait_for_timeout(500)'
                ])
            if "name" in step:
                code_lines.extend([
                    'page.get_by_role("textbox", name="Enter your Name").fill("Test User")',
                    'page.wait_for_timeout(500)'
                ])

        elif "click" in step:
            if "login" in step:
                code_lines.append('page.get_by_role("button", name="Log in").click()')
            elif "sign up" in step:
                code_lines.append('page.get_by_role("button", name="Sign Up").click()')
            else:
                code_lines.append('page.get_by_role("button").first.click()')
            code_lines.append('page.wait_for_timeout(1000)')  # Wait after click

        elif "should see" in step or "expect" in step:
            if "dashboard" in step:
                code_lines.append(f'expect(page).to_have_url(re.compile(r".*/dashboard.*"))')
            elif "error" in step:
                code_lines.append('expect(page.locator("text=error")).to_be_visible()')
            elif "welcome" in step:
                code_lines.append('expect(page.locator("text=Welcome")).to_be_visible()')

        if not code_lines:
            code_lines.append(f'# TODO: Implement step - "{step}"')

        return code_lines

  