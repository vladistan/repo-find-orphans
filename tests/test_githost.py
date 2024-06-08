from pathlib import Path

import pytest
from repo_find_orphans.manifest import Manifest
from repo_find_orphans.remote import GitHosting
from repo_find_orphans.scan import find_remote_orphans
from repo_find_orphans.selections import Selections


@pytest.fixture(scope="session")
def selections(selections_yaml: Path):
    return Selections(selections_yaml)


def test_parse_selections(selections: Selections):
    assert len(selections.selections) == 5


def test_unspecified_selection_allows_everything(selections: Selections):
    assert "repo-common" in selections["vladistan"]
    assert "kitchen" in selections["vladistan"]


def test_include_in_selection_automatically_exclude_the_rest(selections: Selections):
    assert "dotfiles-base" in selections["dcreager"]
    assert "dotfiles-private" in selections["dcreager"]
    assert "kitchen" not in selections["dcreager"]


def test_when_selection_only_excludes_admit_except_ones_on_excl_list(selections: Selections):
    assert "dotfiles-base" in selections["Ebiquity"]
    assert "log-parser" in selections["Ebiquity"]
    assert "rnaseq" in selections["Ebiquity"]
    assert "procure" not in selections["Ebiquity"]
    assert "procure-large" not in selections["Ebiquity"]
    assert "procure-excl" not in selections["Ebiquity"]


def test_complex_selection_case(selections: Selections):
    assert "dotfiles-base" not in selections["solmir"]
    assert "bob" in selections["solmir"]
    assert "bob-villa" in selections["solmir"]
    assert "bob-the-operator" not in selections["solmir"]
    assert "bob-the-operator-n1" not in selections["solmir"]
    assert "bill" in selections["solmir"]
    assert "bill-clinton" in selections["solmir"]
    assert "bill-gates" not in selections["solmir"]
    assert "bill-gates-n1" not in selections["solmir"]


def test_selections_with_account_prefix(selections: Selections):
    assert "vladistan/repo-common" in selections
    assert "vladistan/kitchen" in selections

    assert "dcreager/dotfiles-private" in selections
    assert "dcreager/kitchen" not in selections

    assert "Ebiquity/log-parser" in selections
    assert "Ebiquity/rnaseq" in selections
    assert "Ebiquity/procure" not in selections

    assert "solmir/bob-the-operator" not in selections
    assert "solmir/bob-the-operator-n1" not in selections
    assert "solmir/bill" in selections
    assert "solmir/bill-clinton" in selections


def __test_fetch_gh_repos():
    github = GitHosting()
    repos = github.get_repos()

    assert len(repos) > 180
    assert "vladistan/ambari" in repos
    assert "vladistan/repo-common" in repos
    assert "Ebiquity/AAR_NER" in repos
    assert "PrintLessPlans/kernel" in repos


def __test_find_remote_orphans(manifest: Manifest, selections: Selections):
    orphans = find_remote_orphans(manifest, selections)
    orphans = list(orphans)
    assert len(orphans) > 300
