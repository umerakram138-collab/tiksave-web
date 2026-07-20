import os
import re
import shutil
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
from yt_dlp import YoutubeDL

app = Flask(__name__)

TIKTOK_URL_RE = re.compile(
    r"^https?://(?:(?:www|m|vm|vt)\.)?tiktok\.com/",
    re.IGNORECASE
)

def safe_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', "_", name or "tiktok-video")
    name = re.sub(r"\s+", " ", name).strip()
    return name[:100] or "tiktok-video"

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/download")
def download():
    url = (request.form.get("url") or "").strip()

    if not url:
        return render_template("index.html", error="Please paste a TikTok video link."), 400

    if not TIKTOK_URL_RE.match(url):
        return render_template("index.html", error="Please enter a valid TikTok link."), 400

    temp_dir = tempfile.mkdtemp(prefix="tiksave_")
    output_template = str(Path(temp_dir) / "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
        "socket_timeout": 25,
        "retries": 2,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        },
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = Path(ydl.prepare_filename(info))

        if not downloaded_path.exists():
            candidates = list(Path(temp_dir).glob("*"))
            if not candidates:
                raise RuntimeError("Downloaded file was not created.")
            downloaded_path = max(candidates, key=lambda p: p.stat().st_size)

        title = safe_filename(info.get("title") or "tiktok-video")
        extension = downloaded_path.suffix or ".mp4"
        download_name = f"{title}{extension}"

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
            return response

        return send_file(
            downloaded_path,
            as_attachment=True,
            download_name=download_name,
            mimetype="video/mp4"
        )

    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return render_template(
            "index.html",
            error=(
                "This video could not be downloaded. It may be private, restricted, "
                "deleted, or TikTok may have temporarily changed its system."
            )
        ), 422

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
