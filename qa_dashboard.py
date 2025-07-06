import streamlit as st
import xml.etree.ElementTree as ET
from pathlib import Path
import streamlit.components.v1 as components

def parse_junit_xml(xml_path):
    if not Path(xml_path).exists():
        return []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    test_cases = []
    for testcase in root.iter("testcase"):
        name = testcase.attrib.get("name")
        classname = testcase.attrib.get("classname")
        time = testcase.attrib.get("time")
        status = "Passed"

        failure = testcase.find("failure")
        if failure is not None:
            status = "Failed"
        
        test_cases.append({
            "Name": name,
            "Suite": classname,
            "Time (s)": time,
            "Status": status,
        })

    return test_cases

# Streamlit UI
st.set_page_config(page_title="QA Agent Test Dashboard", layout="wide")
st.title("🧪 QA Agent Test Report")

xml_path = "report/report.xml"
html_report = "report/report.html"

test_results = parse_junit_xml(xml_path)

if not test_results:
    st.warning("⚠️ No test report found. Run tests first.")
else:
    status_icons = {"Passed": "✅", "Failed": "❌"}

    st.subheader("📊 Summary Table")
    st.dataframe([
        {**tr, "Status": status_icons.get(tr["Status"], tr["Status"])}
        for tr in test_results
    ])

    st.subheader("📄 HTML Report Preview")

    if Path(html_report).exists():
        with open(html_report, "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=600, scrolling=True)

        st.markdown(f"[🧾 Click here to view full HTML report in browser](./{html_report})")
    else:
        st.warning("⚠️ HTML report not found. Please run the tests to generate it.")
