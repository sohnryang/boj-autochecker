from pathlib import Path
from typing import List
from xdg import xdg_config_home

from . import __version__
from .config import CheckerConfig
from .runner import check_output, clean_temporary_files, run_source_file
from .boj_parser import fetch_sample_io

import argparse
import colorama


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
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "probno", metavar="PROB_ID", type=int, help="The problem ID for solution"
    )
    parser.add_argument(
        "filepath", metavar="FILE", type=str, help="The solution code to test"
    )
    parsed_args = parser.parse_args(args)
    samples = fetch_sample_io(parsed_args.probno)
    filepath = Path(parsed_args.filepath)
    config_file_path = xdg_config_home() / "boj-checker/config.json"
    try:
        config = CheckerConfig.fromfilepath(config_file_path)
    except FileNotFoundError:
        config = CheckerConfig('{"language_configs": []}')
    print(f"Testing code for {len(samples)} sample{'s' if len(samples) > 1 else ''}")
    for i, sample in enumerate(samples):
        print(f"Testing sample #{i}: ", end="")
        input_str, solution = sample
        try:
            output, exit_code = run_source_file(
                filepath, input_str, config.languageconfig_table
            )
        except NotImplementedError:
            print(f"{colorama.Fore.BLUE}Unknown language{colorama.Style.RESET_ALL}")
            break
        except ValueError:
            print(f"{colorama.Fore.BLUE}Compilation Error{colorama.Style.RESET_ALL}")
            break
        finally:
            clean_temporary_files(filepath)

        if exit_code != 0:
            print(f"{colorama.Fore.RED}RTE{colorama.Style.RESET_ALL}")
        elif check_output(solution, output):
            print(f"{colorama.Fore.GREEN}AC{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}WA{colorama.Style.RESET_ALL}")
            print(f"Expected output >>>{colorama.Fore.GREEN}")
            print(solution)
            print(f"{colorama.Style.RESET_ALL}\nActual output >>>{colorama.Fore.RED}")
            print(output)
            print(colorama.Style.RESET_ALL)
