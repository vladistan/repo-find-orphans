from pathlib import Path

import pytest
from repo_find_orphans.manifest import Manifest
from repo_find_orphans.types.project import Project


@pytest.fixture(scope="session")
def base_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def repo_xml(base_dir: Path) -> Path:
    return base_dir / "fixtures" / "repo" / "repo.xml"


@pytest.fixture(scope="session")
def selections_yaml(base_dir: Path) -> Path:
    return base_dir / "fixtures" / "repo" / "selections.yaml"


@pytest.fixture(scope="session")
def project_path(base_dir: Path) -> Path:
    return base_dir / "fixtures"


@pytest.fixture(scope="session")
def manifest(repo_xml: Path) -> Manifest:
    return Manifest(repo_xml)


@pytest.fixture(scope="session")
def projects(manifest: Manifest) -> list[Project]:
    return manifest.projects
