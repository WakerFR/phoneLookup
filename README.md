# Reverse Lookup Tool

🔍 A Python tool for performing reverse lookup of phone numbers to identify network providers and locations.

## Introduction

This tool utilizes web scraping techniques to fetch information from Comfi's reverse lookup service. It is designed to be multi-threaded and can optionally use proxies for better performance and anonymity.

## Features

- **Multi-threaded Processing**: Utilizes threading to handle multiple phone numbers concurrently.
- **Proxy Support**: Ability to use proxies for making requests.
- **Output**: Organizes results into directories based on country and network provider.

## Usage

### Prerequisites

- Python 3.x
- Required Python packages (`colorama`, `requests`, `beautifulsoup4`)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/reverse-lookup.git
   cd reverse-lookup
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
    ```
The requirements.txt file contains a list of Python packages required for this project. Running the above command will install all necessary dependencies.

If you prefer, you can manually install each package listed in requirements.txt using individual pip install commands.
3. Usage
For usage instructions and running the tool, refer to the Usage section in the README.
