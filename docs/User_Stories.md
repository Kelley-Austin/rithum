---
generator: cheese:user-stories
generatedAt: 2026-06-02T17:18:14.685Z
generatorVersion: 1
sources:
  - docs/Personas.md
---

# User Stories

### US-001 — Brand Cases Assigned to Correct Queue on Creation
- **As a** Tier 1 Support Agent
- **I want** incoming cases to be automatically assigned to the appropriate brand queue when they are created
- **So that** I can find and claim cases relevant to my team without manually hunting through unstructured backlogs
- **Acceptance:** Cases created for each brand are placed into the correct queue immediately upon creation with no manual intervention required; agents see only their relevant queue(s) in the Service Console.
- **Personas:** Tier 1 Support Agent
- **Slices:**
  - [ST-21832](docs/slices/ST-21832.md)
- **Status:** not-started

---

### US-002 — Queue Backlog Visibility for Supervisors
- **As a** Case Supervisor / Queue Manager
- **I want** all incoming cases distributed across structured, named queues
- **So that** I can monitor volume at a glance and redistribute work across Tier 1 and Tier 2 without relying on agents to self-report backlog
- **Acceptance:** A supervisor can view case counts per queue in Reports & Dashboards; no cases sit in an unassigned or generic bucket after queue configuration is complete.
- **Personas:** Case Supervisor / Queue Manager, Salesforce Administrator / Developer
- **Slices:**
  - [ST-21832](docs/slices/ST-21832.md)
- **Status:** not-started

---

### US-003 — Internally Created Cases Automatically Routed to Tier 2
- **As a** Tier 1 Support Agent
- **I want** cases created by internal users in a designated context to be routed directly to a Tier 2 queue without requiring me to manually escalate them
- **So that** I do not spend time triaging cases that should never enter my queue
- **Acceptance:** Cases meeting the internal-user creation criteria are assigned to the correct Tier 2 queue on save; Tier 1 agents do not see these cases in their queue views.
- **Personas:** Tier 1 Support Agent, Salesforce Administrator / Developer
- **Slices:**
  - [ST-21904](docs/slices/ST-21904.md)
- **Status:** not-started

---

### US-004 — Tier 2 Queue Receives Internally Escalated Cases with Context
- **As a** Tier 2 Support Agent
- **I want** cases routed from internal creation to arrive in my queue already categorized and labeled with routing context
- **So that** I can begin work immediately without performing manual triage to understand why the case landed with me
- **Acceptance:** Each internally routed case displays a routing reason or origin indicator visible in the Service Console list view; no additional Tier 1 touch is required before the case appears in the Tier 2 queue.
- **Personas:** Tier 2 Support Agent
- **Slices:**
  - [ST-21904](docs/slices/ST-21904.md)
- **Status:** not-started

---

### US-005 — Sub-Category Selection Triggers Automatic Tier 2 Routing
- **As a** Tier 1 Support Agent
- **I want** cases I categorize with specific sub-categories to be automatically routed to Tier 2
- **So that** I do not have to manually escalate eligible cases or remember which sub-categories require escalation
- **Acceptance:** Selecting a qualifying sub-category on a case record triggers reassignment to the correct Tier 2 queue without additional agent action; Tier 1 agents receive a confirmation that the case has been routed.
- **Personas:** Tier 1 Support Agent
- **Slices:**
  - [ST-21900](docs/slices/ST-21900.md)
- **Status:** not-started

---

### US-006 — Supervisor Oversight of Escalation Routing Logic
- **As a** Case Supervisor / Queue Manager
- **I want** sub-category and internal-trigger routing rules to be configurable and reportable
- **So that** I can review routing outcomes, identify misrouted cases, and adjust escalation thresholds without filing a development request
- **Acceptance:** A supervisor can run a report showing cases routed to Tier 2 by routing trigger (sub-category vs. internal creation); routing rule criteria are documented and adjustable by an authorized administrator.
- **Personas:** Case Supervisor / Queue Manager, Salesforce Administrator / Developer
- **Slices:**
  - [ST-21900](docs/slices/ST-21900.md)
  - [ST-21904](docs/slices/ST-21904.md)
- **Status:** not-started

---

### US-007 — Supervisors Flag Accounts as Priority Attention
- **As a** Case Supervisor / Queue Manager
- **I want** to mark strategic or high-risk accounts with a system-level Priority Attention flag
- **So that** agents handling those accounts' cases are alerted to elevated handling requirements without relying on agent memory or informal communication
- **Acceptance:** A supervisor can set and remove the Priority Attention flag on an account record; the flag persists and is visible to all agents who access the account or its related cases.
- **Personas:** Case Supervisor / Queue Manager, Account Team Member
- **Slices:**
  - [ST-21905](docs/slices/ST-21905.md)
- **Status:** not-started

---

