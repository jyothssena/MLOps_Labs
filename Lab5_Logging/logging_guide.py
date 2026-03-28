import logging
import os

# =============================================================================
# STEP 1 — Basic Configuration
# =============================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
# =============================================================================
# STEP 2 — Logging Messages at Different Levels
# =============================================================================
logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")

# =============================================================================
# STEP 3 — Using Custom Loggers
# =============================================================================
logger = logging.getLogger("my_module")

logger.debug("Debug message from my_module")
logger.info("Info message from my_module")

# =============================================================================
# STEP 4 — Logging Exceptions
# =============================================================================
try:
    result = 10 / 0
except ZeroDivisionError:
    logging.exception("An error occurred while dividing by zero")

# =============================================================================
# STEP 5 — Log Handlers (console + file simultaneously)
# =============================================================================
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_PATH)

module_logger = logging.getLogger("my_module_handlers")
module_logger.addHandler(console_handler)
module_logger.addHandler(file_handler)

try:
    result = 10 / 0
except ZeroDivisionError:
    module_logger.exception("An error occurred while dividing by zero")

# =============================================================================
# STEP 6 — Custom Log Levels
# Define two new levels: VERBOSE (below DEBUG) and AUDIT (above WARNING)
# =============================================================================
VERBOSE_LEVEL = 5   # Lower than DEBUG (10)
AUDIT_LEVEL   = 35  # Between WARNING (30) and ERROR (40)

logging.addLevelName(VERBOSE_LEVEL, "VERBOSE")
logging.addLevelName(AUDIT_LEVEL,   "AUDIT")

def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VERBOSE_LEVEL):
        self._log(VERBOSE_LEVEL, message, args, **kwargs)

def audit(self, message, *args, **kwargs):
    if self.isEnabledFor(AUDIT_LEVEL):
        self._log(AUDIT_LEVEL, message, args, **kwargs)

# Attach the new methods to the Logger class so all loggers can use them
logging.Logger.verbose = verbose
logging.Logger.audit   = audit

custom_logger = logging.getLogger("custom_levels")
custom_logger.setLevel(VERBOSE_LEVEL)  # Allow all levels including VERBOSE
custom_file_handler = logging.FileHandler(LOG_PATH)
custom_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
custom_logger.addHandler(custom_file_handler)

custom_logger.verbose("This is a verbose message — lower than DEBUG")
custom_logger.debug("This is a debug message")
custom_logger.info("This is an info message")
custom_logger.audit("AUDIT: User 'admin' logged in successfully")
custom_logger.warning("This is a warning message")
custom_logger.error("This is an error message")
custom_logger.critical("This is a critical message")

# =============================================================================
# STEP 7 — Custom Filters
# Filter 1: Only allow messages that contain a specific keyword
# Filter 2: Block messages from a specific logger name
# =============================================================================

# --- Filter 1: Keyword Filter ---
class KeywordFilter(logging.Filter):
    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def filter(self, record):
        # Only allow log records whose message contains the keyword
        return self.keyword.lower() in record.getMessage().lower()

# --- Filter 2: Block Logger Filter ---
class BlockLoggerFilter(logging.Filter):
    def __init__(self, blocked_name):
        super().__init__()
        self.blocked_name = blocked_name

    def filter(self, record):
        # Block any log records coming from the specified logger name
        return record.name != self.blocked_name

# Apply Keyword Filter — only messages containing "payment" will pass
keyword_handler = logging.StreamHandler()
keyword_handler.addFilter(KeywordFilter("payment"))

filtered_logger = logging.getLogger("filtered_logger")
filtered_logger.addHandler(keyword_handler)
filtered_logger.setLevel(logging.DEBUG)
filtered_logger.propagate = False
filtered_file_handler = logging.FileHandler(LOG_PATH)
filtered_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
filtered_logger.addHandler(filtered_file_handler)  # Don't pass logs up to root logger

print("\n--- Keyword Filter: only 'payment' messages ---")
filtered_logger.info("User logged in")                          # blocked
filtered_logger.info("Payment of $200 received")               # allowed
filtered_logger.warning("Payment gateway timeout")             # allowed
filtered_logger.error("Failed to process refund for order 99") # blocked

# =============================================================================
# STEP 8 — Logging Multiple Error Types
# =============================================================================
error_logger = logging.getLogger("error_examples")
error_file_handler = logging.FileHandler(LOG_PATH)
error_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_file_handler)

print("\n--- ValueError ---")
try:
    number = int("not_a_number")  # Can't convert a string to int
except ValueError:
    error_logger.exception("ValueError: invalid literal for int()")

print("\n--- FileNotFoundError ---")
try:
    with open("nonexistent_file.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    error_logger.exception("FileNotFoundError: file does not exist")

print("\n--- TypeError ---")
try:
    result = "hello" + 5  # Can't add a string and an integer
except TypeError:
    error_logger.exception("TypeError: unsupported operand types")

print("\n--- KeyError ---")
try:
    data = {"name": "Alice", "age": 25}
    print(data["email"])  # Key doesn't exist in the dictionary
except KeyError:
    error_logger.exception("KeyError: key not found in dictionary")

# Apply Block Logger Filter — suppress logs from "noisy_module"
block_handler = logging.StreamHandler()
block_handler.addFilter(BlockLoggerFilter("noisy_module"))

app_logger = logging.getLogger("app")
app_logger.addHandler(block_handler)
app_logger.setLevel(logging.DEBUG)
app_logger.propagate = False

noisy_logger = logging.getLogger("noisy_module")
noisy_logger.parent = app_logger  # Make noisy_module a child of app
noisy_logger.propagate = True

print("\n--- Block Logger Filter: suppress 'noisy_module' ---")
app_logger.info("App started successfully")                     # allowed
noisy_logger.debug("noisy_module: internal poll tick")         # blocked
noisy_logger.debug("noisy_module: cache miss on key 'user_1'") # blocked
app_logger.warning("Low memory warning")                       # allowed