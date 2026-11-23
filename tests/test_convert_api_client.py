import pytest
from pdf_image_extractor import YAMLConfigurationLoader, ConfigurationError, ConvertAPI
import convertapi


def test_load_yaml_configuration_reads_api_and_image_settings(tmp_path):
    configuration_file = tmp_path / "config.yaml"
    configuration_file.write_text(
        "api_credential_key: test-api-key\n"
        "image_output_format: png\n",
        encoding="utf-8",
    )
    configuration = YAMLConfigurationLoader().load(configuration_file)
    assert configuration["api_credential_key"] == "test-api-key"
    assert configuration["image_output_format"] == "png"


def test_load_yaml_configuration_rejects_invalid_yaml(tmp_path):
    configuration_file = tmp_path / "config.yaml"
    configuration_file.write_text("api_credential_key: [unterminated\n", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        YAMLConfigurationLoader().load(configuration_file)


def test_fetch_images_from_pdf_uses_configuration(monkeypatch, tmp_path):
    pdf_file = tmp_path / "document.pdf"
    output_dir = tmp_path / "images"
    configuration_file = tmp_path / "config.yaml"
    configuration_file.write_text(
        "api_credential_key: test-api-key\n"
        "image_output_format: png\n"
        "image_output_dir: {}\n".format(output_dir),
        encoding="utf-8",
    )
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
    monkeypatch.setattr(convertapi, "convert", fake_convert)

    saved_files = ConvertAPI(configuration_file).fetch_images_from_pdf(pdf_file)
    assert saved_files == expected_files
    assert convertapi.api_credentials == "test-api-key"
    assert captured["convert_format"] == "extract-images"
    assert captured["parameters"] == {
        "File": pdf_file,
        "ImageOutputFormat": "png",
    }
    assert captured["from_format"] == "pdf"
    assert captured["output_dir"] == str(output_dir)