### US-008 — Priority Attention Cases Visually Distinguished in Tier 2 Queue
- **As a** Tier 2 Support Agent
- **I want** cases linked to Priority Attention accounts to be visually flagged or separated in my queue view
- **So that** I can apply heightened SLA awareness to those cases without having to cross-reference the account record manually
- **Acceptance:** Priority Attention cases display a distinct indicator (e.g., field value, highlight, or queue segment) in the Tier 2 Service Console list view; standard cases are not affected.
- **Personas:** Tier 2 Support Agent, Case Supervisor / Queue Manager
- **Slices:**
  - [ST-21905](docs/slices/ST-21905.md)
- **Status:** not-started

---

### US-009 — Account Team Notified When a Managed Account Submits a Case
- **As an** Account Team Member (Account Executive / Customer Success)
- **I want** to receive an automated notification when one of my named accounts submits a new case
- **So that** I can proactively engage the customer and stay informed about account health without waiting for support to reach out to me manually
- **Acceptance:** Account team members receive a notification (email or Salesforce notification) when a case is created for an account they own or are a member of; the notification includes the case subject, priority, and a direct link to the case record.
- **Personas:** Account Team Member, Case Supervisor / Queue Manager
- **Slices:**
  - [ST-21906](docs/slices/ST-21906.md)
- **Status:** in-progress

---

### US-010 — Agent Transfers a Case to Another Team Without Losing History
- **As a** Tier 1 Support Agent
- **I want** to transfer a case to a different team using a structured transfer action
- **So that** the receiving team has full case history and I do not have to manually update multiple related child records
- **Acceptance:** Completing the transfer action reassigns the case and all directly related child records to the target team or queue in a single operation; no case history, comments, or attachments are lost during transfer.
- **Personas:** Tier 1 Support Agent
- **Slices:**
  - [ST-21914](docs/slices/ST-21914.md)
- **Status:** not-started

---

### US-011 — Parent Case Updates Propagate to All Child Cases
- **As a** Tier 1 Support Agent
- **I want** edits I make to a parent case to automatically update the relevant fields on all associated child cases
- **So that** I do not have to open and edit each child record individually when a parent case changes
- **Acceptance:** Saving an update to a defined set of fields on a parent case triggers synchronization to all child cases linked to that parent; the sync completes without requiring agent action on individual child records.
- **Personas:** Tier 1 Support Agent
- **Slices:**
  - [ST-21919](docs/slices/ST-21919.md)
- **Status:** not-started

---

### US-012 — Tier 2 Agents Work from Current Child Case Data
- **As a** Tier 2 Support Agent
- **I want** child cases I work to reflect the latest state of their parent case
- **So that** I do not duplicate work already done at the parent level or act on stale information
- **Acceptance:** Child cases display synchronized field values within a defined time window after the parent is updated; agents are not required to manually refresh or re-sync child records.
- **Personas:** Tier 2 Support Agent, Tier 1 Support Agent
- **Slices:**
  - [ST-21919](docs/slices/ST-21919.md)
- **Status:** not-started

---

### US-013 — Jira Comments Automatically Appear on the Linked Salesforce Case
- **As a** Jira-Connected Engineering / Product Stakeholder
- **I want** comments I add to a Jira issue to propagate automatically to the linked Salesforce case record
- **So that** I can share engineering context with support agents without switching tools or duplicating my communication
- **Acceptance:** A comment added to a Jira ticket linked to a Salesforce case appears as a case comment or feed post on the Salesforce record within a defined sync interval; the comment author and timestamp are preserved.
- **Personas:** Jira-Connected Engineering / Product Stakeholder, Salesforce Administrator / Developer
- **Slices:**
  - [ST-21911](docs/slices/ST-21911.md)
- **Status:** not-started

---

### US-014 — Support Agents See Engineering Context Directly on the Case
- **As a** Tier 2 Support Agent
- **I want** Jira comments from engineering to appear on the Salesforce case record without requiring me to access Jira
- **So that** I have the engineering context I need to resolve complex issues and set accurate customer expectations
- **Acceptance:** Jira-originated comments are visible in the case feed or a dedicated section on the case record layout; agents do not need Jira access to read them.
- **Personas:** Tier 2 Support Agent
- **Slices:**
  - [ST-21911](docs/slices/ST-21911.md)
- **Status:** not-started

---

### US-015 — Custom Fields Created to Support the Case Data Model
- **As a** Salesforce Administrator / Developer
- **I want** all required custom fields created on the Case object according to a defined field specification
- **So that** automation, routing, and reporting built in subsequent slices have the data structure they depend on, and no schema drift or data loss occurs during migration
- **Acceptance:** All fields listed in the field specification exist in the target sandbox with the correct data types, labels, and API names; existing case records are not affected by field additions.
- **Personas:** Salesforce Administrator / Developer
- **Slices:**
  - [ST-22674](docs/slices/ST-22674.md)
- **Status:** not-started
