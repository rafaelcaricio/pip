from pip.log import logger

class ConsoleOutput:
    delegation_marker = 'notify_'

    def __init__(self, cmd_opts, output_formatters=[]):
        self.formatter = None
        self.output_formatters = output_formatters

        formats_available = self.formats_available()
        cmd_opts.add_option('--output',
            action='store',
            default=formats_available[0],
            choices=formats_available,
            help='Output type to render: ' + ', '.join(formats_available) + '.')

    def formats_available(self):
        return [formatter.format_type for formatter in self.output_formatters]

    def set_output_type_based_on(self, options):
        for formatter in self.output_formatters:
            if formatter.format_type == options.output:
                self.formatter = formatter

    def __getattr__(self, attr_name):
        if attr_name.startswith(self.delegation_marker):
            method_name = attr_name.replace(self.delegation_marker, '')
            return getattr(self.formatter, method_name)


class CommandOutput:
    def output(self, text):
        logger.notify(text)

    def output_end(self):
        pass
