'''
Created on Sep 10, 2014

@author: jrosner
'''
input_files  = {'normal': '__REQUIRED__',
                'tumor':  '__REQUIRED__',
                'ref':    '__REQUIRED__',
                'config': None}

output_files = {'output_dir':'__REQUIRED__'}

input_params = {'num_procs': 8,
                'isSkipDepthFilters': '__FLAG__'}

return_value = []
