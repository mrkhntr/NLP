import io


def file_to_str(filepath):
    with io.open(filepath, 'r', encoding='iso-8859-15') as f:
        text = f.read()
    return text


def write_to_filepath(text, filepath):
    with io.open(filepath, 'w', encoding='iso-8859-15') as f:
        f.write(text)
