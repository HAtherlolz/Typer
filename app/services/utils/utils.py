from fastapi import HTTPException


async def pagination(page: int, page_size) -> int:
    if page < 1:
        raise HTTPException(status_code=400, detail="The wrong page number")
    offset = (page - 1) * page_size
    return offset
