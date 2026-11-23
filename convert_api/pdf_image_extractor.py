from pathlib import Path
from .configuration import YAMLConfigurationLoader


class PDFImageExtractor:
    def __init__(self, configuration_file=None):
        if configuration_file is None:
            configuration_file = Path(__file__).resolve().parent.parent / "config.yaml"
        self.configuration = YAMLConfigurationLoader().load(configuration_file)

    def fetch(self, pdf_file_path):
        """
        Fetches images from a PDF file using the ConvertAPI service.

        :param pdf_file_path: Path to the PDF file.
        :return: List of paths to the extracted image files.
        """
        image_output_format = self.configuration["image_output_format"]
        output_dir = self.configuration["image_output_dir"]
        import convertapi
        convertapi.api_credentials = self.configuration["api_credential_key"]
        result = convertapi.convert('extract-images', {
            'File': pdf_file_path,
            'ImageOutputFormat': image_output_format,
        }, from_format='pdf')
        return result.save_files(output_dir)
