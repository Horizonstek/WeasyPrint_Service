"""PDF rendering FastAPI service using Jinja2 templates and WeasyPrint."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape
from pydantic import BaseModel
from weasyprint import HTML
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings:
    """Runtime configuration pulled from environment variables."""

    api_key: str

    def __init__(self) -> None:
        self.api_key = os.getenv("PDF_SERVICE_API_KEY", "dev-secret")


settings = Settings()


def build_template_environment() -> Environment:
    """Return a Jinja2 environment configured for HTML templates."""

    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=False,
    )


template_env = build_template_environment()


class RenderRequest(BaseModel):
    template_name: str
    data: Dict[str, Any]


app = FastAPI(
    title="Universal PDF Rendering Service",
    description="Render HTML templates to PDF using WeasyPrint.",
    version="0.1.0",
)


def _verify_api_key(provided_key: str) -> None:
    """Ensure the caller supplied the expected API key."""

    if provided_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")


@app.post("/WeasyPrint/report", response_class=Response, summary="Render PDF from template")
async def render_pdf(
    payload: RenderRequest,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> Response:
    """Render the requested template with supplied data and return a PDF."""

    _verify_api_key(x_api_key)

    try:
        template = template_env.get_template(payload.template_name)
    except TemplateNotFound as exc:
        raise HTTPException(status_code=404, detail=f"Template '{payload.template_name}' not found.") from exc

    html_content = template.render(**payload.data)

    pdf_bytes = HTML(string=html_content, base_url=str(STATIC_DIR)).write_pdf()

    filename = f"{Path(payload.template_name).stem}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@app.get("/WeasyPrint/health", summary="Health check")
async def health_check() -> Dict[str, str]:
    """Simple endpoint for uptime monitoring."""

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
