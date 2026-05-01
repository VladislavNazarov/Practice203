def convert_project_to_text(project_path: str) -> str:
    import os
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project not found: {project_path}")
    output_dir = project_path + "_text"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "export.xml"), "w", encoding="utf-8") as f:
        f.write("<project/>")
    return output_dir
