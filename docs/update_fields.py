"""
ST-22314: Update Category_dsco__c and Sub_Category_dsco__c field dependencies
to match the 'Final for 2026' sheet.

Safe approach:
  - Only ADDS new values / mappings; never removes existing ones.
  - Skips "Delivery Suite - Shipping Labels" (duplicate of existing "Delivery Suite" value).
"""
import openpyxl
import xml.etree.ElementTree as ET
import re

NS = 'http://soap.sforce.com/2006/04/metadata'
ET.register_namespace('', NS)

# Sub-categories in the sheet that are actually aliases of existing API names
SHEET_TO_EXISTING = {
    'Delivery Suite - Shipping Labels': 'Delivery Suite',
    'Missing Trading Partner': 'Missing trading partner',
}
SKIP_AS_NEW_VALUE = {'Delivery Suite - Shipping Labels'}

# ── Parse spreadsheet ───────────────────────────────────────────────────────
wb = openpyxl.load_workbook('docs/Global Support - Salesforce Categories- 2026.xlsx')
ws = wb['Final for 2026']

sheet_mapping = {}   # {canonical_subcat: set(categories)}
sheet_categories = set()
current_category = None

for row in ws.iter_rows(min_row=2, values_only=True):
    cat    = str(row[0]).strip() if row[0] is not None else ''
    subcat = str(row[3]).strip() if row[3] is not None else ''
    if cat and cat != 'Category':
        current_category = cat
        sheet_categories.add(cat)
    if subcat and current_category:
        canonical = SHEET_TO_EXISTING.get(subcat, subcat)
        sheet_mapping.setdefault(canonical, set()).add(current_category)

# ── Parse Category_dsco__c ──────────────────────────────────────────────────
cat_path = 'force-app/main/default/objects/Case/fields/Category_dsco__c.field-meta.xml'
cat_tree = ET.parse(cat_path)
cat_root = cat_tree.getroot()

existing_cats = set()
cat_vsd = cat_root.find('.//{%s}valueSetDefinition' % NS)
for v in cat_vsd.findall('{%s}value' % NS):
    fn = v.find('{%s}fullName' % NS)
    if fn is not None:
        existing_cats.add(fn.text)

# ── Parse Sub_Category_dsco__c ──────────────────────────────────────────────
sub_path = 'force-app/main/default/objects/Case/fields/Sub_Category_dsco__c.field-meta.xml'
sub_tree = ET.parse(sub_path)
sub_root = sub_tree.getroot()

existing_subcats = set()
sub_vsd = sub_root.find('.//{%s}valueSetDefinition' % NS)
for v in sub_vsd.findall('{%s}value' % NS):
    fn = v.find('{%s}fullName' % NS)
    if fn is not None:
        existing_subcats.add(fn.text)

# existing valueSettings: {valueName: set(controllingFieldValues)}
existing_vs = {}
sub_vs_parent = sub_root.find('.//{%s}valueSet' % NS)
for vs in sub_vs_parent.findall('{%s}valueSettings' % NS):
    vname_el = vs.find('{%s}valueName' % NS)
    if vname_el is None:
        continue
    vname = vname_el.text
    cfvs = set(el.text for el in vs.findall('{%s}controllingFieldValue' % NS))
    existing_vs[vname] = cfvs

# ── Update Category_dsco__c ─────────────────────────────────────────────────
new_cats = sorted(sheet_categories - existing_cats)
print("Adding %d new categories: %s" % (len(new_cats), new_cats))

for cat_name in new_cats:
    v_el = ET.SubElement(cat_vsd, '{%s}value' % NS)
    fn_el = ET.SubElement(v_el, '{%s}fullName' % NS)
    fn_el.text = cat_name
    df_el = ET.SubElement(v_el, '{%s}default' % NS)
    df_el.text = 'false'
    lb_el = ET.SubElement(v_el, '{%s}label' % NS)
    lb_el.text = cat_name

# ── Update Sub_Category_dsco__c ─────────────────────────────────────────────
# 1. Add new value entries
new_subcats = sorted(
    s for s in sheet_mapping if s not in existing_subcats and s not in SKIP_AS_NEW_VALUE
)
print("Adding %d new sub-category values" % len(new_subcats))

for sub_name in new_subcats:
    v_el = ET.SubElement(sub_vsd, '{%s}value' % NS)
    fn_el = ET.SubElement(v_el, '{%s}fullName' % NS)
    fn_el.text = sub_name
    df_el = ET.SubElement(v_el, '{%s}default' % NS)
    df_el.text = 'false'
    lb_el = ET.SubElement(v_el, '{%s}label' % NS)
    lb_el.text = sub_name

# 2. Add / update valueSettings
# Build a dict of vs elements by valueName for efficient lookup
vs_elements = {}
for vs in sub_vs_parent.findall('{%s}valueSettings' % NS):
    vname_el = vs.find('{%s}valueName' % NS)
    if vname_el is not None:
        vs_elements[vname_el.text] = vs

added_vs = 0
updated_vs = 0

for subcat, cats in sorted(sheet_mapping.items()):
    if subcat in SKIP_AS_NEW_VALUE:
        continue
    current_cfvs = existing_vs.get(subcat, set())
    missing_cfvs = cats - current_cfvs
    if not missing_cfvs:
        continue

    if subcat in vs_elements:
        # Add missing controllingFieldValues to existing element
        vs_el = vs_elements[subcat]
        vname_el = vs_el.find('{%s}valueName' % NS)
        for cfv in sorted(missing_cfvs):
            new_cfv = ET.Element('{%s}controllingFieldValue' % NS)
            new_cfv.text = cfv
            vs_el.insert(list(vs_el).index(vname_el), new_cfv)
        updated_vs += 1
    else:
        # Create new valueSettings element
        vs_el = ET.SubElement(sub_vs_parent, '{%s}valueSettings' % NS)
        for cfv in sorted(cats):
            cfv_el = ET.SubElement(vs_el, '{%s}controllingFieldValue' % NS)
            cfv_el.text = cfv
        vn_el = ET.SubElement(vs_el, '{%s}valueName' % NS)
        vn_el.text = subcat
        added_vs += 1

print("Updated %d existing valueSettings, added %d new valueSettings" % (updated_vs, added_vs))

# ── Pretty-print helper ─────────────────────────────────────────────────────
def indent(elem, level=0):
    pad = '\n' + '    ' * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + '    '
        if not elem.tail or not elem.tail.strip():
            elem.tail = pad
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = pad
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = pad
    if not level:
        elem.tail = '\n'

indent(cat_root)
indent(sub_root)

# ── Write output ─────────────────────────────────────────────────────────────
cat_tree.write(cat_path, encoding='UTF-8', xml_declaration=True)
sub_tree.write(sub_path, encoding='UTF-8', xml_declaration=True)
print("Done. Files written.")
