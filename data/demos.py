"""
Demo data for all portfolio project interactive demos.
AvenuePulse demo reflects the real architecture in Projeto Avenue.
"""

from __future__ import annotations
import uuid
import random
from datetime import datetime, timezone


# ── AvenuePulse ───────────────────────────────────────────────────────────────

# Real prices from pricing-go/main.go
_BASE_PRICES = {
    "AAPL":  185.00,
    "MSFT":  428.00,
    "NVDA":  137.00,
    "GOOGL": 174.00,
    "AMZN":  184.00,
    "META":  596.00,
    "TSLA":  178.00,
    "AVGO":  232.00,
    "BRKB":  458.00,
    "JPM":   248.00,
    "LLY":   796.00,
    "V":     288.00,
    "UNH":   296.00,
    "XOM":   114.00,
    "MA":    498.00,
    "COST":  936.00,
    "HD":    392.00,
    "PG":    168.00,
    "NFLX": 1051.00,
    "JNJ":   158.00,
    "VOO":   486.00,
}

# Max single-order notional from MaxSingleOrderNotionalRule
_NOTIONAL_LIMIT = 25_000.00


def _spread(base: float) -> float:
    """Simulate ±0.4% market spread — same logic as pricing-go."""
    variation = random.uniform(-0.004, 0.004)
    return round(base * (1 + variation), 2)


def _short_id(full_id: str) -> str:
    return full_id[:8] + "..."


_SCENARIOS = {
    "buy_aapl_50": {
        "label": "BUY AAPL — 50 shares @ $185.00",
        "symbol": "AAPL",
        "side": "Buy",
        "quantity": 50,
        "limit_price": 185.00,
        "account_id": "ACC-DEMO-001",
    },
    "buy_tsla_200": {
        "label": "BUY TSLA — 200 shares @ $180.00  (will be rejected)",
        "symbol": "TSLA",
        "side": "Buy",
        "quantity": 200,
        "limit_price": 180.00,
        "account_id": "ACC-DEMO-002",
    },
    "sell_googl_40": {
        "label": "SELL GOOGL — 40 shares @ $174.00",
        "symbol": "GOOGL",
        "side": "Sell",
        "quantity": 40,
        "limit_price": 174.00,
        "account_id": "ACC-DEMO-003",
    },
    "buy_msft_60": {
        "label": "BUY MSFT — 60 shares @ $428.00  (will be rejected)",
        "symbol": "MSFT",
        "side": "Buy",
        "quantity": 60,
        "limit_price": 428.00,
        "account_id": "ACC-DEMO-004",
    },
}


def _build_avenue_scenario(key: str) -> dict:
    s = _SCENARIOS[key]
    symbol = s["symbol"]
    side = s["side"]
    quantity = s["quantity"]
    limit_price = s["limit_price"]
    account_id = s["account_id"]

    market_price = _spread(_BASE_PRICES[symbol])
    effective_price = min(limit_price, market_price)
    notional = round(quantity * effective_price, 2)
    latency_ms = random.randint(9, 22)

    order_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())
    corr_id = "corr-" + str(uuid.uuid4())[:8]
    message_id = uuid.uuid4().hex[:16]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Risk evaluation — replicates CompositeRiskPolicy exactly
    supported_symbols = list(_BASE_PRICES.keys())
    rules = []

    # Rule 1: SupportedAssetRule
    asset_pass = symbol in supported_symbols
    rules.append({
        "name": "SupportedAssetRule",
        "check": f"{symbol} in [{', '.join(supported_symbols)}]",
        "result": "PASS" if asset_pass else "FAIL",
        "passed": asset_pass,
    })

    # Rule 2: MaxSingleOrderNotionalRule (only evaluated if rule 1 passes)
    notional_pass = notional <= _NOTIONAL_LIMIT
    if asset_pass:
        rules.append({
            "name": "MaxSingleOrderNotionalRule",
            "check": f"${notional:,.2f} {'≤' if notional_pass else '>'} ${_NOTIONAL_LIMIT:,.0f}",
            "result": "PASS" if notional_pass else "FAIL",
            "passed": notional_pass,
        })

    all_passed = asset_pass and notional_pass
    decision = "Approved" if all_passed else "Rejected"

    if not asset_pass:
        reason = f"Symbol {symbol} is not in the supported asset list."
    elif not notional_pass:
        reason = (
            f"Single-order notional ${notional:,.2f} "
            f"exceeds the limit of ${_NOTIONAL_LIMIT:,.0f}."
        )
    else:
        reason = "All risk rules passed."

    risk_profile = "low" if notional < 10_000 else "medium" if notional < 20_000 else "high"

    return {
        # Order
        "order_id": order_id,
        "order_id_short": _short_id(order_id),
        "account_id": account_id,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "limit_price": f"{limit_price:,.2f}",
        "status": "PendingRisk",
        # Pricing (from pricing-go)
        "market_price": f"{market_price:,.2f}",
        "effective_price": f"{effective_price:,.2f}",
        "notional": f"{notional:,.2f}",
        "latency_ms": latency_ms,
        "pricing_source": "mock-market",
        # Outbox / event envelope
        "event_name": "orders.order-placed.v1",
        "event_id": event_id,
        "event_id_short": _short_id(event_id),
        "corr_id": corr_id,
        "message_id": message_id,
        "now": now,
        # Risk
        "rules": rules,
        "decision": decision,
        "approved": all_passed,
        "reason": reason,
        "risk_profile": risk_profile,
        "exposure": f"{notional:,.2f}",
        # MongoDB projection snippet
        "mongo_doc": (
            f'{{\n'
            f'  "orderId": "{_short_id(order_id)}",\n'
            f'  "accountId": "{account_id}",\n'
            f'  "decision": "{decision}",\n'
            f'  "reason": "{reason}",\n'
            f'  "riskProfile": "{risk_profile}",\n'
            f'  "flagged": {"true" if not all_passed else "false"},\n'
            f'  "exposureAfterOrder": {notional},\n'
            f'  "recordedAt": "{now}"\n'
            f'}}'
        ),
    }


