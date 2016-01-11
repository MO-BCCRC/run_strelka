'''
Created on Sep 10, 2014

@author: jrosner
##tests for the miseqTsv2Vcf component
'''

import unittest
import component_reqs, component_main
import subprocess
import os
from collections import defaultdict

class args():
    def __init__(self):
        self.tumor      = '/sample/path/checks/make_cmd/tumor.bam'
        self.normal     = '/sample/path/checks/make_cmd/normal.bam'
        self.ref        = '/sample/path/checks/make_cmd/ref.fa'
        self.config     = '/sample/path/checks/make_cmd/config.ini'
        self.output_dir = '/sample/path/checks/make_cmd/out/'
        self.num_procs  = 8

class check_requirements(unittest.TestCase):
    def setUp(self):
        self.args = args()

    #make sure that the required fields are present in reqs file
    def test_verify_reqs(self):
        try:
            _ = component_reqs.env_vars
            _ = component_reqs.parallel
            _ = component_reqs.requirements
            _ = component_reqs.parallel_param
            #_ = component_reqs.parallel_mode
            _ = component_reqs.memory
            _ = component_reqs.version

        except:
            self.assertEqual(True, False, 'Please complete the requirements file')

    #The python version must be atleast 2.7.0
    def test_verify_python(self):
        cmd = component_reqs.requirements['python'] + ' -V'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cmdout, cmderr = proc.communicate()

        if (cmdout=='' and cmderr == '') or (cmdout != '' and cmderr != ''):
            self.assertEqual(True, False, 'Couldn\'t retreive the version information: '+cmdout+' '+cmderr)

        elif cmdout == '':
            val = cmderr.strip().split()[1].split('.')

        elif cmderr == '':
            val = cmderr.strip().split()[1].split('.')

        self.assertGreaterEqual(int(val[0]), 2, 'The major version of python must be 2 or greater')
        if int(val[0])>2:
            return

        self.assertGreaterEqual(int(val[1]), 7, 'The minor version of python must be 7 or greater')
        if int(val[0])>7:
            return

        self.assertGreaterEqual(int(val[1]), 5, 'The patch version of python must be 5 or greater')


    def test_make_cmd(self):
        comp = component_main.Component()
        comp.args = self.args
        cmd,cmd_args = comp.make_cmd()
        cmd_args = ' '.join(map(str,cmd_args))

        #The actual resulting command:
        # real_command ='python ' + os.path.abspath('./component_seed') + '/miseqTsv2Vcf.py'

        real_command = '{1} --normal {2} --tumor {3} --ref {4} --config {5} --output_dir {6}\n' \
                       'cd {6}' \
                       'make -j {7}'.format(
                                             component_reqs.requirements['strelka'],
                                             '/sample/path/checks/make_cmd/normal.bam',
                                             '/sample/path/checks/make_cmd/tumor.bam',
                                             '/sample/path/checks/make_cmd/ref.fa',
                                             '/sample/path/checks/make_cmd/config.ini',
                                             '/sample/path/checks/make_cmd/out/',
                                             8
                                             )

        real_command_args = []

        print 'cmd'
        print cmd
        print 'real'
        print real_command

        #Ensure that the commands match exactly
        self.assertEqual(real_command, cmd, 'Please recheck the cmd variable in make_cmd')

        self.assertEqual(real_command_args,cmd_args,'Please recheck the cmd_args list in make_cmd')

    def test_params(self):
        try:
            from component_params import input_files,input_params,output_files,return_value
        except:
            self.assertEqual(True,False,'Please complete the params file')

        try:
            import component_ui
        except:
            #cannot run this test if running in unittest mode as ui isn't available
            self.assertEqual(True, True, '')
            return

        arg_act = defaultdict(tuple)
        for val in component_ui.parser._actions[1:]:
            arg_act[val.dest] = (val.required,val.default)

            if val.required == None:
                self.assertEqual(val.default, None,
                                 'The optional argument: '+ val.dest+' has no default value')

        #merge all the dictionaries together
        params_dict = dict(input_files.items() + input_params.items() + output_files.items())

        for dest,(req,default) in arg_act.iteritems():

            if req == True:
                self.assertEqual(params_dict[dest], '__REQUIRED__', 'params and ui dont match')
            else:
                if not params_dict[dest] in [default,None]:
                    self.assertEqual(True, False, 'Please ensure that either default or ' +\
                                     '__OPTIONAL__ flag is provided for: '+params_dict[dest])

def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    checkreqs = loader.loadTestsFromTestCase(check_requirements)

    suite.addTests(checkreqs)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
