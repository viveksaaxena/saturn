from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import supabase
from typing import Optional

router = APIRouter(prefix="/api/notes", tags=["Notes"])

class NoteCreate(BaseModel):
    user_id: str  # string for Supabase ID
    title: str
    content: Optional[str] = ""

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

@router.get("/")
def get_notes(user_id: str):
    try:
        result = supabase.table("notes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return {"notes": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def create_note(note: NoteCreate):
    try:
        result = supabase.table("notes").insert({
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content
        }).execute()
        return {"notes": [result.data[0]]}  # return as list to match frontend
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-date")
def get_notes_by_date(user_id: str, date: str):
    try:
        result = supabase.table("notes").select("*").eq("user_id", user_id).like("created_at", f"{date}%").order("created_at", desc=True).execute()
        return {"notes": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    try:
        update_data = {}
        if note.title is not None:
            update_data["title"] = note.title
        if note.content is not None:
            update_data["content"] = note.content

        result = supabase.table("notes").update(update_data).eq("id", note_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Note not found")
        return {"notes": [result.data[0]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}")
def delete_note(note_id: int):
    try:
        result = supabase.table("notes").delete().eq("id", note_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Note not found")
        return {"message": "Note deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
