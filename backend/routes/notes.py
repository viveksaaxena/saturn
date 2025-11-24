from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.database import get_supabase   # ✅ correct import for Render

router = APIRouter(prefix="/api/notes", tags=["Notes"])

# Create Supabase client safely
supabase = get_supabase()


class NoteCreate(BaseModel):
    user_id: str
    title: str
    content: Optional[str] = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@router.get("/")
def get_notes(user_id: str):
    if supabase is None:
        raise HTTPException(500, "Supabase not configured")

    try:
        result = (
            supabase
            .table("notes")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return {"notes": result.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_note(note: NoteCreate):
    if supabase is None:
        raise HTTPException(500, "Supabase not configured")

    try:
        result = (
            supabase
            .table("notes")
            .insert({
                "user_id": note.user_id,
                "title": note.title,
                "content": note.content
            })
            .execute()
        )

        return {"notes": [result.data[0]]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-date")
def get_notes_by_date(user_id: str, date: str):
    if supabase is None:
        raise HTTPException(500, "Supabase not configured")

    try:
        result = (
            supabase
            .table("notes")
            .select("*")
            .eq("user_id", user_id)
            .like("created_at", f"{date}%")
            .order("created_at", desc=True)
            .execute()
        )
        return {"notes": result.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    if supabase is None:
        raise HTTPException(500, "Supabase not configured")

    try:
        update_data = {}

        if note.title is not None:
            update_data["title"] = note.title

        if note.content is not None:
            update_data["content"] = note.content

        result = (
            supabase
            .table("notes")
            .update(update_data)
            .eq("id", note_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(404, "Note not found")

        return {"notes": [result.data[0]]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{note_id}")
def delete_note(note_id: int):
    if supabase is None:
        raise HTTPException(500, "Supabase not configured")

    try:
        result = (
            supabase
            .table("notes")
            .delete()
            .eq("id", note_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(404, "Note not found")

        return {"message": "Note deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

