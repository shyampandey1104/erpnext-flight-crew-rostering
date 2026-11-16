# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "aviation"
app_title = "Erpnext Flight Crew Rostering"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Flight Crew Rostering for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/aviation/css/aviation.bundle.css"
app_include_js = "/assets/aviation/js/aviation.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "aviation.engine.on_document_submit",
        "on_cancel": "aviation.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "aviation.engine.daily_scheduled_sync"
    ]
}
