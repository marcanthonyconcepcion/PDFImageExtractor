import pytest
from configuration import ConfigurationError, YAMLConfigurationLoader


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
