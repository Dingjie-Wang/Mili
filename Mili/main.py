import argparse
from TrEESR import TrEESR
from TransELS import TransELS
# import os
# os.system("taskset -p 0xfffff %d" % os.getpid())
# affinity_mask = os.sched_getaffinity(0)
# os.sched_setaffinity(0, affinity_mask)
def parse_arguments():
    """
    Parse the arguments
    """
    parser = argparse.ArgumentParser(description="Isoform quantification tools",add_help=True)
    subparsers = parser.add_subparsers(help='sub-command help',dest="subparser_name")
    parser_TrEESR = subparsers.add_parser('cal_K_value', help='Calculate K values')
    parser_TransELS = subparsers.add_parser('quantify', help='Isoform quantification')
    
    requiredNamed_TrEESR = parser_TrEESR.add_argument_group('required named arguments for calculation of K values')
    requiredNamed_TrEESR.add_argument('-gtf','--gtf_annotation_path', type=str, help="The path of annotation file",required=True)
    requiredNamed_TrEESR.add_argument('-lrsam','--long_read_sam_path', type=str, help="The path of long read sam file",required=True)
    requiredNamed_TrEESR.add_argument('-o','--output_path', type=str, help="The path of output directory",required=True)
    optional_TrEESR = parser_TrEESR.add_argument_group('optional arguments')
    optional_TrEESR.add_argument('-t','--threads',type=int, default=1,help="Number of threads")

    requiredNamed_TransELS = parser_TransELS.add_argument_group('required named arguments for isoform quantification')
    requiredNamed_TransELS.add_argument('-gtf','--gtf_annotation_path', type=str, help="The path of annotation file",required=True)
    requiredNamed_TransELS.add_argument('-lrsam','--long_read_sam_path', type=str, help="The path of long read sam file",required=True)
    requiredNamed_TransELS.add_argument('-o','--output_path', type=str, help="The path of output directory",required=True)
    
    optional_TransELS = parser_TransELS.add_argument_group('optional arguments')
    optional_TransELS.add_argument('-srsam','--short_read_sam_path', type=str, help="The path of short read sam file",default=None)
    optional_TransELS.add_argument('--alpha',type=str,default='adaptive', help="Alpha[default:adaptive]: SR and LR balance parameter")
    optional_TransELS.add_argument('--beta',type=str, default='1e-6',help="Beta[default:1e-6]: L2 regularization parameter")
    optional_TransELS.add_argument('--filtering',type=bool,default=False, help="Whether the very short long reads will be filtered[default:True][True,False]")
    optional_TransELS.add_argument('-t','--threads',type=int, default=1,help="Number of threads")
    args = parser.parse_args()
    if args.subparser_name == 'cal_K_value':
        print('Calculate K values')
        TrEESR(args.gtf_annotation_path,args.output_path,args.long_read_sam_path,args.threads)
    elif args.subparser_name == 'quantify':
        print('Isoform quantification',flush=True)
        if (args.alpha == 'adaptive'):
            alpha = 'adaptive'
        else:
            try:
                alpha = float(args.alpha)
            except:
                raise Exception('Alpha given is not numeric')
        if (args.beta == 'adaptive'):
            beta = 'adaptive'
        else:
            try:
                beta = float(args.beta)
            except:
                raise Exception('Beta given is not numeric')
        if (args.short_read_sam_path is None):
            args.alpha = 1.0
        TransELS(args.gtf_annotation_path,args.short_read_sam_path,args.long_read_sam_path,args.output_path,'original',alpha,beta,1e-6,args.filtering,args.threads)
    else:
        parser.print_help()
if __name__ == "__main__":
    parse_arguments()
