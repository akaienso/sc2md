#!/usr/bin/env python3
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
import argparse
import sys

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Inject source code into Markdown documents.")

# Define the optional arguments
parser.add_argument("-i", "--interactive", action="store_true", help="Enable interactive mode for confirmation before each injection.")
parser.add_argument("-l", "--extensions", type=str, help="Comma-separated list of file extensions to include. Example: -l php,scss,html")
parser.add_argument("-n", "--names", type=str, help="Comma-separated list of filenames to specifically inject. Example: -n functions.php,landing-page.php")

# Parse the arguments
args = parser.parse_args()

if args.interactive:
    print("Interactive mode enabled.")
if args.extensions:
    extensions = args.extensions.split(',')
    print("Filtering for extensions:", extensions)
if args.names:
    names = args.names.split(',')
    print("Specific files to inject:", names)

# Prompt for the Markdown file path
markdown_path = input("Enter the full path to the Markdown file (leave empty to create a new one): ").strip()

if markdown_path:
    # Check if the specified Markdown file exists
    if not os.path.exists(markdown_path):
        print(f"The specified Markdown file does not exist: {markdown_path}")
        create_new = input("Would you like to create this Markdown file? (y/n): ").strip().lower()
        if create_new == 'y':
            # Create a new Markdown file with a header based on the file name
            with open(markdown_path, 'w', encoding='utf-8') as md_file:
                md_file.write(f"# {os.path.basename(markdown_path)}\n\n")
            print(f"Created a new Markdown file: {markdown_path}")
        else:
            print("Please specify an existing Markdown file.")
            sys.exit()
else:
    # No path provided; prompt for a file name and create a new file in a default directory
    default_directory = r"C:\Users\rob\workbench\Notes\Obsidian\Member Minder Pro\inbox"
    filename = input("Enter a name for the new Markdown file: ").strip() + ".md"
    markdown_path = os.path.join(default_directory, filename)
    with open(markdown_path, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# {filename}\n\n")
    print(f"Created a new Markdown file: {markdown_path}")

# Prompt for the source code directory path
while True:
    source_code_dir_input = input("Enter the path to the root of the source code directory (required): ").strip()
    
    # Resolve the relative path to an absolute path immediately
    source_code_dir = os.path.abspath(source_code_dir_input)
    
    # Check if the resolved path is a valid directory
    if os.path.isdir(source_code_dir):
        break  # Valid directory provided, exit loop
    else:
        print(f"The specified path does not exist or is not a directory: {source_code_dir}")
        
        # Offer a second chance or the option to exit
        second_chance = input("Please provide a valid path, or press 'Enter' to exit the script: ").strip()
        if second_chance == '':
            print("Exiting the script. No changes made.")
            sys.exit()
        
        # Resolve the second chance input to an absolute path
        source_code_dir = os.path.abspath(second_chance)
        if os.path.isdir(source_code_dir):
            break  # Valid directory provided after second chance, exit loop
        else:
            print(f"The provided path does not exist or is not a directory: {source_code_dir}")
            # If the second chance is also invalid, the loop will continue prompting

# After determining markdown_path and source_code_dir
# Read the Markdown file into `lines`
with open(markdown_path, 'r') as md_file:
    lines = md_file.readlines()

def get_files_to_process(directory, extensions=None, names=None):
    excluded_extensions = ['log', 'tmp']  # Add any other extensions you wish to exclude
    files_to_process = []
    for root, dirs, files in os.walk(directory, topdown=True):
        # Exclude hidden directories from dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            # Skip hidden files and files with excluded extensions
            if file.startswith('.') or file.split('.')[-1] in excluded_extensions:
                continue
            if extensions and not file.split('.')[-1] in extensions:
                continue
            if names and file not in names:
                continue
            files_to_process.append(os.path.join(root, file))
    return files_to_process

extensions = args.extensions.split(',') if args.extensions else None
names = args.names.split(',') if args.names else None
files_to_process = get_files_to_process(source_code_dir, extensions, names)

# Keep the regex pattern for any Markdown header
any_header_pattern = r'^#+ '

# Initialize a counter for processed files
processed_files_count = 0
# Initialize a variable to track the last insertion index
last_insertion_index = len(lines) - 1
# Ensure you have the base source code directory as an absolute path for consistency
base_source_code_dir = os.path.abspath(source_code_dir)
processed_files_count = 0
last_processed_filename = None  # This will hold the filename of the last file processed

# Loop through each file to be processed
for sourcecode_path in files_to_process:
    # Calculate the relative path of the source code file from the base source code directory
    relative_path = os.path.relpath(sourcecode_path, start=base_source_code_dir)
    print(f"Processing {relative_path}...")  # Update to use relative path

    # Update last_processed_filename with the current file's name
    last_processed_filename = os.path.basename(sourcecode_path)

    if args.interactive:
        confirm = input(f"Inject {relative_path} into the Markdown file? (y/n): ")
        if confirm.lower() != 'y':
            continue

    try:
        with open(sourcecode_path, 'r', encoding='utf-8') as file:
            sourcecode_content = file.read()
        
        # Escape code block delimiters in the source code content
        sourcecode_content = sourcecode_content.replace("```", "`\u200B``")
        
    except UnicodeDecodeError:
        print(f"Skipping {relative_path} due to encoding issues.")
        continue

    # Use the relative path in the injection point pattern
    injection_point_pattern = r'^#+ ' + re.escape(relative_path.replace("\\", "/")) + r'$'
    injection_point_found = False

    for i, line in enumerate(lines):
        if re.match(injection_point_pattern, line.strip()):
            injection_point_index = i + 1
            injection_point_found = True
            break

    # Construct the source code block
    file_extension = os.path.splitext(relative_path)[1][1:]  # Update for consistency with relative path use
    sourcecode_block = f"```{file_extension}\n{sourcecode_content}\n```\n"

    if injection_point_found:
        # Insert the source code content at the found injection point
        lines.insert(injection_point_index, sourcecode_block)
        last_insertion_index = injection_point_index
    else:
        # Update to use relative path in the new header
        new_header = f"### {relative_path.replace('\\', '/')}\n"  # Ensure forward slashes
        new_content = f"{new_header}{sourcecode_block}\n"
        if last_insertion_index < len(lines) - 1:
            lines.insert(last_insertion_index + 1, new_content)
        else:
            lines.append(new_content)
        last_insertion_index = len(lines)

    # Increment the processed files count for each file processed
    processed_files_count += 1
    
# ANCHOR: Markdown File Writing
# Write the modified content back to the Markdown file, updating it with the inserted source code code blocks.
with open(markdown_path, 'w', encoding='utf-8') as md_file:
    md_file.writelines(lines)
    
# Extract markdown_filename from markdown_path
markdown_filename = os.path.basename(markdown_path)
# After processing all files, construct the confirmation message
if processed_files_count > 1:
    process_result = f"{processed_files_count} files have been"
elif processed_files_count == 1:
    # Use last_processed_filename for a specific message when exactly one file was processed
    process_result = f"'{last_processed_filename}' has been"
else:
    process_result = "No files have been"

confirmation_message = f"Process complete. {process_result} added to '{os.path.basename(markdown_path)}'."

# Print the confirmation message
print(confirmation_message)
print(f"PATH: {markdown_path}")