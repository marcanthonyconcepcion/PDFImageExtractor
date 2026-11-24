from typing import Any, Dict


class PDFImageExtractor:
    def __init__(self, configuration: Dict[str, Any]):
        self.image_output_format = configuration["image_output_format"]
        self.image_output_dir = configuration["image_output_dir"]
        self.api_credential_key = configuration["api_credential_key"]

    def fetch(self, pdf_file_path):
        """
        Fetches images from a PDF file using the ConvertAPI service.

        :param pdf_file_path: Path to the PDF file.
        :return: List of paths to the extracted image files.
        """
        import convertapi
        convertapi.api_credentials = self.api_credential_key
        result = convertapi.convert('extract-images', {
            'File': pdf_file_path,
            'ImageOutputFormat': self.image_output_format,
        }, from_format='pdf')
        return result.save_files(self.image_output_dir)
