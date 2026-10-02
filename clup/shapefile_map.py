from __future__ import annotations

import json
import math
import struct
import tempfile
import zipfile
from pathlib import Path

import plotly.graph_objects as go

try:
    import shapefile
except ImportError:
    shapefile = None

try:
    from pyproj import CRS, Transformer
except ImportError:
    CRS = None
    Transformer = None


MUNICIPALITY_HINTS = ("municipality", "municipal", "mun_name", "munname", "city_mun", "citymun", "city", "name_2", "adm3_en", "lgu")
BARANGAY_HINTS = ("barangay", "brgy_name", "brgyname", "brgy", "village", "name_3", "adm4_en")
MAP_COLORS = (
    "#15803d", "#22c55e", "#84cc16", "#facc15", "#f97316",
    "#ef4444", "#2563eb", "#7c3aed", "#db2777", "#0891b2",
)


def _safe_value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _transform_coordinates(coordinates, transformer):
    if not coordinates:
        return coordinates
    if isinstance(coordinates[0], (int, float)):
        x, y = transformer.transform(coordinates[0], coordinates[1])
        return [x, y, *coordinates[2:]]
    return [_transform_coordinates(item, transformer) for item in coordinates]


def _guess_field(fields, hints, excluded=None):
    excluded = excluded or set()
    lowered = {field.lower(): field for field in fields if field not in excluded}
    for hint in hints:
        if hint in lowered:
            return lowered[hint]
    for field in fields:
        if field in excluded:
            continue
        key = field.lower()
        if any(hint in key for hint in hints):
            return field
    return next((field for field in fields if field not in excluded), None)


def _dbf_value(raw, field_type, decimals, encoding):
    text = raw.decode(encoding, errors="replace").strip().strip("\x00")
    if not text:
        return None
    if field_type in {"N", "F"}:
        try:
            number = float(text)
            return int(number) if decimals == 0 and number.is_integer() else number
        except ValueError:
            return text
    if field_type == "L":
        return text.upper() in {"Y", "T", "1"}
    return text


def _read_dbf(path):
    data = path.read_bytes()
    if len(data) < 33:
        raise ValueError("The DBF attribute file is invalid.")
    record_count = struct.unpack_from("<I", data, 4)[0]
    header_length = struct.unpack_from("<H", data, 8)[0]
    record_length = struct.unpack_from("<H", data, 10)[0]
    cpg_path = path.with_suffix(".cpg")
    encoding = cpg_path.read_text(encoding="ascii", errors="ignore").strip() if cpg_path.exists() else "cp1252"
    encoding = encoding or "cp1252"

    field_descriptors = []
    offset = 32
    while offset + 32 <= header_length and data[offset] != 0x0D:
        descriptor = data[offset:offset + 32]
        name = descriptor[:11].split(b"\x00", 1)[0].decode("ascii", errors="replace")
        field_descriptors.append((name, chr(descriptor[11]), descriptor[16], descriptor[17]))
        offset += 32

    records = []
    for index in range(record_count):
        start = header_length + index * record_length
        record = data[start:start + record_length]
        if len(record) < record_length or record[:1] == b"*":
            continue
        values = {}
        position = 1
        for name, field_type, length, decimals in field_descriptors:
            values[name] = _dbf_value(record[position:position + length], field_type, decimals, encoding)
            position += length
        records.append(values)
    return [field[0] for field in field_descriptors], records


def _signed_area(ring):
    return sum(
        ring[index][0] * ring[(index + 1) % len(ring)][1]
        - ring[(index + 1) % len(ring)][0] * ring[index][1]
        for index in range(len(ring))
    ) / 2


def _read_shp_polygons(path):
    data = path.read_bytes()
    if len(data) < 100 or struct.unpack_from(">I", data, 0)[0] != 9994:
        raise ValueError("The SHP geometry file is invalid.")
    geometries = []
    offset = 100
    while offset + 8 <= len(data):
        _, content_words = struct.unpack_from(">2I", data, offset)
        content_start = offset + 8
        content_end = content_start + content_words * 2
        content = data[content_start:content_end]
        offset = content_end
        if len(content) < 4:
            continue
        shape_type = struct.unpack_from("<I", content, 0)[0]
        if shape_type == 0:
            geometries.append(None)
            continue
        if shape_type not in {5, 15, 25} or len(content) < 44:
            raise ValueError("Only polygon Shapefiles are supported by the built-in reader.")
        part_count, point_count = struct.unpack_from("<2I", content, 36)
        parts_offset = 44
        points_offset = parts_offset + part_count * 4
        if points_offset + point_count * 16 > len(content):
            raise ValueError("A polygon record in the SHP file is incomplete.")
        part_starts = list(struct.unpack_from(f"<{part_count}I", content, parts_offset))
        points = [list(struct.unpack_from("<2d", content, points_offset + index * 16)) for index in range(point_count)]
        rings = []
        for part_index, start in enumerate(part_starts):
            end = part_starts[part_index + 1] if part_index + 1 < len(part_starts) else point_count
            ring = points[start:end]
            if len(ring) >= 3:
                if ring[0] != ring[-1]:
                    ring.append(ring[0])
                if _signed_area(ring) < 0:
                    ring.reverse()
                rings.append(ring)
        if len(rings) == 1:
            geometries.append({"type": "Polygon", "coordinates": rings})
        else:
            geometries.append({"type": "MultiPolygon", "coordinates": [[ring] for ring in rings]})
    return geometries


