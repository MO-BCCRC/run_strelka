'''
Created on Sep 24, 2014

@author: jrosner
'''

import argparse


parser = argparse.ArgumentParser(
                    description='''run strelka software''')

parser.add_argument("--normal",
                    default=None, metavar='NORMAL.BAM',
                    required=True,
                    help= '''normal bam file''')

parser.add_argument("--tumor",
                    default=None, metavar='TUMOR.BAM',
                    required=True,
                    help= '''tumor bam file''')

parser.add_argument("--ref",
                    default=None, metavar='REF.FA',
                    required=True,
                    help= '''genome reference fasta file''')

parser.add_argument("--config",
                    default=None, metavar='CONFIG.INI',
                    help= '''strelka config file''')

parser.add_argument("--output_dir",
                    default=None, metavar='OUT.VCF',
                    required=True,
                    help='''basename of the vcf output file''')

parser.add_argument("--num_procs",
                    default=8,
                    help='''number of cores''')


args = parser.parse_args()


# $STRELKA_INSTALL_DIR/bin/configureStrelkaWorkflow.pl
# --normal=$nBAM
# --tumor=$tBAM
# --ref=$STRELKA_REF
# --config=$STRELKA_CONFIG
# --output-dir=$STRELKA_OUTDIR
