# SOCOCA Monitoring Portal

One Streamlit application with a shared Supabase login for:

- Incident Dashboard
- Evacuation Dashboard
- Future CLUP Monitoring module

## Run locally

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
2. Add the same Supabase credentials used by the current Incident Dashboard.
3. Make sure the Incident and Evacuation tables/storage buckets already exist in that Supabase project.
4. Install dependencies: `pip install -r requirements.txt`
5. Start the portal: `streamlit run app.py`

The portal signs users in through the Incident Dashboard's Supabase Auth and `accounts` table. The Evacuation Dashboard inherits that username, role, active status, and assigned dashboard. User creation and password management remain in the Incident Dashboard's Admin Settings so there is only one account source.

## Streamlit Community Cloud

Set the main file path to `app.py` and copy the required values from your local `secrets.toml` into the app's Secrets settings. Never commit the real secrets file.
