# PDF Image Extractor

This project extracts images from PDF files using the ConvertAPI `extract-images`
conversion. Extracted images are saved to the configured output directory.

## Requirements

- Python 3.8 or newer
- A ConvertAPI account and API credential

## Setup

From the project directory, create and activate a virtual environment, then install
the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` in the project root:

```yaml
api_credential_key: "YOUR_CONVERTAPI_CREDENTIAL"
image_output_format: jpg
image_output_dir: "workspace_output"
```

- `api_credential_key` is your ConvertAPI credential.
- `image_output_format` is the format for extracted images, such as `jpg` or `png`.
- `image_output_dir` is where ConvertAPI saves the extracted images. Relative paths
  are interpreted by ConvertAPI relative to the process working directory.

Keep your credential private. Do not commit a real credential to a public repository.

## Usage

Pass the PDF path as the positional argument. By default, the program reads
`config.yaml` from the project directory:

```powershell
python main.py "C:\path\to\document.pdf"
```

To use a different configuration file, provide `--config-file`:

```powershell
python main.py "C:\path\to\document.pdf" --config-file "C:\path\to\config.yaml"
```

The program sends the PDF to ConvertAPI and prints the paths returned for the
extracted images. The ConvertAPI service requires an internet connection and may
apply account usage limits.

## Tests

Run the test suite from the project directory:

```powershell
pytest
```
