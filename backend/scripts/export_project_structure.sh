#!/bin/bash

# File path for exported project structure file
EXPORT_FILE="/backend/structure.exported.txt"

# Define the root directory of your project
ROOT_DIR="."

# Define patterns to exclude (relative to ROOT_DIR)
EXCLUDE_PATTERNS=("*.log" "*.tmp" "node_modules" "venv" ".git" "__pycache__")

# Function to print the directory structure
print_structure() {
    local dir="$1"
    local indent="$2"

    # List all files and directories in the given directory
    for item in "$dir"/*; do
        # Check if item is a directory
        if [ -d "$item" ]; then
            local basename=$(basename "$item")
            # Check if the directory matches any exclude pattern
            if [[ ! " ${EXCLUDE_PATTERNS[@]} " =~ " ${basename} " ]]; then
                echo "${indent}${basename}/" >> "$EXPORT_FILE"
                # Recursively print the structure of the directory
                print_structure "$item" "    $indent"
            fi
        elif [ -f "$item" ]; then
            local basename=$(basename "$item")
            # Check if the file matches any exclude pattern
            should_exclude=false
            for pattern in "${EXCLUDE_PATTERNS[@]}"; do
                if [[ "$basename" == $pattern ]]; then
                    should_exclude=true
                    break
                fi
            done
            if [ "$should_exclude" = false ]; then
                echo "${indent}${basename}" >> "$EXPORT_FILE"
            fi
        fi
    done
}
# Clear the output file if it exists
> "$EXPORT_FILE"

# Print the project structure
print_structure "$ROOT_DIR" ""

# Apply all permissions for file to be exported
chmod 777 $EXPORT_FILE

# Notification of completion
echo "Project structure has been written to $EXPORT_FILE"
