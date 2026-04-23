from flask import Flask, abort, render_template, request

from data.profile import profile, projects


app = Flask(__name__)


REVIEW_SAMPLES = {
    "factorial": {
        "label": "Factorial Function",
        "prompt": "Create a Python function that returns the factorial of a non-negative integer.",
        "code": """def factorial(n):
    result = 0
    for i in range(1, n):
        result *= i
    return result""",
        "issues": [
            {
                "title": "Incorrect initialization",
                "detail": "The accumulator starts at 0, so every multiplication keeps the result at 0.",
                "category": "correctness",
            },
            {
                "title": "Loop excludes the final multiplier",
                "detail": "The range stops before n, so the logic misses the last required multiplication.",
                "category": "instruction_following",
            },
            {
                "title": "No edge-case handling",
                "detail": "The function does not guard negative values or explicitly validate the input.",
                "category": "quality",
            },
        ],
        "positive_notes": [
            "The function name is clear and readable.",
            "The implementation is compact and easy to inspect.",
        ],
    },
    "emails": {
        "label": "Email Validator",
        "prompt": "Write a Python function to validate that an email contains '@' and a domain suffix.",
        "code": """def is_valid_email(value):
    if "@" not in value:
        return False
    local, domain = value.split("@")
    return "." in local""",
        "issues": [
            {
                "title": "Checks dot in the wrong segment",
                "detail": "The validation looks for '.' in the local part instead of the domain.",
                "category": "correctness",
            },
            {
                "title": "Unsafe split behavior",
                "detail": "Using split without constraining the result can break when the string contains more than one '@'.",
                "category": "quality",
            },
        ],
        "positive_notes": [
            "The first guard clause catches a common invalid input quickly.",
            "The function returns booleans consistently.",
        ],
    },
}

CHALLENGE_LIBRARY = {
    "arrays": {
        "title": "Sliding Window Alert",
        "brief": "Analyze a list of values and detect the first subarray that exceeds a threshold.",
        "constraints": [
            "Handle empty lists safely",
            "Support repeated values",
            "Return the starting index or -1 if not found",
        ],
        "test_cases": [
            "[3, 1, 4, 1, 5], window=3, threshold=8 -> 0",
            "[1, 1, 1, 1], window=2, threshold=5 -> -1",
        ],
    },
    "strings": {
        "title": "Instruction-Following Formatter",
        "brief": "Normalize a sentence while preserving word order and removing duplicated whitespace.",
        "constraints": [
            "Keep punctuation untouched",
            "Avoid regex-only solutions",
            "Return an empty string if the input is empty",
        ],
        "test_cases": [
            "'hello   world' -> 'hello world'",
            "' keep   punctuation! ' -> 'keep punctuation!'",
        ],
    },
    "apis": {
        "title": "Async Retry Planner",
        "brief": "Design a function that schedules retries for failed API calls using exponential backoff.",
        "constraints": [
            "Cap the retry delay",
            "Reject invalid retry counts",
            "Return a list of retry timestamps or offsets",
        ],
        "test_cases": [
            "retries=3, base=2 -> [2, 4, 8]",
            "retries=0, base=2 -> []",
        ],
    },
}

REMOTE_TASKS = [
    {
        "title": "Review AI-generated Python solution",
        "status": "In Review",
        "priority": "High",
        "owner": "Gabriel",
    },
    {
        "title": "Draft challenge prompt with edge cases",
        "status": "Planned",
        "priority": "Medium",
        "owner": "Gabriel",
    },
    {
        "title": "Organize async notes for weekly handoff",
        "status": "Done",
        "priority": "Low",
        "owner": "Gabriel",
    },
    {
        "title": "Validate scoring rubric against guidelines",
        "status": "In Review",
        "priority": "High",
        "owner": "Gabriel",
    },
]

REMOTE_UPDATES = [
    "Reviewed two generated solutions and documented the main correctness issues.",
    "Prepared a challenge outline with instructions, expected outputs, and edge cases.",
    "Consolidated async notes to make handoff easier for distributed collaboration.",
]

BUG_REPORTS = [
    {
        "title": "Login button freezes on slow network",
        "severity": "High",
        "impact": "Users cannot complete sign-in reliably.",
        "status": "Needs Fix",
    },
    {
        "title": "Profile image fails on first load",
        "severity": "Medium",
        "impact": "Visual regression with fallback missing.",
        "status": "Investigating",
    },
    {
        "title": "Dashboard counter off by one",
        "severity": "Low",
        "impact": "Minor reporting mismatch in summary card.",
        "status": "Backlog",
    },
]

