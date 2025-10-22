def file_exists(file_path):
    """Check if a file exists at the given path."""
    import os
    return os.path.isfile(file_path)

def read_file_contents(file_path):
    """Read the contents of a file and return them as a string."""
    with open(file_path, 'r') as file:
        return file.read()

def write_to_file(file_path, content):
    """Write the given content to a file at the specified path."""
    with open(file_path, 'w') as file:
        file.write(content)

def delete_file(file_path):
    """Delete the file at the given path if it exists."""
    import os
    if file_exists(file_path):
        os.remove(file_path)
