import os
import pkg_resources
from pip.basecommand import Command
from pip.log import logger
from pip.commands.output import ConsoleOutput
from pip.commands.output.show import TextFormat


class ShowCommand(Command):
    """Show information about one or more installed packages."""
    name = 'show'
    usage = """
      %prog [options] <package> ..."""
    summary = 'Show information about installed packages.'

    def __init__(self, *args, **kw):
        super(ShowCommand, self).__init__(*args, **kw)
        self.cmd_opts.add_option(
            '-f', '--files',
            dest='files',
            action='store_true',
            default=False,
            help='Show the full list of installed files for each package.')

        self.console = ConsoleOutput(self.cmd_opts, output_formatters=[TextFormat()])

        self.parser.insert_option_group(0, self.cmd_opts)

    def run(self, options, args):
        self.console.set_output_type_based_on(options)
        if not args:
            logger.warn('ERROR: Please provide a package name or names.')
            return
        query = args

        results = self.search_packages_info(query, options.files)
        self.console.notify_packages_infos(results, options.files)
        self.console.notify_output_end()

    def search_packages_info(self, query, list_all_files):
        """
        Gather details from installed distributions. Print distribution name,
        version, location, and installed files. Installed files requires a
        pip generated 'installed-files.txt' in the distributions '.egg-info'
        directory.
        """
        installed_packages = dict(
            [(p.project_name.lower(), p) for p in pkg_resources.working_set])
        for name in query:
            normalized_name = name.lower()
            if normalized_name in installed_packages:
                dist = installed_packages[normalized_name]
                package = {
                    'name': dist.project_name,
                    'version': dist.version,
                    'location': dist.location,
                    'requires': [dep.project_name for dep in dist.requires()],
                }
                if list_all_files:
                    filelist = os.path.join(
                        dist.location,
                        dist.egg_name() + '.egg-info',
                        'installed-files.txt')
                    if os.path.isfile(filelist):
                        package['files'] = []
                        for line in open(filelist):
                            package['files'].append(line.strip())
                    else:
                        package['files'] = None
                yield package