API_PAYLOADS = {
    "orders": {
        "label": "Orders Endpoint",
        "payload": """{
  "status": 200,
  "orders": [
    {"id": 101, "total": 49.9, "currency": "BRL"},
    {"id": 102, "currency": "BRL"}
  ]
}""",
        "issues": [
            "Second order is missing the 'total' field.",
            "No pagination metadata is returned for a collection endpoint.",
        ],
    },
    "user": {
        "label": "User Profile Endpoint",
        "payload": """{
  "status": 200,
  "user": {
    "id": 7,
    "name": "Gabriel",
    "email": null
  }
}""",
        "issues": [
            "Email is null even though the client expects a string.",
            "No explicit updated timestamp is provided for cache validation.",
        ],
    },
}

TEST_SCENARIOS = {
    "sorting": {
        "title": "Sorting Function",
        "cases": [
            "Normal case: [3, 1, 2] -> [1, 2, 3]",
            "Edge case: [] -> []",
            "Boundary case: [1] -> [1]",
            "Duplicate values: [2, 2, 1] -> [1, 2, 2]",
        ],
    },
    "calculator": {
        "title": "Calculator Division",
        "cases": [
            "Normal case: 10 / 2 -> 5",
            "Edge case: 0 / 5 -> 0",
            "Invalid input: 5 / 0 -> handled error",
            "Negative values: -9 / 3 -> -3",
        ],
    },
}

DOTNET_ENDPOINTS = [
    {
        "name": "GET /api/orders",
        "status": "Healthy",
        "latency": "82 ms",
        "note": "Stable response time and valid payload contract.",
    },
    {
        "name": "POST /api/payments",
        "status": "Warning",
        "latency": "241 ms",
        "note": "Latency spike detected during peak load simulation.",
    },
    {
        "name": "GET /api/users/{id}",
        "status": "Critical",
        "latency": "510 ms",
        "note": "Intermittent null payload found in profile response.",
    },
]

DOTNET_VALIDATION_CASES = {
    "registration": {
        "label": "User Registration DTO",
        "request": """{
  "name": "",
  "email": "gabriel.com",
  "age": 15
}""",
        "errors": [
            "Name is required.",
            "Email must be a valid email address.",
            "Age must be at least 18.",
        ],
    },
    "invoice": {
        "label": "Invoice Request DTO",
        "request": """{
  "customerId": 0,
  "amount": -45,
  "currency": ""
}""",
        "errors": [
            "CustomerId must be greater than zero.",
            "Amount must be positive.",
            "Currency is required.",
        ],
    },
}


def build_review_demo(sample_key):
    sample = REVIEW_SAMPLES.get(sample_key, REVIEW_SAMPLES["factorial"])
    issue_count = len(sample["issues"])
    score = max(58, 96 - issue_count * 12)
    return {
        "selected_key": sample_key if sample_key in REVIEW_SAMPLES else "factorial",
        "samples": REVIEW_SAMPLES,
        "sample": sample,
        "score": score,
        "quality_flags": [
            "Correctness" if any(item["category"] == "correctness" for item in sample["issues"]) else "Stable",
            "Instruction Following" if any(item["category"] == "instruction_following" for item in sample["issues"]) else "Aligned",
            "Code Quality" if any(item["category"] == "quality" for item in sample["issues"]) else "Readable",
        ],
    }


def build_challenge_demo(topic, difficulty):
    selected_topic = topic if topic in CHALLENGE_LIBRARY else "arrays"
    selected_difficulty = difficulty if difficulty in {"junior", "mid", "senior"} else "mid"
    challenge = CHALLENGE_LIBRARY[selected_topic]
    difficulty_labels = {
        "junior": "Junior",
        "mid": "Mid-Level",
        "senior": "Senior",
    }
    expectations = {
        "junior": "Focus on correctness, readable control flow, and basic input validation.",
        "mid": "Expect edge-case handling, clarity, and good decomposition choices.",
        "senior": "Expect strong tradeoff reasoning, scalable logic, and explicit assumptions.",
    }
    return {
        "topics": CHALLENGE_LIBRARY,
        "selected_topic": selected_topic,
        "selected_difficulty": selected_difficulty,
        "difficulty_label": difficulty_labels[selected_difficulty],
        "expectation": expectations[selected_difficulty],
        "challenge": challenge,
    }


