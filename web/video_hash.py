import hashlib

def hash_video_file(file_obj):
    """
    Generate SHA256 hash for a video file-like object.
    This will change if even 1 byte of the file changes.
    """
    sha256_hash = hashlib.sha256()
    for chunk in iter(lambda: file_obj.read(4096), b""):
        sha256_hash.update(chunk)
    file_obj.seek(0) 
    return sha256_hash.hexdigest()