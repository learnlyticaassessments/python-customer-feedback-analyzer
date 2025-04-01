import importlib.util
import datetime
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    FeedbackAnalyzer = student_module.FeedbackAnalyzer
    analyzer = FeedbackAnalyzer()

    report_lines = [f"\n=== Feedback Analyzer Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==="]

    test_cases = [
        {
            "desc": "Clean and tokenize input",
            "func": "clean_and_tokenize",
            "input": "Excellent service and SUPPORT!",
            "expected": ['excellent', 'service', 'and', 'support']
        },
        {
            "desc": "Word frequency count",
            "func": "compute_frequency",
            "input": ['good', 'service', 'good', 'team'],
            "expected": {'good': 2, 'service': 1, 'team': 1}
        },
        {
            "desc": "Most frequent word",
            "func": "get_most_frequent",
            "input": {'great': 3, 'good': 2, 'okay': 1},
            "expected": ('great', 3)
        },
        {
            "desc": "Clean sentence with punctuation",
            "func": "clean_and_tokenize",
            "input": "Amazing SERVICE. amazing support!!!",
            "expected": ['amazing', 'service', 'amazing', 'support']
        },
        {
            "desc": "Empty frequency dict",
            "func": "get_most_frequent",
            "input": {},
            "expected": "No words to analyze."
        }
    ]

    edge_cases = [
        {"func": "clean_and_tokenize", "desc": "Function contains only pass"},
        {"func": "compute_frequency", "desc": "Function contains only pass"},
        {"func": "get_most_frequent", "desc": "Function contains only pass"},
        {"func": "clean_and_tokenize", "desc": "Hardcoded token list", "expected": ['excellent', 'service', 'and', 'support'], "input": "Excellent service and SUPPORT!"},
        {"func": "compute_frequency", "desc": "Hardcoded frequency", "expected": {'good': 2, 'service': 1, 'team': 1}, "input": ['good', 'service', 'good', 'team']},
        {"func": "get_most_frequent", "desc": "Hardcoded top word", "expected": ('great', 3), "input": {'great': 3, 'good': 2, 'okay': 1}},
    ]

    for i, case in enumerate(test_cases, 1):
        try:
            method = getattr(analyzer, case["func"])
            edge_case_failed = False
            failing_reason = None

            for edge in edge_cases:
                if edge["func"] != case["func"]:
                    continue

                src = inspect.getsource(getattr(FeedbackAnalyzer, edge["func"])).replace(" ", "").replace("\n", "").lower()

                if "pass" in src and len(src) < 80:
                    edge_case_failed = True
                    failing_reason = "Function contains only 'pass'"
                    break

                if "input" in edge:
                    result = getattr(analyzer, edge["func"])(edge["input"])
                    if result == edge["expected"]:
                        # Check for hardcoded return lines
                        if edge["func"] == "clean_and_tokenize" and "return['excellent','service','and','support']" in src:
                            edge_case_failed = True
                            failing_reason = "Hardcoded return: fixed token list"
                            break
                        if edge["func"] == "compute_frequency" and "return{'good':2,'service':1,'team':1}" in src:
                            edge_case_failed = True
                            failing_reason = "Hardcoded return: fixed frequency dict"
                            break
                        if edge["func"] == "get_most_frequent" and "return('great',3)" in src:
                            edge_case_failed = True
                            failing_reason = "Hardcoded return: fixed most frequent word"
                            break
                        if all(kw not in src for kw in ["split", "translate", "punctuation", "for", "in", "max", "key"]):
                            edge_case_failed = True
                            failing_reason = edge["desc"]
                            break

            result = method(case["input"])
            expected = case["expected"]

            # If edge case failed, fail the test
            if edge_case_failed:
                status = "❌"
            else:
                status = "✅" if result == expected or (expected == "No words to analyze." and result is None) else "❌"

            if status == "✅":
                msg = f"{status} Test Case {i} Passed: {case['desc']} | Actual={result}"
            else:
                msg = f"{status} Test Case {i} Failed: {case['desc']} | Expected={expected} | Actual={result}"

            if edge_case_failed:
                msg += f" | Reason: Edge case validation failed - {failing_reason}"

            print(msg)
            report_lines.append(msg)

        except Exception as e:
            msg = f"❌ Test Case {i} Crashed: {case['desc']} | Error={str(e)}"
            print(msg)
            report_lines.append(msg)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
