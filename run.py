import sys
import argparse

def get_fitness_functions_dict():
    return {
        'velocity_height': {
            'toolbox': "vh",
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

    return parser


if __name__ == "__main__":

    args = get_argument_parser().parse_args()

    parser.add_argument("-f", "--file", dest="filename",
                        help="write report to FILE", metavar="FILE")

    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

    args = parser.parse_args()

    if(len(sys.argv) != 6):
        print("Wrong number of arguments!")
        print("Usage:", sys.argv[0],
              "EXPERIMENT_NAME NUM_OF_ISLANDS MIGRATIONS_RATIO max_iterations_wo_improvement MODEL")
        sys.exit()


    print(sys.argv)