def get_avenue_demo(selected_key: str = "buy_aapl_50") -> dict:
    if selected_key not in _SCENARIOS:
        selected_key = "buy_aapl_50"
    return {
        "scenarios": {k: {"label": v["label"]} for k, v in _SCENARIOS.items()},
        "selected_key": selected_key,
        "scenario": _build_avenue_scenario(selected_key),
    }


# ── AI Code Review Sandbox ────────────────────────────────────────────────────

_CODE_SAMPLES = {
    "fizzbuzz": {
        "label": "FizzBuzz implementation",
        "prompt": "Write a Python function that returns FizzBuzz output for numbers 1 to n.",
        "code": (
            "def fizzbuzz(n):\n"
            "    result = []\n"
            "    for i in range(n):   # off-by-one: should be range(1, n+1)\n"
            "        if i % 15 == 0:\n"
            "            result.append('FizzBuzz')\n"
            "        elif i % 3 == 0:\n"
            "            result.append('Fizz')\n"
            "        elif i % 5 == 0:\n"
            "            result.append('Buzz')\n"
            "        else:\n"
            "            result.append(i)  # should be str(i)\n"
            "    return result"
        ),
        "issues": [
            {"title": "Off-by-one error", "detail": "range(n) starts at 0; should be range(1, n+1)."},
            {"title": "Type inconsistency", "detail": "Appending int i instead of str(i) breaks list homogeneity."},
            {"title": "Missing docstring", "detail": "No type hints or docstring for public function."},
        ],
        "positive_notes": [
            "Clear list-accumulation pattern.",
            "FizzBuzz check (% 15) correctly placed before individual checks.",
            "Readable variable names.",
        ],
        "score": 54,
    },
    "reverse_string": {
        "label": "Reverse a string",
        "prompt": "Write a Python function that reverses a string without using slicing.",
        "code": (
            "def reverse_string(s):\n"
            "    result = ''\n"
            "    for char in s:\n"
            "        result = char + result\n"
            "    return result"
        ),
        "issues": [
            {"title": "O(n²) string concatenation", "detail": "String concatenation in a loop is quadratic. Use list + join."},
            {"title": "No input validation", "detail": "No type check for non-string inputs."},
        ],
        "positive_notes": [
            "Correctly reverses without slicing as instructed.",
            "Clean loop structure.",
        ],
        "score": 68,
    },
}


def get_code_review_demo(selected_key: str = "fizzbuzz") -> dict:
    if selected_key not in _CODE_SAMPLES:
        selected_key = "fizzbuzz"
    sample = _CODE_SAMPLES[selected_key]
    flags = ["Logic Error", "Type Issue", "Style"] if selected_key == "fizzbuzz" else ["Performance", "Validation"]
    return {
        "samples": {k: {"label": v["label"]} for k, v in _CODE_SAMPLES.items()},
        "selected_key": selected_key,
        "sample": sample,
        "score": sample["score"],
        "quality_flags": flags,
    }


