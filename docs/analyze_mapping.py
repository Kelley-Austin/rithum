import openpyxl
import xml.etree.ElementTree as ET

NS = 'http://soap.sforce.com/2006/04/metadata'

# === Parse spreadsheet ===
wb = openpyxl.load_workbook('docs/Global Support - Salesforce Categories- 2026.xlsx')
ws = wb['Final for 2026']

sheet_mapping = {}
sheet_categories = set()
current_category = None

for row in ws.iter_rows(min_row=2, values_only=True):
    cat    = str(row[0]).strip() if row[0] is not None else ''
    subcat = str(row[3]).strip() if row[3] is not None else ''
    if cat and cat != 'Category':
        current_category = cat
        sheet_categories.add(cat)
    if subcat and current_category:
        sheet_mapping.setdefault(subcat, set()).add(current_category)

# === Parse existing Category_dsco__c ===
tree = ET.parse('force-app/main/default/objects/Case/fields/Category_dsco__c.field-meta.xml')
root = tree.getroot()
existing_cat_values = set()
for v in root.findall('.//{%s}valueSetDefinition/{%s}value/{%s}fullName' % (NS, NS, NS)):
    existing_cat_values.add(v.text)

# === Parse existing Sub_Category_dsco__c ===
tree2 = ET.parse('force-app/main/default/objects/Case/fields/Sub_Category_dsco__c.field-meta.xml')
root2 = tree2.getroot()
existing_subcat_values = set()
for v in root2.findall('.//{%s}valueSetDefinition/{%s}value/{%s}fullName' % (NS, NS, NS)):
    existing_subcat_values.add(v.text)

# Parse existing valueSettings: {valueName: set(controllingFieldValues)}
existing_vs = {}
for vs in root2.findall('.//{%s}valueSettings' % NS):
    vname_el = vs.find('{%s}valueName' % NS)
    if vname_el is None:
        continue
    vname = vname_el.text
    cfvs = set(el.text for el in vs.findall('{%s}controllingFieldValue' % NS))
    existing_vs[vname] = cfvs

# === Compute changes ===
new_cats = sheet_categories - existing_cat_values
existing_cats_not_in_sheet = existing_cat_values - sheet_categories

new_subcats = set(sheet_mapping.keys()) - existing_subcat_values

# Existing sub-cats that need new category mappings added
updated_vs = {}
for subcat, cats in sheet_mapping.items():
    current_cfvs = existing_vs.get(subcat, set())
    missing_cfvs = cats - current_cfvs
    if missing_cfvs:
        updated_vs[subcat] = {'current': current_cfvs, 'add': missing_cfvs}

print("=== NEW CATEGORIES TO ADD ===")
for c in sorted(new_cats):
    print("  + " + c)

print("\n=== EXISTING CATEGORIES NOT IN SHEET (kept, not removed) ===")
for c in sorted(existing_cats_not_in_sheet):
    print("  ~ " + c)

print("\n=== NEW SUB-CATEGORIES TO ADD (%d) ===" % len(new_subcats))
for s in sorted(new_subcats):
    print("  + " + s + "  -->  " + str(sorted(sheet_mapping[s])))

print("\n=== EXISTING SUB-CATEGORIES NEEDING NEW CATEGORY MAPPINGS ===")
for s, info in sorted(updated_vs.items()):
    if s not in new_subcats:
        print("  ~ " + s)
        print("      current: " + str(sorted(info['current'])))
        print("      add:     " + str(sorted(info['add'])))
