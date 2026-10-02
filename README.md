# SOCOCA Monitoring Portal

One Streamlit application with a shared Supabase login for:

- Incident Dashboard
- Evacuation Dashboard
- CLUP Monitoring Dashboard

## Run locally

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
2. Copy both `[supabase]` and `[connections.postgres]` from the current Incident Dashboard's `.streamlit/secrets.toml`. The PostgreSQL connection is required for Incident records; Supabase API keys alone are not enough.
3. Make sure the Incident and Evacuation tables/storage buckets already exist in that Supabase project.
4. Run `clup/supabase_setup.sql` once in the same Supabase project's SQL Editor.
5. Install dependencies: `pip install -r requirements.txt`
6. Start the portal: `streamlit run app.py`

The portal signs users in through the Incident Dashboard's Supabase Auth and `accounts` table. Evacuation and CLUP inherit that username, role, active status, and assigned dashboard. Operators can view and upload only to their assigned dashboard. User creation, assignment, and password management remain in the Incident Dashboard's Admin Settings so there is only one account source.

## Streamlit Community Cloud

Set the main file path to `app.py` and copy the required values from your local `secrets.toml` into the app's Secrets settings. Never commit the real secrets file.
