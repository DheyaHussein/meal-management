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
def calculate_ingredients_for_meal(meal_name, people=1):
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
        qty = (ing.qty_per_person or 0) * int(people) * ing.num_weeks
        key = ing.item_code
        # We should deivide by the conversion factor to get stock UOM qty
        # for example if the uom is "كيس*40"  so we divide by 40000 to cunvert from grams to bags
        # we should check if the uom and make the conversion without using the conversion factor from item master
        # we can add a list of known uoms that need conversion
        #     qty = qty / float(ing.uom.split("*")[-1])
        known_uoms = {"كيس*40": 40000, "كيس*50": 50, "راس": 10}
        items = [
                "كيس رز*40",
                "دجاج مثلج ابو700*10",
                "لحم ثور تبيع وزن 110 كيلو",
                "فاصوليا حمراء *50كيلو",
                "فاصولياء سبعه نجوم علب*24",
                "بزالياء علب *24",
                "فول صيني *24",
                "عدس *15ك",
                "فول *25 كيلو",
                "جبن مالح15كيلو",
                "تنك حلوى 13 كيلو",
                "جبن مثلث12*24",
                "بيض*12*30",
                "قشطة*48",
                "عسل *48",
                "زيت 20لتر",
                "صلصه * 12 علبة *350 جرام",
                "ملح *20 ك",
                "كمون مطحون ×25 ك",
                "كبزرة حبوب *10 ك",
                "بسباس حيمي *25 ك",
                "فلفل حبوب ×25كيلو",
                "هرد*25ك ؤ",
                "قرفة *10 ك",
                "قرنفل*5 ك",
                "هيل *5 ك",
                "مجموع بهارات *20باكت",
                "كاري *36 باكت",
                "موتو 1×2*40باكت",
                "ليم مجفف *10",
                "رول تغليف",
                "قصدير*6",
                "خل ابيض *12",
                "بسباس عدني*70 ك",
                "صفار البيض*80",
                "صفار الزعفران",
                "صفار البرتقال",
                "دقن الشيبه",
                "صبغة رز حمرا ×100",
                "عصير منوع*24 حبه",
                "عصير اوليفر منوع* 27 حبه",
                "حليب بقري صغير*28",
                "بسكويت سمايلي 60 حبه",
                "بسكويت ابو ولد",
                "كيك*144",
                "بيبسي منوع*30",
                "طماط 20ك",
                "بطاط 22ك",
                "جزر 10ك",
                "كوسة 15ك",
                "بسباس 21 كيلو",
                "سوادي 8ك",
                "بيبار 8ك",
                "بصل 20ك",
                "ثوم 9ك"
            ]
        
        # if ing.item_code in items:
        #     qty = qty / 1000  # convert grams to kilos for these items only

        if ing.uom in known_uoms:
            qty = float(qty / known_uoms[ing.uom])
            print(qty)
        if key in summary:
            summary[key]["qty"] += qty
        else:
            summary[key] = {"item_code": key, "qty": qty, "uom": ing.uom}

    return list(summary.values())





@frappe.whitelist()
def create_stock_entry_from_calculator(calc_name, from_warehouse=None):
    """
    Create a Stock Entry (Material Issue) from a saved Meal Production Calculator doc.
    This version is defensive: it works even if the calculator doc doesn't have a `company`
    field and it tolerates a few common child-field name differences.
    """
    # fetch calculator (raises if not found)
    calc = frappe.get_doc("Meal Production Calculator", calc_name)

    # --- determine company safely ---
    company = None
    # prefer a company field on the doc if present
    if hasattr(calc, "company") and calc.get("company"):
        company = calc.company
    # else try user default
    if not company:
        company = frappe.defaults.get_user_default("Company")
    # else try global defaults cached
    if not company:
        try:
            company = frappe.get_cached_value("Global Defaults", None, "default_company")
        except Exception:
            company = None
    # final fallback: try first Company record
    if not company:
        try:
            company_doc = frappe.get_all("Company", fields=["name"], limit_page_length=1)
            company = company_doc[0].name if company_doc else None
        except Exception:
            company = None

    if not company:
        frappe.throw("Company could not be determined. Please set a Company in the Calculator or in your User/Global Defaults.")

    # --- aggregate ingredient totals from calculator child table ---
    summary = {}
    # support multiple possible child table fieldnames: 'required_ingredients' (recommended),
    # 'required_items', or fallback to attribute access
    ingredient_rows = []
    if hasattr(calc, "required_ingredients"):
        ingredient_rows = calc.required_ingredients
    elif hasattr(calc, "required_items"):
        ingredient_rows = calc.required_items
    else:
        # look for any child table by scanning fields (last-resort)
        for f in (getattr(calc, "__dict__", {}) or {}):
            val = getattr(calc, f, None)
            if isinstance(val, list) and val and hasattr(val[0], "doctype"):
                # take the first reasonable list that looks like a child table
                ingredient_rows = val
                break

    # now extract item_code and qty robustly (support 'item_code' or 'ingredient' and 'quantity' or 'qty')
    for row in ingredient_rows:
        item_code = row.get("item_code") if isinstance(row, dict) else getattr(row, "item_code", None)
        if not item_code:
            item_code = row.get("ingredient") if isinstance(row, dict) else getattr(row, "ingredient", None)
        qty = None
        if isinstance(row, dict):
            qty = row.get("quantity") or row.get("qty") or row.get("quantity_per_serving")
            uom = row.get("uom")
        else:
            qty = getattr(row, "quantity", None) or getattr(row, "qty", None) or getattr(row, "quantity_per_serving", None)
            uom = getattr(row, "uom", None)

        # skip invalid rows
        if not item_code or not qty:
            continue

        # aggregate
        key = item_code
        if key in summary:
            summary[key]["qty"] += float(qty)
        else:
            summary[key] = {"item_code": key, "qty": float(qty), "uom": uom}

    if not summary:
        frappe.throw("No ingredients found in the calculator (check required_ingredients child table).")

    # --- enrich rows via ERPNext API and build Stock Entry rows ---
    se_rows = []
    for i in summary.values():
        args = {
            "item_code": i["item_code"],
            "company": company,
            "from_warehouse": from_warehouse or getattr(calc, "from_warehouse", None),
            "to_warehouse": None,
            "doctype": "Stock Entry",
            "docname": "",
            "stock_entry_type": "Material Issue",
            "qty": i["qty"],
            "uom": i.get("uom")
        }

        # get full row details (warehouse, conversion factor, expense account, etc.)
        try:
            details = get_item_details(args)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "create_stock_entry_from_calculator.get_item_details_error")
            details = None

        if details:
            # ensure qty is exact from calculation
            details["qty"] = i["qty"]
            se_rows.append(details)
        else:
            # fallback minimal row if get_item_details failed (still try to proceed)
            se_rows.append({
                "item_code": i["item_code"],
                "qty": i["qty"],
                "uom": i.get("uom"),
                "s_warehouse": args.get("from_warehouse")
            })

    # --- create the Stock Entry doc and insert enriched rows ---
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    # se.naming_series = "MAT-ISS-.YYYY.-"
    se.company = company
    se.set_posting_time = 1

    for d in se_rows:
        # append full dict — keys must match Stock Entry Detail fieldnames
        se.append("items", d)

    se.insert()
    return se.name
# Custom Permissions
# ------------------
# Custom permissions can be defined in a standard way as that of Frappe.
# For example, to restrict Event to be visible only to Event Owners:    