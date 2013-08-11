try:
  from StringIO import StringIO
except:
  from io import StringIO

from pip.commands.output.show import TextFormat


def test_when_should_list_all_files_and_files_not_located():
    distributions = [dict(
      name='pip',
      version='1.3.2',
      location='/some/dir',
      requires=['tox', 'mock'],
      files=None
    )]

    output = StringIO()
    text_formatter = TextFormat()
    text_formatter.output = output.write

    text_formatter.packages_infos(distributions, True)

    output_result = output.getvalue()
    assert 'Name: pip' in output_result
    assert 'Version: 1.3.2' in output_result
    assert 'Location: /some/dir' in output_result
    assert 'Requires: tox, mock' in output_result
    assert 'Files:' in output_result
    assert 'Cannot locate installed-files.txt' in output_result


def test_when_should_list_all_files_and_files_located():
    distributions = [dict(
      name='pip',
      version='1.3.2',
      location='/some/dir',
      requires=['tox', 'mock'],
      files=['../some/single_file.py']
    )]

    output = StringIO()
    text_formatter = TextFormat()
    text_formatter.output = output.write

    text_formatter.packages_infos(distributions, True)

    output_result = output.getvalue()
    assert 'Name: pip' in output_result
    assert 'Version: 1.3.2' in output_result
    assert 'Location: /some/dir' in output_result
    assert 'Requires: tox, mock' in output_result
    assert 'Files:' in output_result
    assert '../some/single_file.py' in output_result


def test_when_should_not_list_all_files():
    distributions = [dict(
      name='pip',
      version='1.3.2',
      location='/some/dir',
      requires=['tox', 'mock'],
      files=['../some/single_file.py']
    )]

    output = StringIO()
    text_formatter = TextFormat()
    text_formatter.output = output.write

    text_formatter.packages_infos(distributions, False)

    output_result = output.getvalue()
    assert 'Name: pip' in output_result
    assert 'Version: 1.3.2' in output_result
    assert 'Location: /some/dir' in output_result
    assert 'Requires: tox, mock' in output_result
    assert not 'Files:' in output_result
    assert not '../some/single_file.py' in output_result
