# Ultimate Bruteforcer
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](https://github.com/yourusername/bruteforce-tool/pulls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/bruteforce-tool/pulls)

**⚠️ Legal Notice**: Ultimate Bruteforcer is intended **solely for ethical hacking and authorized penetration testing**. Unauthorized use against systems without explicit written permission is illegal and may violate laws such as the Computer Fraud and Abuse Act (CFAA) or GDPR. Always obtain written consent from the system owner before use.

## Overview

Ultimate Bruteforcer is a Python-based command-line tool designed for ethical hackers to test the security of authentication systems (e.g., web login forms, HTTP Basic, or Digest Authentication) with explicit permission. It supports brute forcing usernames and passwords using customizable wordlists, multithreading with thread pooling for speed, proxy support, CSRF token handling, CAPTCHA detection, and logging. The tool is optimized for performance while incorporating ethical safeguards to minimize impact on target systems.

### Features

- **Command-Line Interface**: Subcommands for updating wordlists (`update`) and running brute force attacks (`run`).
- **Authentication Types**:
  - Form-based (POST requests with customizable field names).
  - HTTP Basic Authentication.
  - HTTP Digest Authentication.
- **Wordlist Management**:
  - Supports single usernames or files (e.g., `usernames.txt`).
  - Password files (e.g., `rockyou.txt`).
  - Downloads wordlists from SecLists (RockYou for passwords, top-usernames-shortlist for usernames).
- **CSRF Token Handling**: Automatically fetches and includes CSRF tokens for form-based logins.
- **Optimized Multithreading**: Uses `ThreadPoolExecutor` and a work queue for efficient, high-speed parallel attempts (default: 10 threads).
- **Rate Limiting Mitigation**: Detects HTTP 429 (Too Many Requests) with exponential backoff (1s, 2s, 4s) and configurable delays (default: 0.5s).
- **Proxy Support**: Routes requests through a specified proxy for anonymization.
- **User-Agent Rotation**: Randomizes user agents to mimic different browsers and evade detection.
- **Customizable Form Fields**: Configurable field names for username, password, and CSRF tokens.
- **Success/Failure Detection**: Uses a user-specified failure identifier and HTTP status codes (200, 301, 302).
- **CAPTCHA Detection**: Pauses on detecting CAPTCHA prompts (default: 300s pause).
- **Logging**: Saves results to a timestamped log file (e.g., `ultimate_bruteforcer_20250526_115100.log`).
- **Error Handling**: Robustly handles network, file, and parsing errors.
- **Ethical Safeguards**: Configurable threads and delays to minimize system impact.

## Installation

Follow these step-by-step instructions to set up Ultimate Bruteforcer.

### Step 1: Prerequisites
- **Python**: Version 3.8 or higher.
- **Dependencies**: The `requests` library for HTTP requests.
- **Wordlists**: Optional but recommended (e.g., RockYou for passwords, usernames list).
- **System**: A system with sufficient CPU cores for multithreading (e.g., 4+ cores for optimal performance).
- **Git**: For cloning the repository (optional if downloading manually).

### Step 2: Clone the Repository
Clone the Ultimate Bruteforcer repository from GitHub to your local machine.

```bash
git clone https://github.com/yourusername/ultimate-bruteforcer.git
cd ultimate-bruteforcer
```

**Note**: Replace `yourusername` with your actual GitHub username or the repository URL.

### Step 3: Install Dependencies
Install the required Python library using pip.

```bash
pip install requests
```

**Verification**: Ensure `requests` is installed by running:
```bash
pip show requests
```

### Step 4: Download Wordlists
Download wordlists for usernames and passwords using the `update` subcommand. This fetches `rockyou.txt` and `usernames.txt` from SecLists.

```bash
python bruteforce.py update
```

**Output**:
```
[+] Downloading latest rockyou.txt for Ultimate Bruteforcer...
[+] Saved to wordlists/rockyou.txt
[+] Downloading latest usernames.txt for Ultimate Bruteforcer...
[+] Saved to wordlists/usernames.txt
```

**Note**: Wordlists are saved in the `wordlists/` directory. You can use custom wordlists by placing them in this folder or elsewhere and specifying their paths.

### Step 5: Verify Directory Structure
Ensure the project directory is set up correctly:
```
ultimate-bruteforcer/
├── bruteforce.py       # Main script
├── utils.py            # Helper functions
├── wordlists/          # Wordlist storage
│   ├── rockyou.txt
│   ├── usernames.txt
├── ultimate_bruteforcer_*.log  # Log files (generated during runs)
```

## Usage

Ultimate Bruteforcer provides two subcommands: `update` (downloads wordlists) and `run` (performs brute force attacks). Below are step-by-step instructions for using the tool.

### Step 1: Prepare the Target
Before running the tool, gather information about the target authentication system (with permission):
- **URL**: The login endpoint (e.g., `https://example.com/login`).
- **Authentication Type**: Form-based, Basic, or Digest.
- **Form Fields**: Names of username, password, and CSRF token fields (if applicable).
- **Failure Identifier**: Text in the response indicating a failed login (e.g., “Invalid credentials”).
- **CAPTCHA Identifier**: Text indicating a CAPTCHA prompt (e.g., “Please complete the CAPTCHA”).
- **CSRF URL**: URL to fetch the CSRF token (if needed).

**Tip**: Use a tool like Burp Suite or browser developer tools to inspect the login page and identify these parameters.

### Step 2: Update Wordlists (Optional)
If you haven’t already, download wordlists:
```bash
python bruteforce.py update
```

Alternatively, use custom wordlists tailored to the target’s password policy (e.g., generated with `Crunch`).

### Step 3: Run a Brute Force Attack
Use the `run` subcommand to perform the brute force attack. Below are example commands for different scenarios.

#### Example 1: Form-based Login
```bash
python bruteforce.py run \
  --url https://example.com/login \
  --user wordlists/usernames.txt \
  --passlist wordlists/rockyou.txt \
  --fail-identifier "Invalid credentials" \
  --captcha-identifier "Please complete the CAPTCHA" \
  --threads 20 \
  --delay 0.3 \
  --proxy http://127.0.0.1:8080 \
  --auth-type form \
  --csrf-field csrf_token \
  --csrf-url https://example.com/login
```

**Explanation**:
- Targets a form-based login with CSRF token.
- Uses 20 threads and a 0.3-second delay for speed.
- Routes requests through a proxy for anonymization.
- Pauses for 300 seconds if a CAPTCHA is detected.

#### Example 2: Basic Authentication
```bash
python bruteforce.py run \
  --url https://example.com/api \
  --user admin \
  --passlist wordlists/rockyou.txt \
  --fail-identifier "Unauthorized" \
  --auth-type basic \
  --threads 15 \
  --delay 0.2
```

**Explanation**:
- Tests Basic Authentication with a single username.
- Uses 15 threads and a 0.2-second delay for faster execution.

#### Command-Line Arguments (for `run`)
| Argument              | Description                                      | Required | Default        |
|-----------------------|--------------------------------------------------|----------|----------------|
| `--url`               | Target login URL (e.g., https://example.com/login) | Yes      | -              |
| `--user`              | Single username or path to usernames file        | Yes      | -              |
| `--passlist`          | Path to password list file                       | Yes      | -              |
| `--user-field`        | Form field name for username                    | No       | `username`     |
| `--pass-field`        | Form field name for password                    | No       | `password`     |
| `--fail-identifier`   | Text in response indicating failed login         | Yes      | -              |
| `--captcha-identifier`| Text indicating CAPTCHA prompt                   | No       | -              |
| `--captcha-pause`     | Pause duration (seconds) on CAPTCHA detection    | No       | 300.0          |
| `--threads`           | Number of parallel threads                      | No       | 10             |
| `--delay`             | Delay between requests (seconds)                | No       | 0.5            |
| `--proxy`             | Proxy URL (e.g., http://127.0.0.1:8080)         | No       | -              |
| `--auth-type`         | Authentication type (form, basic, digest)        | No       | `form`         |
| `--csrf-field`        | CSRF token form field name                      | No       | -              |
| `--csrf-url`          | URL to fetch CSRF token                         | No       | -              |

### Step 4: Monitor Output
- **Console**: Displays real-time results:
  - `[+] SUCCESS: username:password` for successful logins.
  - `[-] Failed: username:password` for failed attempts.
  - `[!] Error: message` for errors (e.g., network issues).
  - `[!] CAPTCHA detected` or `[!] Rate limit detected` with pause details.
- **Log File**: Saves detailed results to `ultimate_bruteforcer_YYYYMMDD_HHMMSS.log` (e.g., `ultimate_bruteforcer_20250526_115100.log`).

**Example Log Entry**:
```
2025-05-26 11:51:00,123 - INFO - SUCCESS: admin:password123 (Status: 200)
2025-05-26 11:51:01,456 - INFO - Failed: admin:123456 (Status: 401)
2025-05-26 11:51:02,789 - WARNING - CAPTCHA detected for user1:password
```

### Step 5: Analyze Results
- Review the log file for successful logins, errors, or CAPTCHA detections.
- Use findings to prepare a report for the system owner, recommending mitigations (e.g., stronger passwords, MFA).

## How It Works

1. **Initialization**:
   - Parses command-line arguments to configure the attack.
   - Sets up logging to a timestamped file.

2. **Wordlist Loading**:
   - Loads usernames (single or from file) and passwords from a file, handling UTF-8 encoding errors.

3. **Work Queue**:
   - Loads all username-password combinations into a `Queue` for efficient distribution.

4. **Thread Pooling**:
   - Uses `ThreadPoolExecutor` with `args.threads` workers (default: 10).
   - Each worker thread:
     - Uses its own `requests.Session` for connection reuse.
     - Fetches tasks from the queue and calls `try_login`.
     - Respects `args.delay` (default: 0.5s) between requests.

5. **Login Attempts**:
   - Constructs HTTP requests (POST for forms, GET for Basic/Digest) with random user-agent and optional proxy.
   - Fetches CSRF tokens for form-based logins.
   - Checks for CAPTCHAs and pauses if detected.
   - Evaluates success (no `fail_identifier` or HTTP 200/301/302) or failure.
   - Handles HTTP 429 with exponential backoff (1s, 2s, 4s).

6. **Completion**:
   - Waits for all tasks to complete (`work_queue.join()`).
   - Logs and prints completion status.

## Performance Optimizations

- **Thread Pooling**: Uses `ThreadPoolExecutor` to reuse threads, reducing creation overhead and improving speed by 20-50% for large wordlists.
- **Work Queue**: Distributes tasks efficiently, minimizing idle threads and ensuring balanced load.
- **Per-Thread Sessions**: Avoids session contention, improving request throughput.
- **Exponential Backoff**: Reduces wait time for rate limits (e.g., from 60s to 1-4s for transient issues).
- **Example**: Testing 1M combinations (1000 usernames × 1000 passwords) with 20 threads could complete in ~10-12 minutes on an 8-core system, compared to ~20 minutes in the original version, depending on network latency.

## Ethical Hacking Guidelines

Ultimate Bruteforcer is designed for **authorized penetration testing only**. Follow these guidelines:

- **Obtain Explicit Permission**: Secure written consent from the system owner, defining the scope (e.g., target URLs, time frame).
- **Minimize Impact**: Use low thread counts (e.g., 10-20) and delays (e.g., 0.3-1.0s) to avoid disrupting the target. Adjust based on system capacity.
- **Respect Rate Limits**: The tool pauses on HTTP 429 and CAPTCHA detection to prevent denial-of-service-like behavior.
- **Secure Data Handling**: Delete log files and any discovered credentials after testing.
- **Responsible Disclosure**: Report findings securely to the client, recommending mitigations like MFA, CAPTCHAs, or stronger password policies.
- **Legal Compliance**: Adhere to laws (e.g., CFAA, GDPR) and the client’s terms of service.

**⚠️ Warning**: Unauthorized use is illegal and may result in severe legal consequences.

## Testing Recommendations

- **Controlled Environment**: Practice on platforms like OWASP Juice Shop or Damn Vulnerable Web App before targeting authorized systems.
- **Wordlists**: Use tailored wordlists (e.g., generated with `Crunch`) based on the target’s password policy.
- **Proxy Setup**: Use tools like Burp Suite or a SOCKS proxy for traffic analysis and anonymization (with permission).
- **Validation**: Inspect the target’s login page to confirm `fail_identifier`, `captcha_identifier`, and form field names.

## Limitations

- **No CAPTCHA Solving**: Pauses on CAPTCHA detection but does not solve CAPTCHAs (requires external services with permission).
- **Basic Lockout Detection**: Detects rate limits (HTTP 429) but not specific account lockout messages.
- **Static Failure Detection**: Relies on a consistent `fail_identifier`; dynamic error messages may cause false positives.
- **No MFA Support**: Ineffective against multi-factor authentication systems.

## Potential Enhancements

- **CAPTCHA Solving**: Integrate a CAPTCHA-solving API (with permission).
- **Account Lockout Detection**: Add support for detecting lockout messages to skip affected usernames.
- **Dynamic Response Parsing**: Support JSON responses or regex for flexible success/failure detection.
- **Progress Tracking**: Display progress (e.g., percentage of combinations tested).
- **Proxy Rotation**: Support a pool of proxies for better anonymization.

## Contributing

Contributions are welcome! Please submit pull requests or issues to improve the tool. Focus on:
- Adding features (e.g., proxy rotation, advanced error handling).
- Enhancing performance (e.g., async I/O with `aiohttp`).
- Improving ethical safeguards (e.g., better lockout detection).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, open an issue on GitHub or contact the maintainer at [your.email@example.com](mailto:your.email@example.com).

**⚠️ Reminder**: Use Ultimate Bruteforcer responsibly and only with explicit permission. Ethical hacking aims to improve security, not exploit it.