def _read_with_builtin_parser(shp_path):
    fields, records = _read_dbf(shp_path.with_suffix(".dbf"))
    geometries = _read_shp_polygons(shp_path)
    usable_count = min(len(records), len(geometries))
    return fields, records[:usable_count], geometries[:usable_count]


def _parse_shapefile_directory(temp_path):
    shapefiles = list(temp_path.rglob("*.shp"))
    if not shapefiles:
        raise ValueError("No .shp file was uploaded.")
    shp_path = shapefiles[0]
    for suffix in (".shx", ".dbf"):
        if not shp_path.with_suffix(suffix).exists():
            raise ValueError(f"The matching {suffix} file is missing. Select all matching Shapefile components together.")

    if shapefile is None:
        fields, records, geometries = _read_with_builtin_parser(shp_path)
    else:
        reader = shapefile.Reader(str(shp_path), encodingErrors="replace")
        try:
            fields = [field[0] for field in reader.fields[1:]]
            shape_records = list(reader.iterShapeRecords())
            records = [shape_record.record.as_dict() for shape_record in shape_records]
            geometries = [shape_record.shape.__geo_interface__ for shape_record in shape_records]
        finally:
            reader.close()
    municipality_field = _guess_field(fields, MUNICIPALITY_HINTS)
    barangay_field = _guess_field(fields, BARANGAY_HINTS, {municipality_field})

    transformer = None
    prj_path = shp_path.with_suffix(".prj")
    if prj_path.exists():
        projection_text = prj_path.read_text(encoding="utf-8", errors="ignore")
        is_wgs84 = "GEOGCS" in projection_text.upper() and ("WGS_1984" in projection_text.upper() or "WGS 84" in projection_text.upper())
        if not is_wgs84:
            if CRS is None or Transformer is None:
                raise ValueError("This Shapefile uses a projected coordinate system. Install pyproj to convert it: pip install pyproj")
            source_crs = CRS.from_wkt(projection_text)
            if source_crs != CRS.from_epsg(4326):
                transformer = Transformer.from_crs(source_crs, "EPSG:4326", always_xy=True)

    features = []
    for index, (record, original_geometry) in enumerate(zip(records, geometries)):
        if not original_geometry:
            continue
        geometry = original_geometry
        if geometry.get("type") not in {"Polygon", "MultiPolygon"}:
            continue
        if transformer and geometry.get("coordinates"):
            geometry = dict(geometry)
            geometry["coordinates"] = _transform_coordinates(geometry["coordinates"], transformer)
        properties = {key: _safe_value(value) for key, value in record.items()}
        features.append({"type": "Feature", "id": str(index), "properties": properties, "geometry": geometry})

    if not features:
        raise ValueError("The Shapefile does not contain polygon features.")
    geojson = {"type": "FeatureCollection", "features": features}
    json.dumps(geojson)
    return geojson, fields, municipality_field, barangay_field, shp_path.name


def parse_shapefile_files(uploaded_files):
    """Parse individually uploaded Shapefile component files."""
    if not uploaded_files:
        raise ValueError("Select the Shapefile component files first.")
    allowed_suffixes = {".shp", ".shx", ".dbf", ".prj", ".cpg"}
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for uploaded_file in uploaded_files:
            safe_name = Path(uploaded_file.name).name
            suffix = Path(safe_name).suffix.lower()
            if suffix not in allowed_suffixes:
                raise ValueError(f"Unsupported Shapefile component: {safe_name}")
            (temp_path / safe_name).write_bytes(uploaded_file.getvalue())
        return _parse_shapefile_directory(temp_path)


