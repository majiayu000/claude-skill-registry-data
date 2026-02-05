---
name: File and Folder Manager
description: A comprehensive skill for creating/deleting project folders and downloading files from URLs into them.
---

# File and Folder Manager

## Overview

This skill provides a robust suite of tools for managing the lifecycle of project-specific data within a Docker container. It is composed of two primary scripts:

1.  **`main_folder.py`**: Handles the creation and secure deletion of temporary project folders.
2.  **`main_file.py`**: Downloads files from a given URL directly into a specified project folder.

Together, they allow you to create a workspace, populate it with necessary files, and clean it up securely.

## When to Use This Skill

Use this skill when you need to:

-   Create temporary, isolated folders for different projects or jobs.
-   Download files from a URL into a specific project folder.
-   Securely delete project folders and their contents after processing is complete.
-   Manage persistent storage for temporary data using Docker volumes.

## Workflow Overview

The skill is divided into two main functionalities, each handled by its own script.

### 1. Folder Management (`main_folder.py`)

This script manages the project directories themselves.

-   **`create(project_id: str)`**
    -   **Purpose**: Create a temporary folder named after the specified project ID.
    -   **Input**: A unique Project ID string.
    -   **Output**: The path of the new folder created in the designated temporary directory (e.g., `/tmp/temp_files/temp_project_<project_id>`).

-   **`delete(project_id: str)`**
    -   **Purpose**: Delete the temporary folder associated with the project ID.
    -   **Input**: A unique Project ID string.
    -   **Output**: The specified project folder and all its contents are removed.

### 2. File Management (`main_file.py`)

This script downloads files from the web.

-   **`download(download_url: str, project_dir: str)`**
    -   **Purpose**: Download a file from a URL and save it to a specific local directory.
    -   **Input**:
        -   `download_url`: The full URL of the file to be downloaded.
        -   `project_dir`: The full path to an existing local directory where the file will be saved.
    -   **Output**: The file is downloaded and saved inside the `project_dir`.

## How to Run the Scripts

### 1. Managing Folders (`main_folder.py`)

Use command-line arguments to specify the mode and project ID.

```bash
# Create a folder for 'project123'
python main_folder.py --mode create --project_id project123

# Delete the folder for 'project123'
python main_folder.py --mode delete --project_id project123```

### 2. Downloading Files (`main_file.py`)

Provide the URL of the file, the target project directory, and optionally specify a filename.

```bash
# Download IFC JSON file with specific filename (as used in workflow)
python main_file.py --download_url "https://supabase.example.com/ifc-data.json" --project_dir "/tmp/temp_files/temp_project_project123" --filename "ifc_json_uuid.json"

# Download a file with URL-derived filename (backward compatibility)
python main_file.py --download_url "https://example.com/data/invoice.pdf" --project_dir "/tmp/temp_files/temp_project_project123"
```

## Configuration Options

-   **`ROOT_PATH`**: Environment variable for a custom root path for folder creation (used by `main_folder.py`).
-   **Default Path**: If `ROOT_PATH` is not set, it defaults to `/tmp/temp_files`.

## Error Handling

The scripts include built-in error handling for:

-   Invalid modes or missing project IDs (`main_folder.py`).
-   Invalid URLs or network failures during download (`main_file.py`).
-   File system errors (e.g., permissions, disk space).
-   Docker volume access errors.

## Usage Tips

-   **Recommended Workflow**:
    1.  Use `main_folder.py --mode create` to create a new project directory.
    2.  Use `main_file.py --download_url` to download one or more files into that directory.
    3.  Once your work is complete, use `main_folder.py --mode delete` to clean up the directory.
-   Ensure proper permissions for the target directories on your Docker host volume.
-   Always provide full, valid URLs for the download script.