# ── Python Challenge Generator ────────────────────────────────────────────────

_TOPICS = {
    "data_structures": {
        "title": "Data Structures",
        "challenges": {
            "junior": {
                "title": "Reverse a linked list",
                "brief": "Given the head of a singly linked list, reverse it in place and return the new head.",
                "constraints": [
                    "Do not use extra data structures.",
                    "O(n) time, O(1) space.",
                    "Handle empty list and single node.",
                ],
                "test_cases": [
                    "Input: [1,2,3,4] → Output: [4,3,2,1]",
                    "Input: [] → Output: []",
                    "Input: [7] → Output: [7]",
                ],
            },
            "mid": {
                "title": "LRU Cache",
                "brief": "Implement an LRU Cache with O(1) get and put using Python.",
                "constraints": [
                    "Use OrderedDict or doubly linked list + hashmap.",
                    "Capacity is a constructor parameter.",
                    "Evict least-recently-used on overflow.",
                ],
                "test_cases": [
                    "cache = LRUCache(2); cache.put(1,1); cache.put(2,2); cache.get(1) → 1",
                    "cache.put(3,3) evicts key 2; cache.get(2) → -1",
                ],
            },
            "senior": {
                "title": "Serialize and deserialize a binary tree",
                "brief": "Design an algorithm to serialize a binary tree to a string and deserialize it back.",
                "constraints": [
                    "Must handle None/null nodes.",
                    "No restriction on encoding format.",
                    "Round-trip must be lossless.",
                ],
                "test_cases": [
                    "tree = [1,2,3,null,null,4,5]; deserialize(serialize(tree)) == tree",
                ],
            },
        },
    },
    "algorithms": {
        "title": "Algorithms",
        "challenges": {
            "junior": {
                "title": "Binary search",
                "brief": "Implement binary search on a sorted list. Return the index or -1 if not found.",
                "constraints": ["O(log n) time.", "Do not use built-in search.", "Handle duplicates by returning any valid index."],
                "test_cases": [
                    "binary_search([1,3,5,7,9], 5) → 2",
                    "binary_search([1,3,5,7,9], 6) → -1",
                    "binary_search([], 1) → -1",
                ],
            },
            "mid": {
                "title": "Merge intervals",
                "brief": "Given a list of intervals, merge all overlapping ones and return the result.",
                "constraints": ["Sort before merging.", "O(n log n) time.", "Output must be sorted."],
                "test_cases": [
                    "merge([[1,3],[2,6],[8,10],[15,18]]) → [[1,6],[8,10],[15,18]]",
                    "merge([[1,4],[4,5]]) → [[1,5]]",
                ],
            },
            "senior": {
                "title": "Median of two sorted arrays",
                "brief": "Find the median of two sorted arrays in O(log(m+n)) time.",
                "constraints": ["O(log(m+n)) time.", "Arrays may be different sizes.", "Handle odd and even total lengths."],
                "test_cases": [
                    "findMedian([1,3], [2]) → 2.0",
                    "findMedian([1,2], [3,4]) → 2.5",
                ],
            },
        },
    },
}

_DIFFICULTY_LABELS = {"junior": "Junior", "mid": "Mid-Level", "senior": "Senior"}
_EXPECTATIONS = {
    "junior": "Correct logic, readable code, handles edge cases.",
    "mid": "Efficient solution, good abstractions, clear reasoning.",
    "senior": "Optimal complexity, handles all edge cases, clean API design.",
}


def get_challenge_demo(selected_topic: str = "data_structures", selected_difficulty: str = "junior") -> dict:
    if selected_topic not in _TOPICS:
        selected_topic = "data_structures"
    if selected_difficulty not in _DIFFICULTY_LABELS:
        selected_difficulty = "junior"
    topic = _TOPICS[selected_topic]
    challenge = topic["challenges"][selected_difficulty]
    return {
        "topics": {k: {"title": v["title"]} for k, v in _TOPICS.items()},
        "selected_topic": selected_topic,
        "selected_difficulty": selected_difficulty,
        "challenge": challenge,
        "difficulty_label": _DIFFICULTY_LABELS[selected_difficulty],
        "expectation": _EXPECTATIONS[selected_difficulty],
    }


# ── Remote Productivity Portal ────────────────────────────────────────────────

