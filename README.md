# *Repo Find Orphans*

This is a simple tool that works alongside Google's
[repo](https://gerrit.googlesource.com/git-repo) multiple git
repository management tool. It addresses two problems:

* **Local Orphans:** Developers may add subprojects to the repository
without first registering them in the repo manifest. This is not a
recommended action in the repo workflow, but it does occur regularly
in large teams. These unregistered directories become orphans, and
the repo tool ignores them during synchronization and updates. This
tool deals with the issue by finding orphan directories, which
developers can then include in the project manifest for future
tracking.

* **Remote Orphans:** This tool can also search your GitHub account
for repositories that do not appear in your repo manifest. This is
useful for discovering repositories where you collaborate but are
not monitored by your repo project.


## **Breaking Changes:**

The version 0.1.0 introduces breaking changes to the CLI interface.

## Installation

There are two ways to install this tool:

1. **Using pip**:   this will install the tool into your active
virtual environment or to the the global python environment.  To
install with pip use the following command

```
   pip install repo-find-orphans
```


2. **Using pipx**: If you want to keep your Python global environment
clean or install Python CLI tools in isolated environments use the
pipx option.

  - First make sure pipx is installed

```
pip install pipx
```

   - Then install the tool

```
pipx install repo-find-orphans
```


This will create a dedicated virtual environment for the tool and add the executable script to your ~/.local/bin


## Usage

After the tool is installed use one of the following commands to find orphan projects.

### Finding Local Orphans

This function scans your local project directory and finds all projects in it. Then it consults the specified manifest file to see which projects exist in the directory but are not mentioned in the manifest.  Then it will print the list of such projects for your review and possible inclusion into the manifest. 

```
repo-find-orphans local MANIFEST_FILE PROJECT_DIR
```

Replace `MANIFEST_FILE` with the path to your manifest file, and `PROJECT_DIR` with the path to your project directory.



### Finding Remote Orphans

This function searches your GitHub account for repositories that do
not appear in your repo manifest. This is handy for finding
remote repositories on which you collaborate but are not monitored
by your repo project.  It uses 'selections.yaml'  file that allows
 specify which projects should be excluded from your remote scan.


For additional details, see [Remote Project
Selection](#remote-project-selection). In addition to the repositories
stored in your Github account, it scans all of the organizations
that you are a member of, as well as individual repositories that
you are added as a collaborator.


To invoke this function use the following command:

```
repo-find-orphans remote MANIFEST_FILE  PATH_TO_SELECTION_CONFIG
```

Replace `MANIFEST_FILE` with the path to your manifest file, and
`PATH_TO_SELECTION_CONFIG` with the path to your selection configuration
file.


#### Remote project selection

The `selections.yaml` file allows you to select which projects to
include or exclude from your remote scan.  The configuration file
consist of multiple top level sections, each section corresponds
to an account or organition under consideration. Each section can
contain an `include` or `exclude` subsection to further refine the
selection.  If neither `include` nor `exclude` sections are specified,
all projects from the organization will be included in the scan.

If either `include` or `exclude` is specified it is interpreted as follows:

- `include:` section is considered first.  If this section contains
a list of prefixes only the projects that match any of the prefixes
will be included in the scan.  If this section is empty or missing
all projects will be included.

- `exclude:` section is considered second.  This section contains
a list of prefixes as well.  If a name of a project matches any of
the prefixes in this section it will be excluded from the scan.  If
this section is empty or missing no projects will be excluded.
  
For example:


```yaml
Ebiquity:
  exclude:
    - procure
```

This configuration will include all projects of the Ebiquity
organization except for the ones starting with `procure`


```yaml
solmir:
  include:
    - bob
    - bill
```

This configuration will only include projects with names starting
with `bob` or `bill` from the `solmir` organization.

```yaml
reddit: {exclude: [""]}
```
This configuration will include all projects of the `reddit` organization. 

```yaml
apache:
  include:
     - accumulo
  exclude:
     - accumulo-examples
     - accumulo-pig
```

This configuration will include only the projects that start
`accumulo` from the `apache` organization, but exclude the
`accumulo-examples` and `accumulo-pig`.



# Troubleshooting

If you installed your tool using pipx, but get the `command not
found` error when you are trying to run it check that `~/.local/bin`
is in your shell search path. If it is not, run `pipx ensurepath`
to fix this

