"""
Script Name: Source Code to Markdown Processor (sc2md)
Description: This script automates the process of injecting source code into specific readable and foldable code-block sections of a Markdown file. It is designed to facilitate the documentation of various programming languages and their usage within a Markdown-based documentation system. The script reads the specified Markdown file, locates headers corresponding to source code filenames, and inserts the file contents formatted as code blocks within the Markdown file. This process is configurable and relies on the current environment settings for both source code and Markdown files to determine the correct file paths.

Author: Rob Moore
Email: io@rmoore.dev
License: Apache License 2.0
Creation Date: 2024-03-18
Last Modified Date: 2024-03-30
Version: 1.0.0

For detailed usage instructions, best practices, and configuration options, please refer to the comprehensive guide available at:
https://wp.rmoore.dev/projects/py/sc2md

ChatGPT prompts were used in the creation of this script. For more information, visit:
https://chat.openai.com/share/f705dd93-2f56-44a2-85d3-64c0388c4b85

NOTE: Ensure that the environment settings and file paths are correctly configured for your project structure before running this script.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import re

# ANCHOR: Environment Setup
# Define current environments for source code and Markdown. These settings dictate which paths will be used for source code and Markdown files.
current_sourcecode_environment = 'dev'  # Possible values: 'dev', 'repo', 'dist'
current_markdown_environment = 'obsidian'  # Possible values: 'obsidian', 'dropbox'

# ANCHOR: source code Path Configuration
# source code environment directory paths. Modify these paths to match the locations on your system.
if current_sourcecode_environment == 'dev':
    # NOTE: Developer Tip - Ensure the development path is accessible and correct for your environment.
    sourcecode_env_path = r'C:\Users\rob\workbench\wordpress\local-sites\osdia-national-website\app\public\wp-content\themes\osdia\inc\nelagala'
elif current_sourcecode_environment == 'repo':
    # NOTE: Developer Tip - The repository path should point to the version-controlled source of your source code files.
    sourcecode_env_path = r'C:\Users\rob\workbench\client-sites\OSDIA\themes\osdia-theme\inc\nelagala'
elif current_sourcecode_environment == 'dist':
    # NOTE: Developer Tip - Distribution path is where the production-ready files reside, often in a staging or live environment.
    sourcecode_env_path = r'C:\Users\rob\Dropbox\Projects\NELAGala'

# ANCHOR: Markdown Path Configuration
# Similar to source code, configure the Markdown environment paths here.
if current_markdown_environment == 'obsidian':
    md_env_path = r'C:\Users\rob\workbench\Notes\Obsidian\Member Minder Pro\Client Sites\OSDIA\National\NELAGala'
elif current_markdown_environment == 'dropbox':
    md_env_path = r'C:\Users\rob\Dropbox\Notes\Work\MMP\Client Sites\OSDIA\National\NELAGala'

# ANCHOR: File Listings
# Define the lists of source code filenames and the single Markdown filename involved in the document generation process.
# NOTE: User Tip - Update this list to include any new source code files you need to process. Add or remove filenames as needed. 
sourcecode_filenames = ['functions.php', 'landing-page.php', 'template-parts/section-header.php', 'template-parts/section-about.php', 'template-parts/section-navigation.php', 'styles/main/styles.scss', 'styles/main/reset.scss', 'styles/main/styles.scss', 'styles/partials/_typography.scss', 'styles/partials/_variables.scss', 'styles/partials/_navbar-responsive.scss', 'styles/partials/_navigation.scss', 'styles/partials/_nelagala-design.scss', 'styles/partials/_header.css']
markdown_filename = 'NELAGala Dev Prompt.md'


# ANCHOR: Markdown Path Assembly
# Full path for the Markdown file. Combines the environment path and the Markdown filename.
markdown_path = os.path.join(md_env_path, markdown_filename)

# ANCHOR: Regex Pattern for Headers
# Define the regex pattern for finding any Markdown header. Used to locate injection points in the Markdown document.
any_header_pattern = r'^#+ '

# ANCHOR: Markdown File Reading
# Open and read the Markdown file specified by `markdown_path`.
with open(markdown_path, 'r') as md_file:
    lines = md_file.readlines()

# ANCHOR: source code File Processing
# Loop through each source code filename, read its contents, and insert it into the Markdown document at the appropriate location.
processed_files_count = 0
for sourcecode_filename in sourcecode_filenames:
    # Full path for the source code file
    sourcecode_path = os.path.join(sourcecode_env_path, sourcecode_filename)
    print(f"Reading {sourcecode_filename}...")
    processed_files_count += 1

    # Read the source code file content
    with open(sourcecode_path, 'r') as file:
        sourcecode_content = file.read()

    # NOTE: Developer Tip - Modify the regex pattern below if your document uses a different scheme for headers.
    injection_point_pattern = r'^#+ ' + re.escape(sourcecode_filename) + r'$'

    # Search for the exact place to inject the source code content within the Markdown file.
    injection_point = None
    for i, line in enumerate(lines):
        if re.match(injection_point_pattern, line.strip()):
            injection_point = i + 1
            break

    # If a matching header is found, find the next headline or EOF to replace the content
    if injection_point is not None:
        end_point = None
        for i in range(injection_point, len(lines)):
            if re.match(any_header_pattern, lines[i].strip()) and i != injection_point:  # Ensure it's not the same header
                end_point = i
                break
        
        # Prepare the source code content with code block formatting for Markdown.
        sourcecode_block = f"```php\n{sourcecode_content}\n```\n"
        
        # Replace or insert the source code content
        if end_point:
            # Replace content between headers
            lines = lines[:injection_point] + [sourcecode_block] + lines[end_point:]
        else:
            # No subsequent header, append everything after the injection point
            lines = lines[:injection_point] + [sourcecode_block]
            
print(f"Processed {processed_files_count} files.")

# ANCHOR: Markdown File Writing
# Write the modified content back to the Markdown file, updating it with the inserted source code code blocks.
with open(markdown_path, 'w') as md_file:
    print("Writing changes to the Markdown file...")
    md_file.writelines(lines)
    
print("All done! The Markdown file has been updated with the source code blocks.")
