---
generator: cheese:slice-summary
generatedAt: 2026-06-02T16:14:50.253Z
generatorVersion: 1
sources:
  - "SF story ST-21905"
---

# ST-21905: Priority Attention Account (part 4)

Let me check the project docs to write an accurate summary.The flow file doesn't exist locally yet. Let me check the git log on the branch to understand what was actually committed.I have enough context. Here is the summary document:

---

## What was done
- Retrieved `force-app/main/default/flows/Brands_Omni_Channel_Routing.flow-meta.xml` from the sandbox and committed it to source control for the first time on this branch.
- Added a **Get Records** node named `Get_Cases_Account` ("Get Case's Account") to the `Brands_Omni_Channel_Routing` flow; it queries the `Account` object filtering on `Id = inputCase.AccountId` AND `Priority_Support_Attention__c = true`.
- Added a new **Assignment** node named `Priority_Account_Tier_2` that sets `inputCase.OwnerId` to `varT_Tier2` (the Brands Tier 2 queue) when the Account lookup finds a match.
- Wired the new nodes into the flow immediately before the existing `Case_Owner_Assignment` Decision node: a priority-account hit short-circuits to Tier 2 assignment; a miss falls through to normal routing.
- Deployed the updated flow to the sandbox (`rithum-sandbox`) for verification.
- Opened a pull request on branch `agent/st-21905-priority-account-tier2-routing` targeting `main` for production deployment via GitHub Actions.

## What's pending
- End-to-end sandbox test: create a Case for an Account with `Priority_Support_Attention__c = true` and confirm Omni-Channel routes the case to the `Brands Tier 2` queue before the PR merges.
- Confirm the `Priority_Support_Attention__c` checkbox field exists and is populated on relevant Account records in the sandbox before production deploy.

## Key decisions
- **Get Records node filters on `Priority_Support_Attention__c` at query time, not in a Decision node** — *Why:* Single-node check avoids a separate Decision element; null/no-match path is handled by the `noRecordsFoundConnector`.
- **Priority account routing sends to standard Tier 2 (`varT_Tier2`), not Tier 2 Urgent** — *Why:* Priority account status signals elevated service tier, not true urgency; urgent flag is a separate routing signal.
- **Flow retrieved and committed to source control as part of this slice** — *Why:* Prior slice (ST-21900) left the flow org-only; versioning it here makes future diffs auditable in git.
- **New routing check placed before `Case_Owner_Assignment` Decision node** — *Why:* Account-level priority must take precedence over sub-category and internal routing rules that follow.

## Files changed
- `force-app/main/default/flows/Brands_Omni_Channel_Routing.flow-meta.xml` — flow retrieved from sandbox and committed for the first time; contains the new `Get_Cases_Account` Get Records node and `Priority_Account_Tier_2` Assignment node.

## Lessons
- Retrieving the flow as part of the story (not after) is the right sequencing — this slice avoided the git-invisible-change problem that ST-21900 hit by pulling `Brands_Omni_Channel_Routing` into source control before modifying it.
- The `noRecordsFoundConnector` on a Get Records node is the cleanest way to express a conditional branch when the condition is purely "did this record exist?"; it removes the need for a downstream Decision node entirely.
- `Priority_Support_Attention__c` must be pre-populated on Account records before this routing logic fires; stories that depend on a checkbox field should confirm data backfill is in scope before the deploy.

## Persona impact
This slice serves: Tier 1 Service Agent, Tier 2 Support Agent, Service Operations Supervisor, Account Manager / Customer Success Manager. Value: Cases from accounts flagged as Priority Attention are automatically routed to Tier 2 without Tier 1 triage, ensuring strategic accounts receive elevated support handling immediately on case creation.
