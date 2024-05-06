# Repo Find Orphans

## Overview

*Repo Find Orphans* is a Python tool that supplements Google's `repo` project repository management tool (available at https://gerrit.googlesource.com/git-repo). Throughout the lifecycle of a project, developers may add subprojects to the repository without registering them in the repo manifest. These unregistered directories become orphans, ignored by the repo tool during synchronization and updates. *Repo Find Orphans* addresses this issue by identifying these orphan directories, enabling developers to add them to the project manifest and ensure they are tracked in future project activities.

## Installation
To install *Repo Find Orphans*, you have two options depending on your preference for Python package management.

1. **Using pip**:
   If you prefer to install it directly into your global Python environment or a virtual environment, you can use pip. Execute the following command in your terminal:
   ```
   pip install repo-find-orphans
   ```

2. **Using pipx**:
   For those who prefer to keep their Python global environment clean or want to install Python CLI tools in isolated environments, pipx is a great alternative. First, ensure you have pipx installed (you can install pipx with `pip install pipx` if you don't have it already). Then run:
   ```
   pipx install repo-find-orphans
   ```
   This method will install *Repo Find Orphans* in an isolated environment but still make it accessible from the command line.


## Usage

To use *Repo Find Orphans* after installation, you can easily scan for orphan directories by using the command-line interface provided. Here's how you can run the tool:

1. **Prepare your environment**:
   Ensure you have the manifest file and the project directory ready. The manifest file should list all the registered subprojects, and the project directory should be the root directory where your projects are located.

2. **Run the tool**:
   Open your terminal and execute the following command:
   ```
   repo-find-orphans scan-projects-cli --manifest-file PATH_TO_MANIFEST --project-dir PATH_TO_PROJECT_DIR
   ```
   Replace `PATH_TO_MANIFEST` with the path to your manifest file and `PATH_TO_PROJECT_DIR` with the path to your project directory.

   Example:
   ```
   repo-find-orphans scan-projects-cli --manifest-file ./manifest.xml --project-dir ./projects
   ```

   This command will scan the project directory and compare it against the manifest file. Any directories in the project directory that are not listed in the manifest file will be printed as orphan directories.

3. **Review the output**:
   The output will list all the orphan directories found during the scan. Review these directories and decide if you need to add them to your manifest file or handle them accordingly.

By following these steps, you can effectively manage and track all subprojects within your repository, ensuring that no directories are left untracked.
