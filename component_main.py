'''

Created on Sep 24, 2014

@author: jrosner

component for running strelka
'''

from kronos.utils import ComponentAbstract
import os


class Component(ComponentAbstract):

    def __init__(self, component_name='run_strelka', component_parent_dir=None, seed_dir=None):
        self.version = '1.2.0'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)


    def make_cmd(self, chunk=None):

        cmd = self.requirements['strelka']

        if hasattr(self.args, 'config') and self.args.config:
            config = self.args.config

        else:
            config = os.path.join(
                                  os.path.dirname(os.path.dirname(cmd)),
                                  'etc/strelka_config_bwa_default.ini'
                                  )

        strelka_args = ['--normal',     self.args.normal,
                        '--tumor',      self.args.tumor,
                        '--ref',        self.args.ref,
                        '--config',     config,
                        '--output-dir', self.args.output_dir,
                        '\n']

        cmd = ' '.join([cmd] + strelka_args)
        cmd = 'rm -fr %s\n' % self.args.output_dir + cmd
        cmd += 'cd %s\n' % self.args.output_dir

        if self.args.isSkipDepthFilters:
            cmd += 'sed -i "s/isSkipDepthFilters = 0/isSkipDepthFilters = 1/" config/run.config.ini\n'

        cmd += 'make -j %s\n' % self.args.num_procs

        # move strelka results to pipeline output directory
        cmd += 'mv -v results/*vcf ../'

        cmd_args = []

        return cmd, cmd_args


    def test(self):
        import component_test
        component_test.run()


def _main():
    comp = Component()
    # comp.test()
    comp.args = component_ui.args
    comp.run()


if __name__ == '__main__':
    import component_ui
    _main()
