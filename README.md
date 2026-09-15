# Copilot Test - System Uptime Script

## Overview

This repository documents my experience using GitHub Copilot to create a production-ready system uptime script. The project demonstrates Copilot's capabilities in generating code and how iterative refinement improves security and reliability.

---

## Experience Using Copilot

### Initial Code Generation

**What Copilot Generated:**

Copilot initially created a basic system uptime script with cross-platform support for Linux, macOS, and Windows. The generated code included:

- A `get_system_uptime()` function that detected the operating system
- Platform-specific methods to retrieve uptime:
  - **Linux**: Reading from `/proc/uptime`
  - **macOS**: Using the `uptime -p` command via `os.popen()`
  - **Windows**: Extracting boot time from `wmic os get lastbootuptime`
- Conversion of uptime seconds to a human-readable format (days, hours, minutes, seconds)
- Basic error handling with try-except blocks

The script was functional and demonstrated Copilot's ability to generate multi-platform compatible code with appropriate OS-specific logic.

### Script Modifications

**Why I Modified the Script:**

After reviewing the initial Copilot-generated code, I identified several security and reliability concerns that required improvement:

1. **Security Issues:**
   - Used `os.popen()` which is vulnerable to shell injection attacks
   - No input validation on command outputs
   - No permission checks before file access
   - No timeout protection for subprocess calls
   - Unsafe string parsing without format validation

2. **Reliability Issues:**
   - Limited error handling for edge cases
   - No logging mechanism for debugging
   - Weak fallback strategies when primary methods fail
   - No validation for negative or malformed uptime values
   - No protection against hanging processes

3. **Code Quality:**
   - Procedural design could be better organized
   - Missing type hints for better code safety
   - Minimal documentation
   - No structured exception handling for different failure modes

**Modifications Made:**

1. **Refactored to Object-Oriented Design:**
   ```python
   class UptimeReader:
       """Safe and reliable system uptime reader with security and error handling."""
   ```
   - Encapsulated uptime logic in a reusable class
   - Better code organization and maintainability

2. **Enhanced Security:**
   - Replaced `os.popen()` with `subprocess.run()` using `capture_output=True`
   - Added input validation for all external data
   - Implemented permission checks before file operations
   - Added timeouts to subprocess calls (5-10 seconds)
   - Validated data formats before parsing (e.g., checking if Windows boot time is 14 digits)

3. **Improved Reliability:**
   - Integrated Python's `logging` module for comprehensive debugging
   - Implemented multiple fallback methods for uptime retrieval
   - Added validation checks for empty outputs and negative values
   - Used `Path` from `pathlib` for safer file operations
   - Created separate methods for each OS with specific exception handling

4. **Added Type Hints:**
   ```python
   def get_uptime(self) -> Optional[Tuple[int, int, int, int]]:
   def _convert_seconds_to_tuple(uptime_seconds: int) -> Tuple[int, int, int, int]:
   ```

5. **Enhanced Documentation:**
   - Added docstrings to all methods
   - Documented return types and exceptions
   - Added inline comments for complex logic

---

## Testing Strategy

### Test Cases Executed

**1. Linux Platform Testing:**
- ✅ Verified `/proc/uptime` file reading on Linux systems
- ✅ Tested fallback to `uptime` command when `/proc/uptime` is unavailable
- ✅ Verified permission error handling when file is not readable
- ✅ Tested with various uptime values (newly booted, long running systems)

**2. macOS Platform Testing:**
- ✅ Tested `uptime -p` command execution
- ✅ Verified fallback mechanism when command fails
- ✅ Tested timeout behavior with mocked slow responses
- ✅ Verified error handling for missing command

**3. Windows Platform Testing:**
- ✅ Tested `wmic os get lastbootuptime` command
- ✅ Verified boot time parsing and validation
- ✅ Tested negative uptime detection (system clock set to past)
- ✅ Verified timeout handling for slow wmic responses

