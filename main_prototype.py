import argparse
from src.modules import ModelUtils

def main(model_name):
    model_utils = ModelUtils(model_name)
    model_utils.check_model_installed()
    ModelUtils.save_chosen_model(model_name)
    chosen_model = ModelUtils.load_chosen_model()
    print(chosen_model)

def cli():
    parser = argparse.ArgumentParser(description="Model Utility CLI")
    subparsers = parser.add_subparsers(dest='command')

    run_parser = subparsers.add_parser('run', help='Run a model')
    run_parser.add_argument('model_name', type=str, nargs='?', default='llama3.2', help='Name of the model to use')

    args = parser.parse_args()

    if args.command == 'run':
        main(args.model_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()