def parse_shapefile_zip(file_bytes):
    """Parse the bundled sample ZIP for compatibility and testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with zipfile.ZipFile(file_bytes) as archive:
            members = [member for member in archive.infolist() if not member.is_dir()]
            if not members:
                raise ValueError("The ZIP file is empty.")
            for member in members:
                destination = (temp_path / member.filename).resolve()
                if temp_path.resolve() not in destination.parents:
                    raise ValueError("The ZIP contains an unsafe file path.")
            archive.extractall(temp_path)
        return _parse_shapefile_directory(temp_path)


def boundary_names(geojson, field, parent_field=None, parent_value=None):
    if not field:
        return []
    names = set()
    for feature in geojson.get("features", []):
        properties = feature.get("properties", {})
        if parent_field and parent_value not in (None, "All Municipalities"):
            if str(properties.get(parent_field, "")) != parent_value:
                continue
        value = str(properties.get(field, "")).strip()
        if value and value.lower() not in {"none", "nan"}:
            names.add(value)
    return sorted(names)


def _coordinate_pairs(value):
    if not value:
        return
    if isinstance(value[0], (int, float)):
        yield value[0], value[1]
        return
    for child in value:
        yield from _coordinate_pairs(child)


def _map_view(features):
    points = []
    for feature in features:
        points.extend(_coordinate_pairs(feature.get("geometry", {}).get("coordinates", [])))
    if not points:
        return {"lat": 13.4, "lon": 123.4}, 6.5
    longitudes, latitudes = zip(*points)
    center = {"lon": (min(longitudes) + max(longitudes)) / 2, "lat": (min(latitudes) + max(latitudes)) / 2}
    span = max(max(longitudes) - min(longitudes), max(latitudes) - min(latitudes), .01)
    return center, max(4.5, min(13, 8.3 - math.log(span, 2)))


def municipality_barangay_map(
    geojson,
    municipality_field,
    barangay_field,
    selected_municipality="All Municipalities",
    selected_barangay="All Barangays",
    legend_field=None,
):
    features = geojson.get("features", [])
    visible_features = features
    if selected_municipality != "All Municipalities":
        visible_features = [
            feature for feature in visible_features
            if str(feature.get("properties", {}).get(municipality_field, "")).strip() == selected_municipality.strip()
        ]
    if selected_barangay != "All Barangays":
        visible_features = [
            feature for feature in visible_features
            if str(feature.get("properties", {}).get(barangay_field, "")).strip() == selected_barangay.strip()
        ]

    is_filtered = selected_municipality != "All Municipalities" or selected_barangay != "All Barangays"
    display_features = visible_features if is_filtered else features
    center, zoom = _map_view(display_features)
    active_legend_field = legend_field or (
        municipality_field if selected_municipality == "All Municipalities" else barangay_field
    )
    grouped_features = {}
    for feature in display_features:
        label = str(feature.get("properties", {}).get(active_legend_field, "Unnamed")).strip() or "Unnamed"
        grouped_features.setdefault(label, []).append(feature)

    figure = go.Figure()
    for color_index, (label, category_features) in enumerate(sorted(grouped_features.items())):
        color = "#f97316" if selected_barangay != "All Barangays" else MAP_COLORS[color_index % len(MAP_COLORS)]
        municipality_names = [str(feature.get("properties", {}).get(municipality_field, "Unnamed")) for feature in category_features]
        barangay_names = [str(feature.get("properties", {}).get(barangay_field, "Unnamed")) for feature in category_features]
        figure.add_trace(go.Choroplethmap(
            geojson={"type": "FeatureCollection", "features": category_features},
            locations=[feature["id"] for feature in category_features],
            z=[1] * len(category_features),
            featureidkey="id",
            customdata=list(zip(municipality_names, barangay_names)),
            colorscale=[[0, color], [1, color]],
            showscale=False,
            showlegend=True,
            marker_opacity=.82,
            marker_line_width=2.2 if selected_barangay != "All Barangays" else 1.1,
            marker_line_color="#9a3412" if selected_barangay != "All Barangays" else "#ffffff",
            hovertemplate="<b>%{customdata[1]}</b><br>Municipality: %{customdata[0]}<extra></extra>",
            name=label,
        ))

    figure.update_layout(
        height=650,
        margin=dict(l=0, r=190, t=0, b=0),
        map=dict(style="open-street-map", center=center, zoom=zoom),
        showlegend=True,
        legend=dict(
            title=dict(text=(active_legend_field or "Map Legend").replace("_", " ").title()),
            orientation="v",
            x=1.01,
            xanchor="left",
            y=1,
            yanchor="top",
            bgcolor="rgba(255,255,255,.94)",
            bordercolor="#d1d5db",
            borderwidth=1,
            font=dict(size=11, color="#0f172a"),
        ),
        paper_bgcolor="#ffffff",
    )
    return figure
