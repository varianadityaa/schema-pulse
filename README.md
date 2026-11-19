# schema-pulse

[![PyPI version](https://img.shields.io/badge/pypi-v1.8.2-blue.svg)](https://pypi.org/project/schema-pulse/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Coverage](https://img.shields.io/badge/coverage-78%25-yellowgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Automated schema validation, drift detection, and statistical anomaly monitoring for Python data ingestion pipelines—with zero third-party dependencies.**

`schema-pulse` is a lightweight library and CLI tool designed for data engineers and backend developers who need deterministic runtime validation without bloating production environments with heavy dependency trees. Built purely on the Python standard library, it enforces strict structural contracts and flags distribution shifts with sub-millisecond overhead.

---

## Key Features

- **Zero External Dependencies:** Pure Python standard library implementation (`typing`, `dataclasses`, `statistics`, `json`). Drop it into any AWS Lambda, Airflow worker, or container without dependency conflicts.
- **Sub-Millisecond Runtime Overhead:** Optimized single-pass validation engine built for high-throughput batch and micro-batch ingestion.
- **Automated Schema Inference & Drift Detection:** Automatically baseline JSON/dict payloads and detect breaking changes (missing keys, type coercion anomalies, unexpected nullability).
- **Statistical Anomaly Alerts:** Lightweight Z-score and interquartile range (IQR) checks on numeric fields during ingestion.
- **First-Class CLI & Python API:** Run checks inline within Python ETL scripts or integrate directly into CI/CD pipelines via the `schema-pulse` CLI.

---

## Installation

```bash
pip install schema-pulse
```

For local development and running the test suite:

```bash
git clone [https://github.com/varianadityaa/schema-pulse.git](https://github.com/varianadityaa/schema-pulse.git)
cd schema-pulse
pip install -e ".[dev]"
pytest
```

---

## Quickstart (Python API)

Define a strict schema contract or infer one from a baseline dataset, then validate incoming records in real time:

```python
from schema_pulse import PulseValidator, Field, AnomalyRule

# 1. Define schema contract and anomaly thresholds
schema = {
    "event_id": Field(str, nullable=False),
    "sensor_temp": Field(float, min_val=-40.0, max_val=125.0, anomaly=AnomalyRule(z_threshold=3.0)),
    "batch_count": Field(int, min_val=1),
    "tags": Field(list, nullable=True),
}

validator = PulseValidator(schema, strict=True)

# 2. Validate incoming ingestion payload
payload = [
    {"event_id": "evt_901", "sensor_temp": 42.5, "batch_count": 120, "tags": ["line-a"]},
    {"event_id": "evt_902", "sensor_temp": 999.9, "batch_count": 118, "tags": None},
]

report = validator.validate_batch(payload)

if not report.is_valid:
    print(f"Detected {len(report.errors)} schema/anomaly violations:")
    for err in report.errors:
        print(f" - Record [{err.index}] | Field '{err.field}': {err.reason}")
```

### Automatic Schema Inference

Generate a reusable JSON schema baseline directly from clean sample records:

```python
from schema_pulse import infer_schema

baseline_records = [
    {"user_id": 101, "latency_ms": 14.2, "status": "ok"},
    {"user_id": 102, "latency_ms": 15.8, "status": "ok"},
]

inferred = infer_schema(baseline_records)
inferred.save("contracts/api_events_v1.json")
```

---

## CLI Usage

`schema-pulse` includes a built-in CLI for validating NDJSON or JSON files in CI/CD checks and shell pipelines:

```bash
# Infer a contract from baseline data
schema-pulse infer data/baseline.ndjson --output contracts/schema.json

# Validate an incoming batch against the saved contract
schema-pulse validate data/incoming_batch.ndjson --contract contracts/schema.json --strict
```

---

## Performance Benchmarks

Benchmarked on Python 3.12 (single core) validating 10,000 nested JSON records (12 fields per record):

| Operation Mode | Avg. Latency / Record | Total Batch Time (10k) | Peak Memory Overhead |
| :--- | :---: | :---: | :---: |
| Standard Type & Null Check | `0.018 ms` | `180 ms` | `< 1.2 MB` |
| Strict Mode + Anomaly Detection | `0.034 ms` | `340 ms` | `< 1.8 MB` |
| Schema Inference (`10k` sample) | `0.041 ms` | `410 ms` | `< 2.4 MB` |

---

## Roadmap (v2.0)

Active development is focused on the upcoming `v2.0` release:

- [ ] **Async Streaming Engine:** Non-blocking `async/await` validation support for Kafka, Kinesis, and async HTTP ingestion streams.
- [ ] **Expanded Test Coverage:** Increasing unit and property-based `pytest` coverage from 78% to >95%.
- [ ] **Pluggable Serialization Adapters:** Native zero-copy support for `dataclasses`, `TypedDict`, and CSV stream readers.
- [ ] **Migration & Diff CLI:** Automated v1-to-v2 contract diffing and human-readable markdown changelog generation.

---

## Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the repository and create your branch (`git checkout -b feat/async-stream-adapter`).
2. Ensure all existing tests pass (`pytest -v`).
3. Submit a Pull Request with a clear description of the problem solved and benchmark impact (if applicable).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

Copyright (c) 2026 [Varian Aditya](https://github.com/varianadityaa)
