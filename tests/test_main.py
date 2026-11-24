import main


def test_main_passes_pdf_and_config_arguments(monkeypatch, tmp_path, capsys):
    pdf_file = tmp_path / "document.pdf"
    config_file = tmp_path / "custom-config.yaml"
    expected_files = ["workspace_output/image-1.jpg"]
    expected_configuration = {"api_credential_key": "test-api-key"}
    calls = {}

    class FakeConfigurationLoader:
        def load(self, file_path):
            calls["configuration_file"] = file_path
            return expected_configuration

    class FakePDFImageExtractor:
        def __init__(self, configuration):
            calls["configuration"] = configuration

        def fetch(self, file_path):
            calls["file_path"] = file_path
            return expected_files

    monkeypatch.setattr(main, "YAMLConfigurationLoader", FakeConfigurationLoader)
    monkeypatch.setattr(main, "PDFImageExtractor", FakePDFImageExtractor)
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(pdf_file), "--config-file", str(config_file)],
    )

    main.main()
    assert calls["file_path"] == pdf_file
    assert calls["configuration_file"] == config_file
    assert calls["configuration"] is expected_configuration
    assert capsys.readouterr().out == "workspace_output/image-1.jpg\n"


def test_main_defaults_to_project_config_file(monkeypatch, tmp_path, capsys):
    pdf_file = tmp_path / "document.pdf"
    calls = {}

    class FakeConfigurationLoader:
        def load(self, file_path):
            calls["configuration_file"] = file_path
            return {}

    class FakePDFImageExtractor:
        def __init__(self, configuration):
            calls["configuration"] = configuration

        def fetch(self, file_path):
            return []

    monkeypatch.setattr(main, "YAMLConfigurationLoader", FakeConfigurationLoader)
    monkeypatch.setattr(main, "PDFImageExtractor", FakePDFImageExtractor)
    monkeypatch.setattr("sys.argv", ["main.py", str(pdf_file)])

    main.main()
    assert calls["configuration_file"] == (
        main.Path(main.__file__).resolve().parent / "config.yaml"
    )
    assert calls["configuration"] == {}
    assert capsys.readouterr().out == ""
