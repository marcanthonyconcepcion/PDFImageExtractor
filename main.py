import argparse
from pathlib import Path
from convert_api import PDFImageExtractor


def main():
    parser = argparse.ArgumentParser(description="Extract images from a PDF using ConvertAPI.")
    parser.add_argument("pdf_file", type=Path, help="PDF file to extract images from")
    default_config_file = Path(__file__).resolve().parent / "config.yaml"
    parser.add_argument(
        "--config-file",
        type=Path,
        default=default_config_file,
        help="Path to the configuration YAML file",
    )
    args = parser.parse_args()
    extracted_files = PDFImageExtractor(args.config_file).fetch(args.pdf_file)
    for file_path in extracted_files:
        print(file_path)


if __name__ == "__main__":
    main()
