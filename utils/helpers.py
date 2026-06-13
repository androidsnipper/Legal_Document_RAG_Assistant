def safe_read(file):
    if file is None:
        raise ValueError("No file uploaded")

    return file