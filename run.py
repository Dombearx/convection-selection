import sys
import argparse

def get_fitness_functions_dict():
    return {
        'velocity_height': {
            'toolbox': "vh",
        },
    }

def get_migration_model_dict():
    return {
        'convection_const': {
            'migration': "convection_const",
        },
        'convection_front': {
            'migration': "convection_front",
        },
    }


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-ff", "--fit_function",
        required=True,
        help="type of fitness function",
        choices=get_fitness_functions_dict().keys(),
    )

    parser.add_argument(
        "-i", "--islands",
        required=True,
        help="number of islands",
        default=10,
        type=int,
    )

    parser.add_argument(
        "-r", "--ratio",
        required=True,
        help="migration ratio",
        default=0.1,
        type=float,
    )

    parser.add_argument(
        "-max", "--max_iter",
        required=True,
        help="max iterations without improvement",
        default=1000,
        type=int,
    )

    parser.add_argument(
        "-m", "--model",
        required=True,
        help="migration model",
        choices=get_migration_model_dict().keys(),
    )

    return parser


if __name__ == "__main__":

    args = get_argument_parser().parse_args()

    print(args)