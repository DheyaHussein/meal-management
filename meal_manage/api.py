# # import frappe

# # @frappe.whitelist()
# # def get_ingredients_from_schedule(schedule):
# #     schedule_doc = frappe.get_doc("Meal Schedule", schedule)
# #     summary = {}

# #     for row in schedule_doc.items:
# #         meal = frappe.get_doc("Meal Recipe", row.meal)
# #         for ingredient in meal.ingredients:   # child table in Meal Recipe
# #             total = ingredient.qty_per_person * row.people
# #             key = ingredient.item_code   # <-- fieldname, not label
# #             if key in summary:
# #                 summary[key]["qty"] += total
# #             else:
# #                 summary[key] = {
# #                     "item_code": ingredient.item_code,
# #                     "qty": total,
# #                     "uom": ingredient.uom
# #                 }
# #             print(list(summary.values()))

# #     return list(summary.values())

# import frappe

# @frappe.whitelist()
# def calculate_stock_entry_meals(stock_entry):
#     doc = frappe.get_doc("Stock Entry", stock_entry)
#     summary = {}

#     for row in doc.custom_meals:   # our new child table
#         meal = frappe.get_doc("Meal Recipe", row.meal)
#         for ingredient in meal.ingredients:
#             total = ingredient.qty_per_person * row.people
#             key = ingredient.item_code
#             if key in summary:
#                 summary[key]["qty"] += total
#             else:
#                 summary[key] = {
#                     "item_code": ingredient.item_code,
#                     "qty": total,
#                     "uom": ingredient.uom
#                 }
#     return list(summary.values())




# apps/meal_manage/meal_manage/api.py
import frappe
from erpnext.stock.get_item_details import get_item_details


@frappe.whitelist()
def calculate_ingredients_for_meal(meal_name, people=1, num_of_meals=1):
    """
    Return aggregated list of {item_code, qty, uom} for a meal and people count.
    """
    if not meal_name:
        return []

    meal = frappe.get_doc("Meal Recipe", meal_name)
    
    
    summary = {}

    for ing in meal.ingredients:
        #to do: handle if qty_per_person is None
        """Calculate total quantity needed for the ingredient.
           - add a parameter to handle the days of meal : for example if the meal is 
           for 3 days and people is 10 so we should multiply by 3*10* qty_per_person
           """
        # 
        qty = (ing.qty_per_person) * int(people) * int(num_of_meals)
        # print(num_of_meals)
        
        qty = float(qty/ing.convert_uom  )
        # print(qty)
        key = ing.item_code
        # We should deivide by the conversion factor to get stock UOM qty
        # for example if the uom is "كيس*40"  so we divide by 40000 to cunvert from grams to bags
        # we should check if the uom and make the conversion without using the conversion factor from item master
        # we can add a list of known uoms that need conversion
        #     qty = qty / float(ing.uom.split("*")[-1])
        # known_uoms = {"كيس*40": 40000, "كيس*50": 50, "راس": 10}

        
        # if ing.item_code in items:
        #     qty = qty / 1000  # convert grams to kilos for these items only

        # if ing.uom in known_uoms:
        #     qty = float(qty / known_uoms[ing.uom])
        #     print(qty)
        if key in summary:
            summary[key]["qty"] += qty
        else:
            summary[key] = {"item_code": key, "qty": qty, "uom": ing.uom}

    return list(summary.values())




@frappe.whitelist()
def create_stock_entry_from_calculator(calc_name, from_warehouse=None, custom_issue=None):
    """
    Create a Stock Entry (Material Issue) from Meal Production Calculator
    (ERPNext 15 compatible version — preserves float quantities like 0.230, 1.110, 10.417)
    """
    import frappe
    from frappe.utils import flt
    from erpnext.stock.get_item_details import get_item_details

    # --- Fetch Calculator ---
    calc = frappe.get_doc("Meal Production Calculator", calc_name)

    # --- Determine Company ---
    company = getattr(calc, "company", None) or frappe.defaults.get_user_default("Company")
    if not company:
        company = frappe.get_cached_value("Global Defaults", None, "default_company")
    if not company:
        frappe.throw("Company could not be determined. Please set it in Calculator or Defaults.")

    # --- Collect Ingredients ---
    rows = getattr(calc, "required_ingredients", []) or getattr(calc, "required_items", [])
    if not rows:
        frappe.throw("No ingredients found in the calculator (check Required Ingredients table).")

    # --- Aggregate Quantities ---
    summary = {}
    for row in rows:
        item_code = getattr(row, "item_code", None) or getattr(row, "ingredient", None)
        qty = (
            getattr(row, "quantity", None)
            or getattr(row, "qty", None)
            or getattr(row, "quantity_per_serving", None)
        )
        uom = getattr(row, "uom", None)

        if not item_code or qty in (None, ""):
            continue

        qty = flt(qty, 6)
        if item_code in summary:
            summary[item_code]["qty"] += qty
        else:
            summary[item_code] = {"item_code": item_code, "qty": qty, "uom": uom}

    # --- Build Item Rows for Stock Entry ---
    se_rows = []
    for data in summary.values():
        qty = flt(data["qty"], 6)
        args = {
            "item_code": data["item_code"],
            "company": company,
            "from_warehouse": from_warehouse or getattr(calc, "from_warehouse", None),
            "stock_entry_type": "Material Issue",
            "qty": qty,
            "uom": data.get("uom"),
        }

        try:
            details = get_item_details(args)
        except Exception:
            details = {}

        details.update({
            "item_code": data["item_code"],
            "qty": qty,
            "transfer_qty": qty,
            "uom": data.get("uom"),
            "s_warehouse": args.get("from_warehouse"),
            "basic_rate": details.get("basic_rate", 0.0)
        })
        se_rows.append(details)

    # --- Create Stock Entry ---
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.company = company
    se.set_posting_time = 1
    se.custom_issue_to = custom_issue or None

    for d in se_rows:
        se.append("items", d)

    # 🔹 Save normally (ERPNext will round values)
    se.insert(ignore_permissions=True)

    # 🔹 Immediately correct the float quantities directly in DB
    for row in se.items:
        precise_qty = flt(next((i["qty"] for i in se_rows if i["item_code"] == row.item_code), row.qty), 6)
        frappe.db.set_value(
            "Stock Entry Detail",
            row.name,
            {
                "qty": precise_qty,
                "transfer_qty": precise_qty,
                "stock_uom": row.stock_uom,
            },
            update_modified=False,
        )

    frappe.msgprint(f"✅ Stock Entry <b>{se.name}</b> created with full decimal precision.")
    return se.name


# Custom Permissions
# ------------------
# Custom permissions can be defined in a standard way as that of Frappe.
# For example, to restrict Event to be visible only to Event Owners:    