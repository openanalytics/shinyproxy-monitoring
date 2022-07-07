import json
import sys

with open(sys.argv[1]) as fh:
    dashboard = json.load(fh)

dashboard["editable"] = False
dashboard["refresh"] = "10s"
dashboard["time"]["from"] = "now-30m"
dashboard["time"]["to"] = "now"
dashboard["time"]["timezone"] = "browser"

for panel in dashboard["panels"]:
    datasource = panel["datasource"]['uid']
    if datasource != "${datasource}":
        print("ERROR: found panel with invalid datasource, must use variable", panel["title"])
        sys.exit(10)

for template in dashboard["templating"]["list"]:
    if template["name"] == "level":
        template["current"] = {"selected": True,
                               "text": ["All"],
                               "value": ["$__all"]
                               }
    else:
        template["current"] = {}

    if template["name"] != "level" and template["name"] != "datasource":
        template["refresh"] = 2
        template["sort"] = 5

    if "datasource" in template and template["datasource"]["uid"] != "${datasource}":
        print("ERROR: found panel with invalid datasource, must use variable")
        sys.exit(10)

with open(sys.argv[1], "w") as fh:
    json.dump(dashboard, fh, indent=2)
