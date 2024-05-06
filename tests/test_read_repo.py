from pathlib import Path

import pytest
from repo_find_orphans.parse import parse_manifest
from repo_find_orphans.scan import scan_projects
from repo_find_orphans.types.project import Project


@pytest.fixture()
def repo_xml() -> Path:
    base_dir = Path(__file__).parent
    return base_dir / "fixtures" / "repo" / "repo.xml"


@pytest.fixture()
def project_path() -> Path:
    base_dir = Path(__file__).parent
    return base_dir / "fixtures"


@pytest.fixture()
def projects(repo_xml: Path) -> list[Project]:
    return parse_manifest(repo_xml)


def test_read_manifest(projects: list[Project]):
    assert len(projects) == 8


def test_finds_new_projects(project_path: Path, projects: list[Project]):
    file_list = scan_projects(project_path, projects)
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
