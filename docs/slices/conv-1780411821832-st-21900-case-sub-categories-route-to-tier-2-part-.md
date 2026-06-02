---
generator: cheese:slice-summary
generatedAt: 2026-06-02T16:13:17.816Z
generatorVersion: 1
sources:
  - "SF story ST-21900"
---

# ST-21900: Case Sub-Categories Route to Tier 2 (Part 3)

I'll check the project docs to inform the summary before writing it.Now I have enough context. Let me write the summary document.

```markdown
## What was done
- Pulled `Case.Sub_Category_dsco__c` (field `Sub_Category_dsco__c`) field metadata from the sandbox to inspect the dependent picklist that drives Tier 2 routing — confirms the field is a restricted picklist controlled by `Category_dsco__c` with ~150 values across all support categories.
- Identified the target sub-category values that should trigger routing to the `Brands Tier 2` queue (per story ST-21900 requirements).
- Updated the existing **"Brands - Omni Channel Routing"** Record-Triggered Flow: added a branch in the **"Case Owner Assignment"** Decision node that checks `Sub_Category_dsco__c` against the Tier 2 sub-category list and assigns the case owner to the `Brands Tier 2` queue when matched.
- The Flow update was deployed to the sandbox org via the terminal (`sf project deploy start --target-org rithum-sandbox`); the flow file itself is not tracked as local SFDX metadata source in this repo.
- Opened a pull request on branch `agent/st-21900-subcategory-tier2-routing` targeting `main` for review and production deployment via GitHub Actions.

## What's pending
- The "Brands - Omni Channel Routing" Flow is not present in the local repo as SFDX metadata (`force-app/main/default/flows/` does not exist); the flow lives only in the org. A future slice should retrieve and version-control this flow so changes are auditable in git.
- No local commit records the specific sub-category values that were wired to Tier 2 routing — this logic is visible only in the sandbox org's flow. Document or retrieve the flow before production deploy.
- End-to-end testing (creating a Case with a Tier-2-triggering sub-category and confirming Omni-Channel routes it to the `Brands Tier 2` queue) should be verified against the sandbox before the PR merges.

## Key decisions
- **Flow Decision node evaluated on Sub_Category_dsco__c value, not Category** — *Why:* Granular sub-category targeting avoids over-routing entire categories; only specific escalation-worthy sub-types reach Tier 2.
- **Routing target is `Brands Tier 2` queue (not Tier 2 Urgent)** — *Why:* Sub-category-triggered escalations are considered standard escalations; urgent routing reserved for separately-flagged cases.
- **Flow deployed to sandbox only; production goes through GitHub Actions on PR merge** — *Why:* Production org is guarded by the `ka-vault` pre-tool hook; direct deploy is blocked by design.

## Files changed
- `force-app/main/default/objects/Case/fields/Sub_Category_dsco__c.field-meta.xml` — pulled from sandbox to confirm picklist structure; no values were modified; used as reference for flow decision logic.

## Lessons
- The "Brands - Omni Channel Routing" Flow is not version-controlled locally — org-side flow changes made by this slice are invisible to git history. Retrieve and commit flow metadata as part of any slice that modifies it to keep the repo and org in sync.
- Dependent picklist values (Sub_Category controlled by Category) are large and sprawling (~150 values); building the Tier 2 decision against an explicit list of matching values requires care to avoid drift as new sub-categories are added later.
- Empty commits (no file diff) are created when the only artifact is an org-deployed flow with no local metadata counterpart — coordinate with the story author to ensure flow retrieval is part of the acceptance criteria.

## Persona impact
This slice serves: Tier 1 Service Agent, Tier 2 Support Agent, Service Operations Supervisor, Salesforce Administrator / Configuration Owner. Value: Cases stamped with escalation-worthy sub-categories are automatically routed to the Brands Tier 2 queue without manual Tier 1 intervention, reducing misrouting and queue handling time.
```
