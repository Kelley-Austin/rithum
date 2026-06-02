---
generator: cheese:personas
generatedAt: 2026-06-02T14:52:43.520Z
generatorVersion: 1
sources:
  - .sf-cache/inventory.md
---

# Personas

## Tier 1 Service Agent
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Service Cloud (Service Console)
- **Data visibility:** Queue-owned cases visible to all queue members; own-assigned cases visible by role hierarchy
- **Daily tasks:** Monitor brand-specific case queues for new inbound cases; accept and work cases from queue; apply case sub-category to trigger correct routing; escalate to Tier 2 when sub-category or internal flag requires it
- **Pain points:** Cases arriving in the wrong queue; no clear signal when a case should escalate; priority accounts indistinguishable from standard accounts in the queue
- **Slices that serve this persona:**
  - ST-21832: Case Queues (Part 1)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21905: Priority Attention Account (Part 4)

## Tier 2 Support Agent
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Service Cloud (Service Console)
- **Data visibility:** All cases routed to Tier 2 queue; role hierarchy visibility over Tier 1 cases for context
- **Daily tasks:** Work escalated cases routed by sub-category rules; handle internally-flagged cases from Tier 1; manage higher-complexity or brand-escalated issues; maintain SLA on priority-account cases
- **Pain points:** Receiving cases without sufficient context for the escalation reason; mixed routing causing irrelevant cases to land in Tier 2; no historical field data to understand account background pre-migration
- **Slices that serve this persona:**
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21904: Internal Route to Tier 2 (Part 2)
  - ST-21905: Priority Attention Account (Part 4)
  - ST-22674: Field Creation (ST-21903)

## Service Operations Supervisor
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Service Cloud (Service Console, Omni-Channel Supervisor)
- **Data visibility:** All cases across all queues and agents via role hierarchy or "View All" on Case
- **Daily tasks:** Monitor queue depth and Omni-Channel routing health across all brand queues; adjust agent capacity and queue priority settings; review routing rule effectiveness; track SLA compliance for priority-attention accounts
- **Pain points:** Urgent cases not surfacing ahead of standard cases; no unified view of brand-segmented queues; inability to identify priority-account backlog at a glance
- **Slices that serve this persona:**
  - ST-21832: Case Queues (Part 1)
  - ST-21905: Priority Attention Account (Part 4)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)

## Internal Support Submitter
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Service Cloud or internal-facing custom app
- **Data visibility:** Cases they created or are related to; limited to their own team's records
- **Daily tasks:** Log internal cases on behalf of a team or department; flag a case for Tier 2 handling via the internal routing mechanism; track status of internally-submitted cases
- **Pain points:** No standardized path to get a case directly to Tier 2 without going through Tier 1 triage; internal cases mingling with customer cases in the same queue
- **Slices that serve this persona:**
  - ST-21904: Internal Route to Tier 2 (Part 2)

## Account Manager / Customer Success Manager
- **Profile:** [needs input]
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Sales Cloud or Service Cloud (account/case cross-reference)
- **Data visibility:** Accounts and cases within their assigned territory or ownership; does not see queue internals
- **Daily tasks:** Identify which accounts carry the Priority Attention flag; coordinate with support on open cases for priority accounts; escalate cases for high-value accounts when SLA is at risk
- **Pain points:** No visible indicator in Salesforce that an account is Priority Attention; support agents treating priority-account cases the same as standard ones; lack of migrated historical case data making account health hard to assess
- **Slices that serve this persona:**
  - ST-21905: Priority Attention Account (Part 4)
  - ST-22674: Field Creation (ST-21903)

## Salesforce Administrator / Configuration Owner
- **Profile:** System Administrator
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Setup, Service Cloud, Deployment tooling
- **Data visibility:** All data (System Administrator profile)
- **Daily tasks:** Create and maintain Case queues per brand; configure Omni-Channel routing rules and priority values; manage case sub-category picklist values and assignment rules; deploy field additions for the data migration
- **Pain points:** Routing priority misconfiguration causing urgent cases to queue behind standard ones; field schema gaps blocking the case data migration; repeated manual queue setup per brand with no templated pattern
- **Slices that serve this persona:**
  - ST-21832: Case Queues (Part 1)
  - ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)
  - ST-21904: Internal Route to Tier 2 (Part 2)
  - ST-22674: Field Creation (ST-21903)

## Data Migration Engineer
- **Profile:** System Administrator or custom migration profile
- **Permission sets:** [needs input]
- **Role hierarchy:** [needs input]
- **Apps used:** Data Loader, MuleSoft, or ETL tooling alongside Service Cloud
- **Data visibility:** All Case records (requires "Modify All" or equivalent for migration load)
- **Daily tasks:** Map source case fields to new Salesforce schema fields; run migration loads into the Case object; validate field-level data integrity post-load; coordinate with admin on any schema blockers
- **Pain points:** Missing target fields on the Case object causing load failures; no agreed field-naming standard creating schema inconsistency; downstream routing rules broken by incorrectly populated picklist values after migration
- **Slices that serve this persona:**
  - ST-22674: Field Creation (ST-21903)
