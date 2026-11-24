from convert_api import PDFImageExtractor
import convertapi


def test_fetch_uses_configuration(monkeypatch, tmp_path):
    pdf_file = tmp_path / "document.pdf"
    output_dir = tmp_path / "images"
    configuration = {
        "api_credential_key": "test-api-key",
        "image_output_format": "png",
        "image_output_dir": str(output_dir),
    }
    expected_files = [str(output_dir / "page-1.png"), str(output_dir / "page-2.png")]
    captured = {}

    class FakeResult:
        def save_files(self, directory):
            captured["output_dir"] = directory
            return expected_files

    def fake_convert(convert_format, parameters, from_format):
        captured["convert_format"] = convert_format
        captured["parameters"] = parameters
        captured["from_format"] = from_format
        return FakeResult()

    monkeypatch.setattr(convertapi, "api_credentials", "previous-api-key", raising=False)
    monkeypatch.setattr(convertapi, "convert", fake_convert)

    saved_files = PDFImageExtractor(configuration).fetch(pdf_file)
    assert saved_files == expected_files
    assert convertapi.api_credentials == "test-api-key"
    assert captured["convert_format"] == "extract-images"
    assert captured["parameters"] == {
        "File": pdf_file,
        "ImageOutputFormat": "png",
    }
    assert captured["from_format"] == "pdf"
    assert captured["output_dir"] == str(output_dir)
