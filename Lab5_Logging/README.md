# Lab 5 — Python Logging

## Overview
This lab explores Python's built-in `logging` library, starting from basic configuration and progressing to advanced concepts like custom log levels, filters, and multi-handler setups. By the end of this lab, you will understand how to effectively log messages, exceptions, and errors in a real-world Python application.

---

## Prerequisites
- Python 3.x installed
- Basic understanding of Python (functions, exceptions, classes)
- No external libraries required — `logging` and `os` are both part of the Python standard library. Thus there is no requirements.txt

---

## File Structure
```
Lab5_Logging/
├── logging_guide.py   # Main script with all logging examples
├── app.log            # Generated log file (created on first run)
└── README.md          # This file
```

---

## How to Run
```bash
cd Lab5_Logging
python logging_guide.py
```
`app.log` will be created automatically in the same directory as the script.

---

## What the Script Covers

### Step 1 — Basic Configuration
Sets up the root logger using `basicConfig` with a `DEBUG` level and a timestamp-based format.

### Step 2 — Log Levels
Demonstrates all 5 built-in log levels in order of severity:

| Level | Value | Use Case |
|---|---|---|
| DEBUG | 10 | Detailed developer info |
| INFO | 20 | General app events |
| WARNING | 30 | Potential issues |
| ERROR | 40 | Something went wrong |
| CRITICAL | 50 | System-breaking failure |

### Step 3 — Custom Loggers
Creates a named logger (`my_module`) instead of using the root logger, which is best practice in multi-module applications.

### Step 4 — Logging Exceptions
Uses `logger.exception()` to log a `ZeroDivisionError` with its full traceback automatically attached.

### Step 5 — Multiple Handlers
Attaches both a `StreamHandler` (console) and a `FileHandler` (app.log) to the same logger, so messages are sent to both destinations simultaneously.

### Step 6 — Custom Log Levels
Defines two new log levels beyond the defaults:

| Level | Value | Position |
|---|---|---|
| VERBOSE | 5 | Below DEBUG |
| AUDIT | 35 | Between WARNING and ERROR |

New `verbose()` and `audit()` methods are patched directly onto the `Logger` class.

### Step 7 — Custom Filters
Implements two filter classes:
- **`KeywordFilter`** — only allows messages containing a specific keyword (e.g. `"payment"`)
- **`BlockLoggerFilter`** — suppresses all messages from a specific logger (e.g. `"noisy_module"`)

### Step 8 — Multiple Error Types
Logs four different exception types using `logger.exception()`, each with a full traceback:

| Error | Trigger |
|---|---|
| `ValueError` | `int("not_a_number")` |
| `FileNotFoundError` | Opening a non-existent file |
| `TypeError` | `"hello" + 5` |
| `KeyError` | Accessing a missing dictionary key |

---

## Output
Running the script produces:
- **Console output** — all log messages from every step
- **app.log** — messages from Steps 5, 6, 7, and 8 written to file

The log format used throughout is:
```
YYYY-MM-DD HH:MM:SS,mmm - <logger_name> - <LEVEL> - <message>
```