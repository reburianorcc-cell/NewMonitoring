# CLUP Monitoring Module

This module runs inside the SOCOCA Monitoring Portal and uses the Incident Dashboard's existing Supabase Auth session and `accounts` table.

## Access

- Super Admin and Admin: view, create, update, and delete CLUP dashboards.
- Operator: view and upload data only for the dashboard assigned in the portal's Admin Settings.

## Database setup

Run `supabase_setup.sql` once in the same Supabase project used by the portal. It creates the CLUP tables when missing and safely adds the JSONB columns needed by the new sections. It does not reset existing data or create another account system.

## Added sections

- **Boundary Disputes:** upload Excel/CSV records, filter by municipality and barangay, view the status chart, and delete records as an administrator.
- **PDF Documents:** upload PDFs, assign a title and municipality, display the PDF content inside the dashboard, and delete selected files as an administrator.
- **Municipality Map:** upload matching `.shp`, `.shx`, and `.dbf` files together, optionally include `.prj` and `.cpg`, select the municipality/barangay attributes, display a legend, and filter exact boundaries.
