from fastapi import APIRouter, HTTPException, status
from app.schemas import CreateRequest, UpdateRequest, URLResponse, StatsResponse
from app import crud

router = APIRouter(prefix="/shorten", tags=["shorten"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=URLResponse)
def create_short(req: CreateRequest):
    try:
        url_map = crud.create_short(req.url, req.custom_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "id": url_map.id,
        "url": url_map.url,
        "shortCode": url_map.code,
        "createdAt": url_map.created_at,
        "updatedAt": url_map.updated_at,
    }

@router.get("/{code}", response_model=URLResponse)
def get_original(code: str):
    url_map = crud.get_by_code(code)
    if not url_map:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": url_map.id,
        "url": url_map.url,
        "shortCode": url_map.code,
        "createdAt": url_map.created_at,
        "updatedAt": url_map.updated_at,
    }

@router.put("/{code}", response_model=URLResponse)
def update_short(code: str, req: UpdateRequest):
    try:
        url_map = crud.update_url(code, req.url)
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": url_map.id,
        "url": url_map.url,
        "shortCode": url_map.code,
        "createdAt": url_map.created_at,
        "updatedAt": url_map.updated_at,
    }

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short(code: str):
    ok = crud.delete_by_code(code)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return None

@router.get("/{code}/stats", response_model=StatsResponse)
def stats(code: str):
    url_map = crud.get_stats(code)
    if not url_map:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": url_map.id,
        "url": url_map.url,
        "shortCode": url_map.code,
        "createdAt": url_map.created_at,
        "updatedAt": url_map.updated_at,
        "accessCount": url_map.access_count,
    }