def build_productivity_demo(status_filter):
    valid_filters = {"all", "Planned", "In Review", "Done"}
    selected_filter = status_filter if status_filter in valid_filters else "all"
    filtered_tasks = [
        task for task in REMOTE_TASKS if selected_filter == "all" or task["status"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "tasks": filtered_tasks,
        "stats": {
            "planned": sum(task["status"] == "Planned" for task in REMOTE_TASKS),
            "in_review": sum(task["status"] == "In Review" for task in REMOTE_TASKS),
            "done": sum(task["status"] == "Done" for task in REMOTE_TASKS),
        },
        "updates": REMOTE_UPDATES,
    }


def build_bug_triage_demo(severity_filter):
    valid_filters = {"all", "High", "Medium", "Low"}
    selected_filter = severity_filter if severity_filter in valid_filters else "all"
    reports = [
        bug for bug in BUG_REPORTS if selected_filter == "all" or bug["severity"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "reports": reports,
        "stats": {
            "high": sum(item["severity"] == "High" for item in BUG_REPORTS),
            "medium": sum(item["severity"] == "Medium" for item in BUG_REPORTS),
            "low": sum(item["severity"] == "Low" for item in BUG_REPORTS),
        },
    }


def build_api_auditor_demo(payload_key):
    selected_key = payload_key if payload_key in API_PAYLOADS else "orders"
    payload = API_PAYLOADS[selected_key]
    return {
        "selected_key": selected_key,
        "payloads": API_PAYLOADS,
        "payload": payload,
        "score": max(70, 95 - len(payload["issues"]) * 8),
    }


def build_test_case_demo(scenario_key):
    selected_key = scenario_key if scenario_key in TEST_SCENARIOS else "sorting"
    return {
        "selected_key": selected_key,
        "scenarios": TEST_SCENARIOS,
        "scenario": TEST_SCENARIOS[selected_key],
    }


def build_dotnet_monitor_demo(status_filter):
    valid_filters = {"all", "Healthy", "Warning", "Critical"}
    selected_filter = status_filter if status_filter in valid_filters else "all"
    endpoints = [
        item for item in DOTNET_ENDPOINTS if selected_filter == "all" or item["status"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "endpoints": endpoints,
        "stats": {
            "healthy": sum(item["status"] == "Healthy" for item in DOTNET_ENDPOINTS),
            "warning": sum(item["status"] == "Warning" for item in DOTNET_ENDPOINTS),
            "critical": sum(item["status"] == "Critical" for item in DOTNET_ENDPOINTS),
        },
    }


def build_dotnet_validation_demo(case_key):
    selected_key = case_key if case_key in DOTNET_VALIDATION_CASES else "registration"
    return {
        "selected_key": selected_key,
        "cases": DOTNET_VALIDATION_CASES,
        "case": DOTNET_VALIDATION_CASES[selected_key],
        "score": max(72, 96 - len(DOTNET_VALIDATION_CASES[selected_key]["errors"]) * 6),
    }


@app.route("/")
def index():
    return render_template("index.html", profile=profile)


@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((item for item in projects if item["slug"] == slug), None)
    if project is None:
        abort(404)

    demo = None
    if slug == "ai-code-review-sandbox":
        demo = build_review_demo(request.args.get("sample", "factorial"))
    elif slug == "python-challenge-generator":
        demo = build_challenge_demo(
            request.args.get("topic", "arrays"),
            request.args.get("difficulty", "mid"),
        )
    elif slug == "remote-productivity-portal":
        demo = build_productivity_demo(request.args.get("status", "all"))
    elif slug == "bug-triage-board":
        demo = build_bug_triage_demo(request.args.get("severity", "all"))
    elif slug == "api-response-auditor":
        demo = build_api_auditor_demo(request.args.get("payload", "orders"))
    elif slug == "test-case-studio":
        demo = build_test_case_demo(request.args.get("scenario", "sorting"))
    elif slug == "dotnet-api-monitor":
        demo = build_dotnet_monitor_demo(request.args.get("status", "all"))
    elif slug == "dotnet-validation-lab":
        demo = build_dotnet_validation_demo(request.args.get("case", "registration"))

    return render_template("project.html", profile=profile, project=project, demo=demo)


if __name__ == "__main__":
    app.run(debug=True)
