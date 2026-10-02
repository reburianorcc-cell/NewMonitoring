create extension if not exists pgcrypto;

-- CLUP uses the portal's existing Supabase Auth users and public.accounts table.
create table if not exists public.clup_dashboards (
  name text primary key,
  source_name text,
  master_data jsonb not null default '[]'::jsonb,
  locational_data jsonb not null default '[]'::jsonb,
  reclassification_data jsonb not null default '[]'::jsonb,
  land_dispute_data jsonb not null default '[]'::jsonb,
  documents_data jsonb not null default '[]'::jsonb,
  map_data jsonb not null default '{}'::jsonb,
  updated_by text,
  updated_at timestamptz not null default now()
);

create table if not exists public.clup_upload_history (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  username text not null,
  dashboard_name text not null,
  section text not null,
  source_name text
);

alter table public.clup_dashboards enable row level security;
alter table public.clup_upload_history enable row level security;

-- Safe upgrade for an existing CLUP database. Existing rows are preserved.
alter table public.clup_dashboards add column if not exists land_dispute_data jsonb not null default '[]'::jsonb;
alter table public.clup_dashboards add column if not exists documents_data jsonb not null default '[]'::jsonb;
alter table public.clup_dashboards add column if not exists map_data jsonb not null default '{}'::jsonb;

-- Add one missing history entry for maps saved before map history was enabled.
insert into public.clup_upload_history (
  created_at,
  username,
  dashboard_name,
  section,
  source_name
)
select
  d.updated_at,
  coalesce(nullif(d.updated_by, ''), 'system'),
  d.name,
  'Municipality Map',
  d.map_data ->> 'source_name'
from public.clup_dashboards d
where d.map_data ? 'geojson'
  and d.map_data -> 'geojson' is not null
  and not exists (
    select 1
    from public.clup_upload_history h
    where h.dashboard_name = d.name
      and h.section = 'Municipality Map'
      and coalesce(h.source_name, '') = coalesce(d.map_data ->> 'source_name', '')
  );

-- Access is performed by the server-side secret/service key after portal login.
-- No starter records are inserted and existing CLUP records are never reset.