_TASKS = [
    {"title": "Set up CI pipeline", "status": "Done", "priority": "High", "owner": "Gabriel"},
    {"title": "Write API docs", "status": "In Review", "priority": "Medium", "owner": "Gabriel"},
    {"title": "Refactor auth module", "status": "In Review", "priority": "High", "owner": "Gabriel"},
    {"title": "Add unit tests", "status": "Planned", "priority": "Medium", "owner": "Gabriel"},
    {"title": "Design DB schema v2", "status": "Planned", "priority": "Low", "owner": "Gabriel"},
    {"title": "Deploy to staging", "status": "Done", "priority": "High", "owner": "Gabriel"},
]

_UPDATES = [
    "CI pipeline is green — all checks passing.",
    "API docs PR open for review, comments welcome.",
    "Auth refactor in progress — ETA 2 days.",
    "Unit test coverage at 74%, target 90%.",
    "DB schema v2 design meeting scheduled Friday.",
]


def get_portal_demo(selected_filter: str = "all") -> dict:
    filtered = _TASKS if selected_filter == "all" else [t for t in _TASKS if t["status"] == selected_filter]
    stats = {
        "planned": sum(1 for t in _TASKS if t["status"] == "Planned"),
        "in_review": sum(1 for t in _TASKS if t["status"] == "In Review"),
        "done": sum(1 for t in _TASKS if t["status"] == "Done"),
    }
    return {"tasks": filtered, "updates": _UPDATES, "stats": stats, "selected_filter": selected_filter}


# ── Bug Triage Board ──────────────────────────────────────────────────────────

_BUGS = [
    {"title": "Login fails on Safari", "severity": "High", "status": "Open", "impact": "Blocks ~20% of users on macOS/iOS."},
    {"title": "Payment timeout after 30s", "severity": "High", "status": "In Progress", "impact": "Causes abandoned checkouts."},
    {"title": "CSV export missing headers", "severity": "Medium", "status": "Open", "impact": "Data team workaround in place."},
    {"title": "Tooltip overflow on mobile", "severity": "Low", "status": "Open", "impact": "Minor UX issue, non-blocking."},
    {"title": "Search returns stale cache", "severity": "Medium", "status": "In Progress", "impact": "Stale results for ~5 minutes."},
]


def get_triage_demo(selected_filter: str = "all") -> dict:
    filtered = _BUGS if selected_filter == "all" else [b for b in _BUGS if b["severity"] == selected_filter]
    stats = {
        "high": sum(1 for b in _BUGS if b["severity"] == "High"),
        "medium": sum(1 for b in _BUGS if b["severity"] == "Medium"),
        "low": sum(1 for b in _BUGS if b["severity"] == "Low"),
    }
    return {"reports": filtered, "stats": stats, "selected_filter": selected_filter}


# ── API Response Auditor ──────────────────────────────────────────────────────

_PAYLOADS = {
    "user_profile": {
        "label": "/api/users/42 — User Profile",
        "payload": '{\n  "id": 42,\n  "email": null,\n  "name": "John",\n  "role": "admin"\n}',
        "issues": ["email is null — required field missing.", "No created_at timestamp.", "No HTTP status field in envelope."],
        "score": 61,
    },
    "order_list": {
        "label": "/api/orders — Order List",
        "payload": '{\n  "data": [],\n  "total": 0\n}',
        "issues": ["Missing pagination fields (page, per_page).", "No request_id for tracing.", "Empty data with no explanation message."],
        "score": 48,
    },
    "product": {
        "label": "/api/products/7 — Product Detail",
        "payload": '{\n  "id": 7,\n  "name": "Notebook Pro",\n  "price": 1299.99,\n  "stock": 14,\n  "category": "electronics"\n}',
        "issues": ["No currency field alongside price.", "Missing updated_at field."],
        "score": 79,
    },
}


def get_auditor_demo(selected_key: str = "user_profile") -> dict:
    if selected_key not in _PAYLOADS:
        selected_key = "user_profile"
    payload = _PAYLOADS[selected_key]
    return {
        "payloads": {k: {"label": v["label"]} for k, v in _PAYLOADS.items()},
        "selected_key": selected_key,
        "payload": payload,
        "score": payload["score"],
    }


# ── Test Case Studio ──────────────────────────────────────────────────────────

