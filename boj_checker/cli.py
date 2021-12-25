import argparse
import colorama
from pathlib import Path
from typing import List
from .runner import check_output, run_source_file
from .boj_parser import fetch_sample_io


def main(args: List[str]):
    """The main function of BOJ-checker

    Parameters
    ----------
    args
        command line arguments supplied to the tool


    Returns
    -------
    int
        Exit code of the program
    """
    colorama.init()
    parser = argparse.ArgumentParser(description="Check solutions against sample IO.")
    parser.add_argument(
        "probno", metavar="PROB_ID", type=int, help="The problem ID for solution"
    )
    parser.add_argument(
        "filepath", metavar="FILE", type=str, help="The solution code to test"
    )
    parsed_args = parser.parse_args(args)
    samples = fetch_sample_io(parsed_args.probno)
    filepath = Path(parsed_args.filepath)
    print(f"Testing code for {len(samples)} sample{'s' if len(samples) > 1 else ''}")
    for i, sample in enumerate(samples):
        print(f"Testing sample #{i}: ", end="")
        input_str, solution = sample
        output, exit_code = run_source_file(filepath, input_str)
        if exit_code != 0:
            print(f"{colorama.Fore.RED}RTE{colorama.Style.RESET_ALL}")
        elif check_output(solution, output):
            print(f"{colorama.Fore.GREEN}AC{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}WA{colorama.Style.RESET_ALL}")
            print("Expected output:")
            print(solution)
            print("\nActual output:")
            print(output)
