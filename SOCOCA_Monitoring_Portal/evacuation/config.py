from pathlib import Path

APP_TITLE = "Evacuation Center Dashboard"
APP_ICON = "🏠"
SUPABASE_BUCKET = "ev_dashboard"
ACCOUNTS_TABLE = "ev_dashboard_accounts"
DASHBOARDS_TABLE = "ev_dashboards"
HISTORY_TABLE = "ev_dashboard_history"
ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_DATA_FILE = DATA_DIR / "evacuation_centers.csv"
USERS_FILE = DATA_DIR / "users.json"
GALLERY_DIR = DATA_DIR / "gallery"
DATASET_INFO_FILE = DATA_DIR / "dataset_info.json"
DASHBOARDS_DIR = DATA_DIR / "dashboards"
DASHBOARDS_INDEX_FILE = DATA_DIR / "dashboards.json"
HISTORY_FILE = DATA_DIR / "history.json"

REQUIRED_COLUMNS = {
    "Name", "Address", "latitude", "longitude", "Capacity",
    "Actual No. of Evacuees", "No. of Male", "No. of Female",
    "No. of Senior Citizen", "No. of PWD",
}
