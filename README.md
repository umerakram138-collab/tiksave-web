# TikSave — TikTok Video Downloader

A ready-to-deploy Flask website that accepts public TikTok video links and downloads the available video file using yt-dlp.

## Important

- Only download content you own or have permission to use.
- This project is not affiliated with TikTok.
- No-watermark output is not guaranteed.
- TikTok can change its systems, so yt-dlp may occasionally require an update.

## Run locally

1. Install Python 3.11+
2. Open this project folder in Terminal
3. Run:

```bash
pip install -r requirements.txt
python app.py
```

4. Open `http://localhost:5000`

## Publish free on Render

1. Create a free GitHub account and upload this project.
2. Create a Render account.
3. Click **New +** → **Web Service**.
4. Connect the GitHub repository.
5. Render should detect `render.yaml`; otherwise use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --timeout 120`
6. Deploy.

Render gives a free URL such as:
`https://tiksave-web.onrender.com`

## Custom domain

A custom `.com` or `.pk` domain is optional and normally paid. You can use the free Render URL first.
