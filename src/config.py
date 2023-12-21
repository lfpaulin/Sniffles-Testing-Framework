import argparse


# Version
version = 'v0.2.231220'


# Arguments
def get_arguments():
    main_help = """
    Sniffles2 testing Framework <command> [<args>]
        # Complete: perform all benchmarks
            bench
                -j/--json   JSON input with all parameters

        # Single sample benchmark with GIAB HG002 v0.6 (GRCh37):
            giab
                -j/--json   JSON input with all parameters

        # Single sample benchmark with GIAB HG002 CMRG (GRCh38):
            cmrg
                -j/--json   JSON input with all parameters

        # Trio/Mendelian (BCFtools required)
            mendelian
                -j/--json       JSON input with all parameters

        # Merge
            merge
                -j/--json       JSON input with all parameters

        # Population merge with a large number of samples as input
            population
                -j/--json       JSON input with all parameters

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework",
             usage=main_help
    )
    subparsers = parser.add_subparsers(help=main_help, dest="command")

    # ############################################################################################ #
    # Bench all
    """
        -j/--json   JSON input with all parameters
    """
    bench_help = "Perform all benchmark tests"
    subparser_bench = subparsers.add_parser("bench", help=bench_help)
    subparser_bench.add_argument('-j', '--json', type=str, required=True, dest='json', default="", help='')

    # ############################################################################################ #
    # Single sample benchmark with GIAB HG002 v0.6 (GRCh37)
    """
        -j/--json   JSON input with all parameters
    """
    giab_help = "Single sample benchmark with GIAB HG002 v0.6 (GRCh37)"
    subparser_giab = subparsers.add_parser("giab", help=giab_help)
    subparser_giab.add_argument('-j', '--json', type=str, required=True, dest='json', default="", help='')

    # ############################################################################################ #
    # Single sample benchmark with GIAB HG002 CMRG (GRCh38)
    """
        -j/--json   JSON input with all parameters
    """
    cmrg_help = "Single sample benchmark with GIAB HG002 CMRG (GRCh38)"
    subparser_cmrg = subparsers.add_parser("cmrg", help=cmrg_help)
    subparser_cmrg.add_argument('-j', '--json', type=str, required=True, dest='json', default="", help='')

    # ############################################################################################ #
    # Trio/Mendelian (BCFtools required)
    """
        -j/--json       JSON input with all parameters
    """
    mendelian_help = "Trio/Mendelian bench"
    subparser_mendelian = subparsers.add_parser("mendelian", help=mendelian_help)
    subparser_mendelian.add_argument('-j', '--json', type=str, required=True, dest='json', default="", help='')

    # ############################################################################################ #
    # Population merge with a large number of samples as input
    """
         -j/--json       JSON input with all parameters
     """
    population_help = " Population mergeg with a large number of samples as input"
    subparser_popmerge = subparsers.add_parser("pop_merge", help=population_help)
    subparser_popmerge.add_argument('-j', '--json', type=str, required=True, dest='json', default="", help='')

    # ############################################################################################ #

    args = parser.parse_args()
    return args, main_help