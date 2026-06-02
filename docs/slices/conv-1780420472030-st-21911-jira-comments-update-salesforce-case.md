---
generator: cheese:slice-summary
generatedAt: 2026-06-02T17:36:32.328Z
generatorVersion: 1
sources:
  - "SF story ST-21911"
---

# ST-21911: Jira Comments Update Salesforce Case

## What was done
- Created `JiraCommentController.cls` — a `@RestResource` REST endpoint at `/jira/comment` that accepts POST payloads from Jira containing `caseId`, `jiraIssueKey`, `commentBody`, `authorName`, and `commentTimestamp`.
- Endpoint looks up the target `Case` by `Id` (if `caseId` provided) or by `Jira_Number__c` (if only `jiraIssueKey` provided), respects the `Block_Jira_Updates__c` field ("Yes" silently skips processing), creates an internal `CaseComment` (unpublished), and stamps `Last_Jira_Comment_Date_Time__c` on the Case.
- Created `JiraCommentControllerTest.cls` with 7 test methods covering: success by `caseId`, success by `jiraIssueKey`, blocked case, case not found (404), missing identifier (400), and two `buildCommentBody` unit tests.
- Created `Brands_Case_Jira_Comment_Received` auto-launched record-triggered Flow (after-save on `Case`) that fires when `Last_Jira_Comment_Date_Time__c` changes and posts a Chatter message to the Case feed alerting the owner and followers.
- Updated `manifest/package.xml` to include `JiraCommentController`, `JiraCommentControllerTest`, and `Brands_Case_Jira_Comment_Received`.

## What's pending
- Jira-side webhook/integration confirmation: the story description notes "checking with Cole to see if they have a field that is updated in Jira whenever a new Comment is added" — the trigger mechanism from Jira is not yet confirmed.
- Authentication setup (Named Credential / Connected App) for the `/jira/comment` REST endpoint has not been addressed in this slice.
- The story described "Case status update" on new Jira comment, but the current implementation only posts a Chatter notification — no `Status` field change was implemented. Confirm with stakeholders whether a status transition is still required.

## Key decisions
- **Dual-identifier lookup (caseId OR Jira_Number__c)** — *Why:* Jira may not always have the Salesforce Case ID; fallback to `Jira_Number__c` prevents hard dependency on Salesforce IDs in Jira.
- **CaseComment created as unpublished (IsPublished = false)** — *Why:* Keeps Jira-sourced content internal by default; agents decide when/if to publish to the customer.
- **DateTime stamp (Last_Jira_Comment_Date_Time__c) decouples REST endpoint from Chatter notification** — *Why:* Flow listens for the field change rather than the endpoint posting to Chatter directly, keeping concerns separated and the endpoint testable in isolation.
- **Block_Jira_Updates__c flag per Case** — *Why:* Allows individual cases to opt out of Jira-driven updates without disabling the integration globally.

## Files changed
- `force-app/main/default/classes/JiraCommentController.cls` — core REST endpoint logic
- `force-app/main/default/classes/JiraCommentController.cls-meta.xml` — class metadata
- `force-app/main/default/classes/JiraCommentControllerTest.cls` — full test coverage (7 methods)
- `force-app/main/default/classes/JiraCommentControllerTest.cls-meta.xml` — test class metadata
- `force-app/main/default/flows/Brands_Case_Jira_Comment_Received.flow-meta.xml` — Chatter notification flow triggered by `Last_Jira_Comment_Date_Time__c` change
- `manifest/package.xml` — updated to register the two new Apex classes and the new Flow

## Lessons
- Using a DateTime stamp field (`Last_Jira_Comment_Date_Time__c`) as the flow trigger is more reliable than firing from a platform event or invoking Chatter from within the REST endpoint — it survives async boundaries and is easy to re-trigger manually in testing.
- The `Block_Jira_Updates__c` pattern (per-record opt-out returning HTTP 200 "blocked" rather than an error) is worth reusing in other Jira integration endpoints on this project to give admins granular control without breaking the integration contract.

## Persona impact
This slice serves: Support Agent / Case Manager. Value: Jira engineering comments now surface automatically inside Salesforce Cases as internal CaseComments with a Chatter notification, eliminating the need for agents to context-switch into Jira to track engineering updates.
