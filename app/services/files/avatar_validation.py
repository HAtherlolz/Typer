from fastapi import UploadFile


async def is_file_valid(file: UploadFile) -> bool:
    megabyte_limit = 20
    allowed_extensions = ['png', 'jpg', 'jpeg']
    if not file.filename.split('.')[1].lower() in allowed_extensions:
        return False
    if file.size > megabyte_limit * 1024 * 1024:
        return False
    return True
