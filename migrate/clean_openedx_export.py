import json

with open("migrate/export-openedx.json") as f:
    raw = json.load(f)

cleaner = {
    "export_date_utc": raw["export_date_utc"],
    "repo_teams": {
        "write": {
            repo["name"]: [
                team_slug
                for team_slug, level in repo["team_access"].items()
                if level == 2
            ]
            for repo in raw["repos"]
        },
        "maintain": {
            repo["name"]: [
                team_slug
                for team_slug, level in repo["team_access"].items()
                if level == 3
            ]
            for repo in raw["repos"]
        },
        "admin": {
            repo["name"]: [
                team_slug
                for team_slug, level in repo["team_access"].items()
                if level == 4 and team_slug != "openedx-admin"
            ]
            for repo in raw["repos"]
        },
    },
    "repo_users": {
        "write": {
            repo["name"]: [
                username
                for username, level in repo["user_access"].items()
                if level == 2
            ]
            for repo in raw["repos"]
        },
        "maintain": {
            repo["name"]: [
                username
                for username, level in repo["user_access"].items()
                if level == 3
            ]
            for repo in raw["repos"]
        },
        "admin": {
            repo["name"]: [
                username
                for username, level in repo["user_access"].items()
                if level == 4
            ]
            for repo in raw["repos"]
        },
    },
    "team_members": {
        team["slug"]: team["members"]
        for team in raw["teams"]
        if team["slug"] != "openedx-admin"
    },
}


cleanest = {
    **cleaner,
    **{
        scheme: {
            access: {
                repo_name: teams
                for repo_name, teams in repo_teams.items()
                if teams
            }
            for access, repo_teams in cleaner[scheme].items()
        }
        for scheme in ["repo_teams", "repo_users"]
    },
}

with open("migrate/export-openedx-clean.json", 'w') as f:
    json.dump(cleanest, f, indent=4)
