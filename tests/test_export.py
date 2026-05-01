import os
import tempfile
from export import convert_project_to_text


def test_export_creates_text_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = os.path.join(tmpdir, "test.project")
        with open(project_path, "w") as f:
            f.write("<project></project>")
        output_dir = convert_project_to_text(project_path)
        assert os.path.isdir(output_dir)
        assert len(os.listdir(output_dir)) > 0


def test_export_invalid_project_raises_error():
    with tempfile.TemporaryDirectory() as tmpdir:
        bad_project = os.path.join(tmpdir, "nonexistent.project")
        try:
            convert_project_to_text(bad_project)
        except FileNotFoundError:
            return
        assert False, "Should have raised FileNotFoundError"
