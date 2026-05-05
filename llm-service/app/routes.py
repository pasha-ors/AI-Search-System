from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest
from app.service import analyze_text

router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/analyze")
def analyze(req: QueryRequest):
    result = analyze_text(req.text)

    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail=result
        )

    return {
        "success": True,
        "data": result
    }