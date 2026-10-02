import io
import json
import re
import pandas as pd
from .config import DATASET_INFO_FILE, DEFAULT_DATA_FILE, GALLERY_DIR, REQUIRED_COLUMNS

PHOTO_COLUMN_NAMES = {
    "photo", "photos", "image", "images", "gallery", "gallery album",
    "gallery photo", "photo url", "image url", "attachment", "attachments",
}


def _read_bytes(data, filename):
    suffix = filename.lower().rsplit(".", 1)[-1]
    if suffix == "csv":
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
            try:
                return pd.read_csv(io.BytesIO(data), encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("The CSV encoding is not supported.")
    if suffix in ("xlsx", "xls"):
        return pd.read_excel(io.BytesIO(data))
    raise ValueError("Upload a CSV or Excel (.xlsx/.xls) file.")


def validate_columns(df):
    columns = {str(column).strip() for column in df.columns}
    if "Senior Citizens" in columns:
        columns.add("No. of Senior Citizen")
    missing = sorted(REQUIRED_COLUMNS - columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))


def capacity_number(value):
    if pd.isna(value):
        return 0
    numbers = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", str(value))]
    return max(numbers) if numbers else 0


def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    # Support the trailing-space header produced by SOCOCA exports.
    aliases = {"No. of Senior Citizen": "Senior Citizens"}
    df = df.rename(columns=aliases)
    for col in ["Actual No. of Evacuees", "No. of Male", "No. of Female", "Senior Citizens", "No. of PWD"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0).astype(int)
    df["Capacity Numeric"] = df["Capacity"].map(capacity_number)
    df["Available Capacity"] = (df["Capacity Numeric"] - df["Actual No. of Evacuees"]).clip(lower=0)
    denominator = df["Capacity Numeric"].where(df["Capacity Numeric"] > 0)
    df["Occupancy Rate"] = (100 * df["Actual No. of Evacuees"] / denominator).fillna(0)
    df["Status"] = pd.cut(df["Occupancy Rate"], [-1, 0, 80, 99.999999, float("inf")], labels=["Inactive", "Operational", "Near Capacity", "Over Capacity"])
    df["Name"] = df["Name"].fillna(df.get("Spot name", "Unnamed Center")).fillna("Unnamed Center").astype(str).str.strip()
    df["Address"] = df["Address"].fillna("No address provided").astype(str)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    photo_columns = []
    for column in df.columns:
        normalized = column.lower().strip()
        if normalized not in PHOTO_COLUMN_NAMES:
            continue
        # In SOCOCA, the `Photos` column contains reference IDs (for example
        # 1-2-1), not file paths. The actual files are on the Photos worksheet.
        if normalized == "photos":
            values = df[column].fillna("").astype(str)
            looks_like_image = values.str.contains(r"https?://|data:image/|\.(?:png|jpe?g|gif|webp)(?:$|[|;])", case=False, regex=True).any()
            if not looks_like_image:
                continue
        photo_columns.append(column)
    if photo_columns:
        df["Gallery Image"] = df[photo_columns].apply(
            lambda row: " | ".join(str(value).strip() for value in row if pd.notna(value) and str(value).strip()), axis=1
        )
    elif "Gallery Image" not in df.columns:
        df["Gallery Image"] = ""
    return df


def extract_embedded_excel_images(data):
    """Extract pictures and their No/SpotName/Title/Date metadata from SOCOCA XLSX."""
    try:
        from openpyxl import load_workbook
        workbook = load_workbook(io.BytesIO(data), data_only=True)
        sheet = workbook["Photos"] if "Photos" in workbook.sheetnames else workbook.active
        extracted = []
        for number, picture in enumerate(getattr(sheet, "_images", []), start=1):
            marker = getattr(getattr(picture, "anchor", None), "_from", None)
            anchor_row = getattr(marker, "row", 7)
            anchor_col = getattr(marker, "col", 0)
            value_col = anchor_col + 2  # openpyxl cell columns are one-based
            def metadata_value(offset):
                return sheet.cell(anchor_row + offset + 1, value_col).value
            extension = getattr(picture, "format", "png").lower()
            extension = extension if extension in {"png", "jpeg", "jpg", "gif", "webp"} else "png"
            extracted.append({
                "photo_no": metadata_value(-5),
                "spot_name": metadata_value(-4),
                "photo_name": metadata_value(-3),
                "title": metadata_value(-2),
                "date": metadata_value(-1),
                "filename": f"embedded_{number}.{extension}",
                "data": picture._data(),
            })
        return extracted
    except Exception:
        return []


