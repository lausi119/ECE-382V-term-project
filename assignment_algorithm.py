# Advanced Algorithms - Term Project
# Implementing an algorithm for the Incremental Assignment Problem

from incremental_algorithm import IncrementalAssignmentAlgorithm
from util import generate_random_test, load_tests_from_file, write_to_csv, validate_result
import argparse


if __name__ == '__main__':
    generate_random_test()

    parser = argparse.ArgumentParser(description='Run the Incremental Assignment Algorithm.')

    parser.add_argument('--test', type=str, help='Test Type - either `file` or `random`')
    parser.add_argument('--settings', type=str)
    args = parser.parse_args()

    if args.test == 'file':
        examples = [load_tests_from_file()[0]]

    elif args.test == 'random':
        if args.settings is not None:
            settings = args.settings.split(',')
            examples = generate_random_test(
                min_size=int(settings[0]), max_size=int(settings[1]),
                val_range=int(settings[2]), num_tests=int(settings[3])
            )
        else:
            examples = generate_random_test()

    else:
        raise Exception(f"test `{args.test}` is not valid")

    history = []

    for idx in range(0, len(examples)):

        print("")
        print("")
        print("")
        print("")
        print("################################################################")
        print("################################################################")
        print(f"EXAMPLE {idx}")
        print("################################################################")
        print("")

        example = examples[idx]
        output_assignments, size, steps, cache_hits = IncrementalAssignmentAlgorithm(
            example['values'],
            # Couldn't load tuples from the JSON file but I am too lazy to use arrays instead,
            # so im just casting all the solution arrays from the json to tuples here
            [(a[0], a[1]) for a in example['solution']]
        ).run()

        valid, incremental_total, munkres_total = validate_result(example['values'], output_assignments)

        history.append((str(size), str(steps), str(cache_hits), str(valid), str(incremental_total), str(munkres_total)))

    write_to_csv(history)


