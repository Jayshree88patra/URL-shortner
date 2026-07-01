from sqlmodel import Session, select
from app.database import get_session
from app.models import URLMap
import string, random

CODE_LENGTH = 6

def _gen_code(length: int = CODE_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=length))

def create_short(url: str, custom_code: str | None = None) -> URLMap:
    with get_session() as session:
        if custom_code:
            # simple validation
            if not all(c.isalnum() or c in '-_' for c in custom_code):
                raise ValueError("Custom code can contain only alphanumeric characters, '-' and '_'")
            statement = select(URLMap).where(URLMap.code == custom_code)
            if session.exec(statement).first():
                raise KeyError("Custom code already exists")
            code = custom_code
            is_custom = True
        else:
            # generate unique code with retries
            for _ in range(10):
                candidate = _gen_code()
                if not session.exec(select(URLMap).where(URLMap.code == candidate)).first():
                    code = candidate
                    is_custom = False
                    break
            else:
                raise RuntimeError("Failed to generate unique code")

        url_map = URLMap(code=code, url=str(url), custom=is_custom)
        session.add(url_map)
        session.commit()
        session.refresh(url_map)
        return url_map

def get_by_code(code: str) -> URLMap | None:
    with get_session() as session:
        statement = select(URLMap).where(URLMap.code == code)
        return session.exec(statement).first()

def update_url(code: str, new_url: str) -> URLMap:
    with get_session() as session:
        statement = select(URLMap).where(URLMap.code == code)
        url_map = session.exec(statement).first()
        if not url_map:
            raise KeyError("Not found")
        url_map.url = new_url
        import datetime
        url_map.updated_at = datetime.datetime.utcnow()
        session.add(url_map)
        session.commit()
        session.refresh(url_map)
        return url_map

def delete_by_code(code: str) -> bool:
    with get_session() as session:
        statement = select(URLMap).where(URLMap.code == code)
        url_map = session.exec(statement).first()
        if not url_map:
            return False
        session.delete(url_map)
        session.commit()
        return True

def increment_access(code: str) -> None:
    with get_session() as session:
        statement = select(URLMap).where(URLMap.code == code)
        url_map = session.exec(statement).first()
        if url_map:
            url_map.access_count += 1
            session.add(url_map)
            session.commit()

def get_stats(code: str) -> URLMap | None:
    return get_by_code(code)
