import json
import mimetypes
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

from .config import DASHBOARDS_TABLE, HISTORY_TABLE, SUPABASE_BUCKET
from .supabase_client import get_supabase


def _slug(name):
    cleaned = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
    return cleaned[:60] or "dashboard"


def _records_from_dataframe(dataframe):
    """Convert pandas/numpy values into JSON-safe Python records."""
    return json.loads(dataframe.to_json(orient="records", date_format="iso"))


def list_dashboards():
    response = (
        get_supabase()
        .table(DASHBOARDS_TABLE)
        .select("name,slug,source_filename,updated_by,updated_at")
        .order("name")
        .execute()
    )
    return {item["name"]: item for item in (response.data or [])}


def load_dashboard(name):
    if not name:
        return pd.DataFrame()
    response = (
        get_supabase()
        .table(DASHBOARDS_TABLE)
        .select("data")
        .eq("name", name)
        .limit(1)
        .execute()
    )
    if not response.data:
        return pd.DataFrame()
    return pd.DataFrame(response.data[0].get("data") or [])


def _upload_gallery_asset(slug, asset):
    filename = Path(asset["filename"]).name
    object_path = f"gallery/{slug}/{filename}"
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    get_supabase().storage.from_(SUPABASE_BUCKET).upload(
        path=object_path,
        file=asset["data"],
        file_options={"content-type": content_type, "upsert": "true"},
    )
    return filename, f"supabase://{object_path}"


def save_dashboard(name, df, assets, username, source_filename):
    dashboards = list_dashboards()
    action = "Updated" if name in dashboards else "Created"
    slug = dashboards.get(name, {}).get("slug", _slug(name))
    stored = df.copy()

    for asset in assets or []:
        filename, storage_reference = _upload_gallery_asset(slug, asset)
        stored["Gallery Image"] = stored["Gallery Image"].fillna("").str.replace(
            filename, storage_reference, regex=False
        )

    payload = {
        "name": name,
        "slug": slug,
        "source_filename": source_filename,
        "updated_by": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "data": _records_from_dataframe(stored),
    }
    get_supabase().table(DASHBOARDS_TABLE).upsert(payload, on_conflict="name").execute()
    add_history(username, action, name, source_filename)
    st.cache_data.clear()
    return action


def _delete_gallery_folder(slug):
    storage = get_supabase().storage.from_(SUPABASE_BUCKET)
    folder = f"gallery/{slug}"
    objects = storage.list(folder)
    paths = [f"{folder}/{item['name']}" for item in objects if item.get("name")]
    if paths:
        storage.remove(paths)


def delete_dashboard(name, username):
    dashboards = list_dashboards()
    item = dashboards.get(name)
    if not item:
        return False
    _delete_gallery_folder(item["slug"])
    get_supabase().table(DASHBOARDS_TABLE).delete().eq("name", name).execute()
    add_history(username, "Deleted dashboard", name, item.get("source_filename", ""))
    st.cache_data.clear()
    return True


def add_history(username, action, dashboard, filename=""):
    get_supabase().table(HISTORY_TABLE).insert({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": username,
        "action": action,
        "dashboard": dashboard,
        "filename": filename,
    }).execute()


def load_history():
    response = (
        get_supabase()
        .table(HISTORY_TABLE)
        .select("id,timestamp,user,action,dashboard,filename")
        .order("timestamp", desc=True)
        .limit(1000)
        .execute()
    )
    return response.data or []


def delete_history(ids):
    if ids:
        get_supabase().table(HISTORY_TABLE).delete().in_("id", list(ids)).execute()


@st.cache_data(ttl=3300, show_spinner=False)
def get_gallery_image_url(storage_reference):
    if not str(storage_reference).startswith("supabase://"):
        return storage_reference
    object_path = str(storage_reference).removeprefix("supabase://")
    result = (
        get_supabase()
        .storage.from_(SUPABASE_BUCKET)
        .create_signed_url(object_path, 3600)
    )
    return result.get("signedURL") or result.get("signedUrl") or storage_reference
