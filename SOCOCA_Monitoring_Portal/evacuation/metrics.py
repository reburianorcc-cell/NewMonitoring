def dashboard_metrics(df):
    total = len(df)
    active = int((df["Actual No. of Evacuees"] > 0).sum())
    evacuees = int(df["Actual No. of Evacuees"].sum())
    available = int(df["Available Capacity"].sum())
    critical = int((df["Occupancy Rate"] >= 100).sum())
    return total, active, evacuees, available, critical


def profile_metrics(df):
    male = int(df["No. of Male"].sum())
    female = int(df["No. of Female"].sum())
    seniors = int(df["Senior Citizens"].sum())
    pwd = int(df["No. of PWD"].sum())
    total = int(df["Actual No. of Evacuees"].sum())
    unclassified = max(total - male - female, 0)
    return {"Male": male, "Female": female, "Senior Citizens": seniors, "PWD": pwd, "Unclassified": unclassified}