_SCENARIOS_TC = {
    "login": {
        "title": "User login flow",
        "cases": [
            "Valid credentials → 200 OK + JWT token returned.",
            "Invalid password → 401 Unauthorized, no token.",
            "Non-existent email → 401 (same message, no user enumeration).",
            "Empty fields → 400 Bad Request.",
            "SQL injection in email field → 400, no crash.",
            "Rate limit: 5 failed attempts → 429 Too Many Requests.",
        ],
    },
    "payment": {
        "title": "Payment processing",
        "cases": [
            "Valid card, sufficient balance → 200 OK, transaction ID returned.",
            "Expired card → 402 Payment Required, clear error message.",
            "Insufficient funds → 402 with funds-related message.",
            "Invalid CVV → 402, no charge attempted.",
            "Network timeout → retry logic triggered, idempotency key respected.",
            "Duplicate request with same idempotency key → same response, no double charge.",
        ],
    },
    "search": {
        "title": "Search / filter endpoint",
        "cases": [
            "Exact match query → correct items returned.",
            "Partial match → items containing term returned.",
            "Empty query string → all items (or 400, documented behavior).",
            "Special characters (&, <, %) → sanitized, no injection.",
            "Very long query (>1000 chars) → 400 Bad Request.",
            "Filter by non-existent category → empty result, not 404.",
        ],
    },
}


def get_test_studio_demo(selected_key: str = "login") -> dict:
    if selected_key not in _SCENARIOS_TC:
        selected_key = "login"
    return {
        "scenarios": {k: {"title": v["title"]} for k, v in _SCENARIOS_TC.items()},
        "selected_key": selected_key,
        "scenario": _SCENARIOS_TC[selected_key],
    }


# ── .NET API Monitor ──────────────────────────────────────────────────────────

_ENDPOINTS = [
    {"name": "GET /api/v1/health", "status": "Healthy", "latency": "12ms", "note": "All dependencies reachable."},
    {"name": "POST /api/v1/orders", "status": "Healthy", "latency": "84ms", "note": "Pricing call included."},
    {"name": "GET /api/v1/orders", "status": "Warning", "latency": "340ms", "note": "DB query slow — missing index."},
    {"name": "GET /api/v1/metrics", "status": "Healthy", "latency": "22ms", "note": "Cache hit rate 94%."},
    {"name": "POST /api/v1/webhooks/status", "status": "Critical", "latency": "timeout", "note": "RabbitMQ connection dropped."},
]


def get_monitor_demo(selected_filter: str = "all") -> dict:
    filtered = _ENDPOINTS if selected_filter == "all" else [e for e in _ENDPOINTS if e["status"] == selected_filter]
    stats = {
        "healthy": sum(1 for e in _ENDPOINTS if e["status"] == "Healthy"),
        "warning": sum(1 for e in _ENDPOINTS if e["status"] == "Warning"),
        "critical": sum(1 for e in _ENDPOINTS if e["status"] == "Critical"),
    }
    return {"endpoints": filtered, "stats": stats, "selected_filter": selected_filter}


# ── .NET Validation Lab ───────────────────────────────────────────────────────

_CASES_VL = {
    "missing_fields": {
        "label": "Missing required fields",
        "request": '{\n  "accountId": "",\n  "symbol": "AAPL",\n  "side": "Buy",\n  "quantity": 0,\n  "limitPrice": -10.0\n}',
        "errors": [
            "accountId: must not be empty.",
            "quantity: must be greater than 0.",
            "limitPrice: must be a positive value.",
        ],
        "score": 0,
    },
    "unsupported_symbol": {
        "label": "Unsupported symbol",
        "request": '{\n  "accountId": "ACC-001",\n  "symbol": "GME",\n  "side": "Buy",\n  "quantity": 100,\n  "limitPrice": 15.00\n}',
        "errors": ["symbol: 'GME' is not in the supported asset list."],
        "score": 75,
    },
    "valid_request": {
        "label": "Valid request",
        "request": '{\n  "accountId": "ACC-001",\n  "symbol": "MSFT",\n  "side": "Buy",\n  "quantity": 50,\n  "limitPrice": 425.00\n}',
        "errors": [],
        "score": 100,
    },
}


def get_validation_demo(selected_key: str = "missing_fields") -> dict:
    if selected_key not in _CASES_VL:
        selected_key = "missing_fields"
    case = _CASES_VL[selected_key]
    return {
        "cases": {k: {"label": v["label"]} for k, v in _CASES_VL.items()},
        "selected_key": selected_key,
        "case": case,
        "score": case["score"],
    }
