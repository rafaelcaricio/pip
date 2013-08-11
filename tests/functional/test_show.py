import re
from pip import __version__
from pip.commands.show import ShowCommand
from pip.baseparser import create_main_parser
from tests.lib import reset_env, run_pip


def test_show():
    """
    Test end to end test for show command.

    """
    reset_env()
    result = run_pip('show', 'pip')
    lines = result.stdout.split('\n')
    assert len(lines) == 6
    assert lines[0] == '---', lines[0]
    assert lines[1] == 'Name: pip', lines[1]
    assert lines[2] == 'Version: %s' % __version__, lines[2]
    assert lines[3].startswith('Location: '), lines[3]
    assert lines[4] == 'Requires: '


def test_show_with_files_not_found():
    """
    Test for show command with installed files listing enabled and
    installed-files.txt not found.

    """
    reset_env()
    result = run_pip('show', '-f', 'pip')
    lines = result.stdout.split('\n')
    assert len(lines) == 8
    assert lines[0] == '---', lines[0]
    assert lines[1] == 'Name: pip', lines[1]
    assert lines[2] == 'Version: %s' % __version__, lines[2]
    assert lines[3].startswith('Location: '), lines[3]
    assert lines[4] == 'Requires: '
    assert lines[5] == 'Files:', lines[4]
    assert lines[6] == 'Cannot locate installed-files.txt', lines[5]


def test_show_with_all_files():
    """
    Test listing all files in the show command.

    """
    reset_env()
    result = run_pip('install', 'initools==0.2')
    result = run_pip('show', '--files', 'initools')
    assert re.search(r"Files:\n(  .+\n)+", result.stdout)


def test_missing_argument():
    """
    Test show command with no arguments.

    """
    reset_env()
    result = run_pip('show')
    assert 'ERROR: Please provide a package name or names.' in result.stdout


def show_cmd():
    return ShowCommand(create_main_parser())


def test_find_package_not_found():
    """
    Test trying to get info about a nonexistent package.

    """
    result = show_cmd().search_packages_info(['abcd3'], False)
    assert len(list(result)) == 0


def test_search_any_case():
    """
    Search for a package in any case.

    """
    result = list(show_cmd().search_packages_info(['PIP'], False))
    assert len(result) == 1
    assert 'pip' == result[0]['name']


def test_more_than_one_package():
    """
    Search for more than one package.

    """
    result = list(show_cmd().search_packages_info(['Pip', 'Nose', 'Virtualenv'], False))
    assert len(result) == 3
