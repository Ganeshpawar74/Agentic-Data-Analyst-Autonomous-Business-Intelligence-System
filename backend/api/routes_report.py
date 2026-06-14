"""
backend/api/routes_report.py
=============================
Report generation and download endpoints.

  POST /generate-report               — generate or retrieve a cached report
  GET  /generate-report/download/{id} — stream report file for download

Frontend consumer
-----------------
  05_reports.py  →  POST /generate-report
    Payload:  { session_id: str, format: "html"|"markdown"|"pdf" }
    Expects:  ReportResponse:
                { session_id, format, content: str|None, file_path: str|None }
    Uses:
      • data["content"]   → st.markdown() preview or components.html() preview
      • st.download_button(data=data["content"])

  05_reports.py  →  GET /generate-report/download/{session_id}?format=pdf
    Streams file as application/octet-stream.
    Linked directly via <a href="..."> in the Direct Download Links card.

Report file naming convention (set by report_agent.py):
  reports/report_{session_id}_{timestamp}.{ext}
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from backend.models.schemas import ReportRequest, ReportResponse

router = APIRouter()


@router.post("", response_model=ReportResponse)
async def generate_report(request: ReportRequest) -> ReportResponse:
    """
    Return the most-recently generated report for this session.

    The report files are written to settings.reports_dir by the
    report_agent during the /analyze pipeline. This endpoint simply
    locates the matching file and returns its content (html/md) or
    file path (pdf).

    If no report exists yet, returns HTTP 404 with a clear message
    so the frontend can show the "Run an analysis first" empty state.
    """
    from config.settings import get_settings
    settings = get_settings()

    report_dir = settings.reports_dir
    # glob pattern matches all reports for this session regardless of timestamp
    pattern = f"report_{request.session_id}_*"
    files = sorted(report_dir.glob(pattern), reverse=True)

    suffix_map = {"html": ".html", "markdown": ".md", "pdf": ".pdf"}
    target_suffix = suffix_map.get(request.format)

    if target_suffix:
        matching = [f for f in files if f.suffix == target_suffix]
        if matching:
            selected = matching[0]
            if request.format == "pdf":
                return ReportResponse(
                    session_id=request.session_id,
                    format="pdf",
                    file_path=str(selected),
                )
            else:
                return ReportResponse(
                    session_id=request.session_id,
                    format=request.format,
                    content=selected.read_text(encoding="utf-8"),
                    file_path=str(selected),
                )

    raise HTTPException(
        status_code=404,
        detail=(
            f"No {request.format} report found for session {request.session_id}. "
            "Run POST /analyze first to generate a report."
        ),
    )


@router.get("/download/{session_id}")
async def download_report(session_id: str, format: str = "pdf"):
    """
    Stream a report file as a binary download.

    Used by the Direct Download Links card in 05_reports.py:
      <a href="{API_BASE}/generate-report/download/{session_id}?format=html">
    """
    from config.settings import get_settings
    settings = get_settings()

    report_dir = settings.reports_dir
    ext = {"html": ".html", "markdown": ".md", "pdf": ".pdf"}.get(format, f".{format}")
    files = sorted(report_dir.glob(f"report_{session_id}_*{ext}"), reverse=True)

    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"No {format} report found for session {session_id}.",
        )

    mime_map = {
        ".html": "text/html",
        ".md": "text/markdown",
        ".pdf": "application/pdf",
    }
    mime = mime_map.get(ext, "application/octet-stream")

    return FileResponse(
        path=str(files[0]),
        media_type=mime,
        filename=files[0].name,
    )