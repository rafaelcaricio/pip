from pip.commands.output import CommandOutput


class ShowCommandOutput(CommandOutput):
    def packages_infos(self, distributions, list_all_files):
        """
        Print the informations from installed distributions found.
        """
        raise NotImplementedError


class TextFormat(ShowCommandOutput):
    format_type = 'text'

    def packages_infos(self, distributions, list_all_files):
        for dist in distributions:
            self.output("---")
            self.output("Name: %s" % dist['name'])
            self.output("Version: %s" % dist['version'])
            self.output("Location: %s" % dist['location'])
            self.output("Requires: %s" % ', '.join(dist['requires']))
            if list_all_files:
                self.output("Files:")
                if dist['files']:
                    for line in dist['files']:
                        self.output("  %s" % line.strip())
                else:
                    self.output("Cannot locate installed-files.txt")
