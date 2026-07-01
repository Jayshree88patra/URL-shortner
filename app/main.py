from fastapi import FastAPI
from app.routes.shorten import router as shorten_router
from app.database import init_db, get_session
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlmodel import Session, select
from app.models import URLMap

app = FastAPI(title="URL Shortener")

app.include_router(shorten_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/{code}")
def redirect(code: str):
    """Redirect to the target URL and increment access count."""
    with get_session() as session:
        statement = select(URLMap).where(URLMap.code == code)
        url_map = session.exec(statement).first()
        if not url_map:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Short URL not found")
        url_map.access_count += 1
        session.add(url_map)
        session.commit()
        return RedirectResponse(url_map.url)
