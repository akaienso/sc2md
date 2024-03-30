# Source Code to Markdown Processor  _(sc2md)_

## Overview

The **Source Code to Markdown Processor  _(sc2md)_** is a Python script designed to automate the process of injecting source code into specific, readable, and foldable code-block sections of a Markdown file. It supports the documentation of various programming languages within a Markdown-based documentation system. By reading specified Markdown files and locating headers corresponding to source code filenames, it formats and inserts file contents as code blocks. This script is configurable and adaptable to different environments, making it an essential tool for developers looking to streamline their documentation process.

## Features

- Automated injection of source code into Markdown files.
- Supports various programming languages.
- Configurable environments for flexible use cases.
- Simplifies documentation of code within Markdown.

## Installation

To use the **sc2md**, follow these steps:

1. Clone the repository to your local machine:

   ```sh
   git clone https://github.com/akaienso/sc2md.git
   ```

2. Ensure Python 3.6 or later is installed on your system. You can download Python [here](https://www.python.org/downloads/).

3. Navigate to the script's directory:

   ```sh
   cd sc2md
   ```

4. (Optional) Set up a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## Usage

Before running the script, ensure the environment settings and file paths are correctly configured for your project structure.

To execute the script, run:

```sh
python sc2md.py
```

For detailed usage instructions, best practices, and configuration options, refer to the [comprehensive guide](https://wp.rmoore.dev/projects/py/sc2md).

## Contributing

Contributions to the **sc2md** are welcome! Here are a few ways you can help:

- Report bugs and issues.
- Suggest new features or improvements.
- Contribute to the code via pull requests.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests to us.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was created with the help of ChatGPT prompts. For more information, visit [ChatGPT](https://chat.openai.com/share/f705dd93-2f56-44a2-85d3-64c0388c4b85).

## Contact

For any questions or feedback, please contact Rob Moore at [io@rmoore.dev](mailto:io@rmoore.dev).

Thank you for your interest in our project!
