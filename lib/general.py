import os

def walk_replace(rootdir, operator_instance):
    """
    Walk through files in rootdir and apply the
    regex processing from operator_instance.
    """
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith(".py"):
                operator_instance.per_file_operator(filepath)
