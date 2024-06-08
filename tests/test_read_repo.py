from pathlib import Path

from repo_find_orphans.manifest import Manifest
from repo_find_orphans.scan import find_local_orphans
from repo_find_orphans.types.project import Project


def test_custom_remote_is_set(projects: list[Project]):
    repo_common: Project = next(project for project in projects if project.name == "slack-sender.git")
    assert repo_common.remote.name == "bbuck"


def test_project_has_all_elements(projects: list[Project]):
    repo_common = next(project for project in projects if project.name == "repo-common.git")
    assert repo_common.name == "repo-common.git"
    assert repo_common.path == "repo"
    assert repo_common.remote.name == "origin"
    assert repo_common.revision == "master"


def test_read_manifest(manifest: Manifest):
    assert manifest.defaults["remote"] == "origin"
    assert manifest.defaults["revision"] == "master"
    assert len(manifest.projects) == 11
    assert len(manifest.remotes) == 3


def test_remotes_are_parsed_correctly(manifest: Manifest):
    remotes = manifest.remotes
    ghpub = next(remote for remote in remotes if remote.name == "ghpub")
    assert ghpub.name == "ghpub"
    assert ghpub.fetch == "https://github.com/"


def test_get_projects_for_remote(manifest: Manifest):
    projects = manifest.get_projects_for_remote("origin")
    assert len(projects) == 7

    projects = manifest.get_projects_for_remote("ghpub")
    assert len(projects) == 3

    projects = manifest.get_projects_for_remote("bbuck")
    assert len(projects) == 1


def test_project_account_is_right_for_remote(manifest: Manifest):
    projects = manifest.get_projects_for_remote("origin")
    assert projects[0].host_account == "vladistan"

    projects = manifest.get_projects_for_remote("ghpub")
    assert projects[0].host_account == "dcreager"

    projects = manifest.get_projects_for_remote("bbuck")
    assert projects[0].host_account == "Unknown"


def test_can_get_proj_canonical_form(manifest: Manifest):
    projects = manifest.get_projects_for_remote("origin")
    assert projects[0].host_account == "vladistan"
    assert projects[0].canonical_form == "vladistan/repo-common.git"


def test_finds_new_projects(project_path: Path, projects: list[Project]):
    file_list = find_local_orphans(project_path, projects)
    # Ignore dirs that are listed in the proj path
    assert Path("repo") not in file_list
    # Including ones deep in the hierarchy
    assert Path("archive/arm/uboot") not in file_list
    # Ignore dirs that do not contain files
    assert Path("deep") not in file_list
    # Find all the dirs that don't meet above criteria,
    assert Path("new-proj") in file_list
    # Including ones deep in the hierarchy
    assert Path("deep/np2") in file_list


def test_find_all_github_remotes(manifest: Manifest):
    remotes = manifest.remotes_by_type(host_type="github")
    assert len(remotes) == 2
    assert remotes[0].host_account == "vladistan"