def load_default_data():
    raw = DEFAULT_DATA_FILE.read_bytes()
    df = _read_bytes(raw, DEFAULT_DATA_FILE.name)
    validate_columns(df)
    return clean_data(df)


def empty_dashboard_data():
    """Return a clean, schema-ready dashboard with no starter records."""
    columns = [
        "Name", "Address", "latitude", "longitude", "Capacity",
        "Actual No. of Evacuees", "No. of Male", "No. of Female",
        "Senior Citizens", "No. of PWD", "Type of Evacuation Center",
        "Capacity Numeric", "Available Capacity", "Occupancy Rate", "Status",
        "Gallery Image", "Gallery Metadata",
    ]
    return pd.DataFrame(columns=columns)


def load_dataset_name():
    if DATASET_INFO_FILE.exists():
        try:
            return json.loads(DATASET_INFO_FILE.read_text(encoding="utf-8")).get("filename", DEFAULT_DATA_FILE.name)
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_DATA_FILE.name


def parse_upload(uploaded_file):
    data = uploaded_file.getvalue()
    raw_df = _read_bytes(data, uploaded_file.name)
    # Normalize only for validation, so exports with whitespace still work.
    raw_df.columns = raw_df.columns.str.strip()
    validate_columns(raw_df)
    cleaned = clean_data(raw_df)
    assets = extract_embedded_excel_images(data) if uploaded_file.name.lower().endswith(".xlsx") else []
    if "Gallery Metadata" not in cleaned.columns:
        cleaned["Gallery Metadata"] = ""
    for asset in assets:
        matches = pd.Series(False, index=cleaned.index)
        if "Photos" in cleaned.columns and asset.get("photo_no"):
            matches = cleaned["Photos"].fillna("").astype(str).str.split(r"\s*[,|;]\s*", regex=True).apply(lambda values: str(asset["photo_no"]) in values)
        if not matches.any() and asset.get("spot_name"):
            matches = cleaned["Name"].str.strip().str.casefold() == str(asset["spot_name"]).strip().casefold()
        if not matches.any():
            continue
        row_index = matches[matches].index[0]
        current = str(cleaned.at[row_index, "Gallery Image"]).strip()
        cleaned.at[row_index, "Gallery Image"] = " | ".join(filter(None, [current, asset["filename"]]))
        metadata = []
        existing = cleaned.at[row_index, "Gallery Metadata"]
        if pd.notna(existing) and str(existing).strip():
            try: metadata = json.loads(existing)
            except (TypeError, json.JSONDecodeError): metadata = []
        metadata.append({key: asset.get(key) for key in ("filename", "photo_no", "photo_name", "title", "date")})
        cleaned.at[row_index, "Gallery Metadata"] = json.dumps(metadata, default=str)
    return cleaned, assets


def save_uploaded_data(df, assets=None, filename=None, persist=False):
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    for existing in GALLERY_DIR.iterdir():
        if existing.is_file():
            existing.unlink()
    for asset in assets or []:
        (GALLERY_DIR / asset["filename"]).write_bytes(asset["data"])
    if persist:
        derived = ["Capacity Numeric", "Available Capacity", "Occupancy Rate", "Status"]
        df.drop(columns=derived, errors="ignore").to_csv(DEFAULT_DATA_FILE, index=False, encoding="utf-8")
        if filename:
            DATASET_INFO_FILE.write_text(json.dumps({"filename": filename}, indent=2), encoding="utf-8")
