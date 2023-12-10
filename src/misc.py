def convert_path(input_path: str) -> str:
    r"""converts windows file path '\\' into '/'"""
    return input_path.replace("\\", '/')
