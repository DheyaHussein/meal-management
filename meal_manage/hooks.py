app_name = "meal_manage"
app_title = "Meal Management"
app_publisher = "diaa"
app_description = "meal management"
app_email = "diaa@email.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "meal_manage",
# 		"logo": "/assets/meal_manage/logo.png",
# 		"title": "Meal Management",
# 		"route": "/meal_manage",
# 		"has_permission": "meal_manage.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/meal_manage/css/meal_manage.css"
# app_include_js = "/assets/meal_manage/js/meal_manage.js"

# include js, css files in header of web template
# web_include_css = "/assets/meal_manage/css/meal_manage.css"
# web_include_js = "/assets/meal_manage/js/meal_manage.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "meal_manage/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "meal_manage/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "meal_manage.utils.jinja_methods",
# 	"filters": "meal_manage.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "meal_manage.install.before_install"
# after_install = "meal_manage.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "meal_manage.uninstall.before_uninstall"
# after_uninstall = "meal_manage.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "meal_manage.utils.before_app_install"
# after_app_install = "meal_manage.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "meal_manage.utils.before_app_uninstall"
# after_app_uninstall = "meal_manage.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "meal_manage.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"meal_manage.tasks.all"
# 	],
# 	"daily": [
# 		"meal_manage.tasks.daily"
# 	],
# 	"hourly": [
# 		"meal_manage.tasks.hourly"
# 	],
# 	"weekly": [
# 		"meal_manage.tasks.weekly"
# 	],
# 	"monthly": [
# 		"meal_manage.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "meal_manage.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "meal_manage.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "meal_manage.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["meal_manage.utils.before_request"]
# after_request = ["meal_manage.utils.after_request"]

# Job Events
# ----------
# before_job = ["meal_manage.utils.before_job"]
# after_job = ["meal_manage.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"meal_manage.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [{"doctype": "Custom Field", "filters": [{"module": "meal management"}]}, "Translation", "Client Script", ]

