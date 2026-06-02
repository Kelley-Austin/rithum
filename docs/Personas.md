---
generator: cheese:personas
generatedAt: 2026-06-02T17:16:51.119Z
generatorVersion: 1
sources:
  - .sf-cache/inventory.md
---

# Personas

## Tier 1 Support Agent
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** Support > Tier 1 Support > [needs input]
- **Apps used:** Service Cloud (Service Console)
- **Data visibility:** Cases assigned to their queue or owned by them; account and contact read access within their territory
- **Daily tasks:**
  - Triage incoming cases from brand queues and assign or claim them
  - Categorize cases by sub-type and route to Tier 2 when criteria are met
  - Transfer cases to other agents or teams
  - Update parent cases, triggering child case sync
- **Pain points:**
  - No standardized queue structure forces agents to hunt for their cases manually
  - Transferring a case requires finding and manually updating multiple related child records
  - No automated routing means Tier 2-eligible cases sit in Tier 1 queues
- **Slices that serve this persona:**
  - ST-21832: Case Queues (Part 1)
  - ST-21914: Transfer Case
  - ST-21919: Update all Child Cases
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21904: Internal Route to Tier 2 (Part 2)

---

## Tier 2 Support Agent
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** Support > Tier 2 Support > [needs input]
- **Apps used:** Service Cloud (Service Console)
- **Data visibility:** Cases routed to Tier 2 queues; visibility into parent/child case chains; Priority Attention accounts flagged for special handling
- **Daily tasks:**
  - Work escalated cases routed from Tier 1 by sub-category or internal trigger
  - Handle Priority Attention account cases with heightened SLA awareness
  - Resolve complex issues and update child records as work progresses
- **Pain points:**
  - Escalated cases arrive without routing context, requiring manual triage
  - Priority account cases are indistinguishable from standard cases in the queue
  - Child case records go stale when parent case is updated, causing duplicate work
- **Slices that serve this persona:**
  - ST-21904: Internal Route to Tier 2 (Part 2)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21905: Priority Attention Account (part 4)
  - ST-21919: Update all Child Cases

---

## Case Supervisor / Queue Manager
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** Support > Support Management > [needs input]
- **Apps used:** Service Cloud, Reports & Dashboards
- **Data visibility:** All cases across queues and agents within their support organization; full account and contact visibility
- **Daily tasks:**
  - Monitor queue volume and redistribute work across Tier 1 and Tier 2
  - Identify and flag Priority Attention accounts for elevated handling
  - Review routing logic outcomes and adjust escalation thresholds
  - Ensure account team stakeholders are notified on relevant case activity
- **Pain points:**
  - No queue structure means backlog is invisible until someone manually checks
  - Priority accounts have no system-level flag, relying on agent memory
  - Notifications to account owners are ad hoc and inconsistently applied
- **Slices that serve this persona:**
  - ST-21832: Case Queues (Part 1)
  - ST-21905: Priority Attention Account (part 4)
  - ST-21906: Notify Account Team
  - ST-21904: Internal Route to Tier 2 (Part 2)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)

---

## Account Team Member (Account Executive / Customer Success)
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** Sales > Account Management > [needs input]
- **Apps used:** Sales Cloud or Service Cloud (read-only case access)
- **Data visibility:** Accounts they own or are members of; cases tied to those accounts via account team membership
- **Daily tasks:**
  - Monitor case activity on their named accounts to stay informed
  - Engage with customers proactively when a case signals account risk
  - Coordinate with support agents on escalated or Priority Attention accounts
- **Pain points:**
  - Case updates on their accounts arrive late or via manual outreach from support
  - No automated notification means account health surprises surface at renewal or QBR
- **Slices that serve this persona:**
  - ST-21906: Notify Account Team
  - ST-21905: Priority Attention Account (part 4)

---

## Jira-Connected Engineering / Product Stakeholder
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Jira (primary); Salesforce Service Cloud (via integration, read-only or limited write)
- **Data visibility:** Cases linked to Jira issues they own or are watching
- **Daily tasks:**
  - Add comments in Jira on bugs or product issues tied to customer cases
  - Expect those comments to propagate to the Salesforce case record automatically
  - Review case context without switching to Salesforce
- **Pain points:**
  - Jira comments do not reach the Salesforce case, so support agents lack engineering context
  - Agents have to manually relay information between systems, introducing lag and errors
- **Slices that serve this persona:**
  - ST-21911: Jira Comments Update Salesforce Case

---

## Salesforce Administrator / Developer
- **Profile:** System Administrator
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input] (typically outside role hierarchy or at apex)
- **Apps used:** Setup, VS Code / CHEESE IDE, Salesforce CLI, Service Cloud
- **Data visibility:** All data across all objects; full metadata access
- **Daily tasks:**
  - Create and deploy custom fields required for new case data model
  - Configure queues, routing rules, assignment rules, and escalation criteria
  - Maintain and extend the Jira integration middleware
  - Validate automation logic against sandbox data before deployment
- **Pain points:**
  - Field creation without a defined migration plan risks data loss or schema drift
  - No standardized queue or routing metadata makes configuration brittle to change
- **Slices that serve this persona:**
  - ST-22674: Field Creation (ST-21903)
  - ST-21832: Case Queues (Part 1)
  - ST-21904: Internal Route to Tier 2 (Part 2)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21911: Jira Comments Update Salesforce Case