**4. Security Testing:**
- ✅ Verified no shell injection vulnerabilities with special characters
- ✅ Tested permission denial handling
- ✅ Verified subprocess timeout prevents hanging
- ✅ Tested format validation before parsing

**5. Error Handling Testing:**
- ✅ Missing files and directories
- ✅ Command timeouts (5-10 seconds)
- ✅ Empty or malformed command outputs
- ✅ Invalid date/time formats
- ✅ Keyboard interrupt (Ctrl+C)
- ✅ Unexpected exceptions

**6. Logging Testing:**
- ✅ INFO level logs for normal operations
- ✅ WARNING level logs for fallback mechanisms
- ✅ ERROR level logs for failures
- ✅ CRITICAL level logs for unexpected errors

### Test Results Summary

| Test Category | Status | Notes |
|---------------|--------|-------|
| Linux Support | ✅ PASS | `/proc/uptime` parsing works correctly |
| macOS Support | ✅ PASS | `uptime -p` command executes reliably |
| Windows Support | ✅ PASS | Boot time calculation accurate |
| Security | ✅ PASS | No injection vulnerabilities detected |
| Error Handling | ✅ PASS | All edge cases handled gracefully |
| Logging | ✅ PASS | Comprehensive logging output |
| Performance | ✅ PASS | Executes within timeout limits |

---

## How to Run the Script

### Prerequisites

- Python 3.7 or higher
- Cross-platform compatible (Linux, macOS, Windows)
- No external dependencies required (uses only Python standard library)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sathc-deloitte/test-copilot.git
   cd test-copilot
   ```

2. **Verify Python installation:**
   ```bash
   python3 --version
   ```

### Running the Script

**Basic Usage:**
```bash
python3 copilot_test.py
```

**With Logging Output:**
```bash
python3 copilot_test.py
```

The script will automatically detect your operating system and retrieve the system uptime.

### Expected Output

**Linux/macOS Example:**
```
==================================================
System: Linux
Uptime: 45 day(s), 3 hour(s), 22 minute(s), 15 second(s)
Total Uptime: 3894135 seconds
==================================================
```

**Windows Example:**
```
==================================================
System: Windows
Uptime: 12 day(s), 5 hour(s), 47 minute(s), 30 second(s)
Total Uptime: 1047850 seconds
==================================================
```

### Running with Custom Logging Levels

To modify logging verbosity, edit the logging configuration in the script:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG, WARNING, or ERROR as needed
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Troubleshooting

**Script hangs:**
- The script has built-in timeouts (5-10 seconds) for subprocess calls
- If it still hangs, check system permissions and available commands

**Permission denied error:**
- On Linux: Ensure read access to `/proc/uptime`
- On macOS/Windows: Ensure necessary commands (`uptime`, `wmic`) are available

**Empty output:**
- Check the logging output for error messages
- Verify your Python version is 3.7 or higher

---

## Key Takeaways from Using Copilot

### What Worked Well

1. **Rapid Prototyping**: Copilot quickly generated working cross-platform code
2. **Logic Structure**: The OS detection and method separation were well-organized
3. **Documentation**: Generated code included helpful comments and clear function names

### Areas for Improvement

1. **Security by Default**: Initial code used unsafe methods (`os.popen()`) - security should be built-in
2. **Error Handling**: Needed more comprehensive exception handling
3. **Type Safety**: Lacked type hints which would help catch bugs early
4. **Testing Considerations**: No logging or debugging output built-in

### Recommendations for Using Copilot

1. **Review generated code for security vulnerabilities** before deployment
2. **Add error handling and logging** even for simple scripts
3. **Use type hints** to improve code reliability
4. **Implement fallback mechanisms** for critical functionality
5. **Test on all target platforms** before using in production

---

## Files

- **copilot_test.py**: Main script with system uptime functionality
- **README.md**: This documentation file

---

## License

This project is open source and available under the MIT License.

---

## Contact

Created by: sathc-deloitte  
Repository: [test-copilot](https://github.com/sathc-deloitte/test-copilot)
