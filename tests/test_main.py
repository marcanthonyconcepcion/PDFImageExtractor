import main


def test_main_calls_convert_api_with_pdf_and_config_arguments(monkeypatch, tmp_path, capsys):
    pdf_file = tmp_path / "document.pdf"
    config_file = tmp_path / "custom-config.yaml"
    expected_files = ["workspace_output/image-1.jpg"]
    calls = {}

    class FakeConvertAPI:
        def __init__(self, configuration_file):
            calls["configuration_file"] = configuration_file

        def fetch_images_from_pdf(self, file_path):
            calls["file_path"] = file_path
            return expected_files

    monkeypatch.setattr(main, "ConvertAPI", FakeConvertAPI)
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(pdf_file), "--config-file", str(config_file)],
    )

    main.main()

    assert calls["file_path"] == pdf_file
    assert calls["configuration_file"] == config_file
    assert capsys.readouterr().out == "workspace_output/image-1.jpg\n"


def test_main_defaults_to_project_config_file(monkeypatch, tmp_path, capsys):
    pdf_file = tmp_path / "document.pdf"
    calls = {}

    class FakeConvertAPI:
        def __init__(self, configuration_file):
            calls["configuration_file"] = configuration_file

        def fetch_images_from_pdf(self, file_path):
            return []

    monkeypatch.setattr(main, "ConvertAPI", FakeConvertAPI)
    monkeypatch.setattr("sys.argv", ["main.py", str(pdf_file)])

    main.main()

    assert calls["configuration_file"] == (
        main.Path(main.__file__).resolve().parent / "config.yaml"
    )
    assert capsys.readouterr().out == ""
