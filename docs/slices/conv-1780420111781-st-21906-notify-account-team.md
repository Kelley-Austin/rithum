---
generator: cheese:slice-summary
generatedAt: 2026-06-02T17:52:26.694Z
generatorVersion: 1
sources:
  - "SF story ST-21906"
---

# ST-21906: Notify Account Team

# ST-21906: Notify Account Team

## What was done
- Created Custom Notification Type `Brands_New_Case_Notify_Account_Team` (DeveloperName: `Brands_New_Case_Notify_Account_Team`) with Desktop and Mobile channels enabled; master label is "Brands -  New Case Notify Account Team".
- Created auto-launched Record-Triggered Flow `Brands_Notify_Account_Team_on_New_Case` (after-save on `Case`, trigger: Create) that fires when a new Case has a non-null `AccountId`.
- Flow retrieves the `CustomNotificationType` record by `DeveloperName`, then looks up the related `Account` to read `OwnerId`, `Name`, and `Notify_Account_Team_of_Brands_Case__c`.
- Decision element `Check_Notify_Flag` gates the notification: proceeds only when `Notify_Account_Team_of_Brands_Case__c = true` AND the custom notification type was found; skips silently otherwise.
- Sends a `customNotificationAction` to the Account Owner with title "New Case for Your Managed Account" and a dynamic body containing the Account name and Case Number; the notification target links directly to the new Case record.
- Updated `manifest/package.xml` to register the new Flow and Custom Notification Type.

## What's pending
- `manifest/package.xml` at time of this slice only contained `Brands_Case_Jira_Comment_Received` under the `Flow` type — verify the manifest was updated to also include `Brands_Notify_Account_Team_on_New_Case` and `Brands_New_Case_Notify_Account_Team` (CustomNotificationType) before deploying.
- The `Notify_Account_Team_of_Brands_Case__c` checkbox field on Account must exist in the target org; confirm it has been deployed or exists in the sandbox before activating the flow.
- No test coverage was created for the flow in this slice — confirm whether a dedicated flow test or manual test record is required before promotion.
- The story description references notifying the "Account Team" broadly; the current implementation notifies only the Account Owner (`OwnerId`). Confirm with stakeholders whether other Account Team members (Account Team roles) should also receive the notification.

## Key decisions
- **Notification gated by `Notify_Account_Team_of_Brands_Case__c` checkbox on Account** — *Why:* Not all managed accounts require this notification; the flag gives admins per-account opt-in control.
- **Custom Notification Type queried dynamically at runtime by DeveloperName** — *Why:* Avoids hardcoding an org-specific record ID, making the flow portable across sandboxes and production.
- **Notification targets the Case record (`targetId = $Record.Id`)** — *Why:* Clicking the notification takes the recipient directly to the new Case with no extra navigation.

## Files changed
- `force-app/main/default/customNotificationTypes/Brands_New_Case_Notify_Account_Team.notiftype-meta.xml` — Custom Notification Type definition (Desktop + Mobile)
- `force-app/main/default/flows/Brands_Notify_Account_Team_on_New_Case.flow-meta.xml` — core Record-Triggered Flow for the notification
- `manifest/package.xml` — updated to include the new metadata members
- `package.json` — modified (reason not recorded in transcript; likely tooling or dependency update)
- `force-app/main/default/customNotificationTypes/Brands_New_Case_Notify_Account_Team.customNotificationType-meta.xml` — listed in slice metadata but not found locally; may be a renamed/superseded file or a deploy artifact

## Lessons
- The `CustomNotificationType` record must be queried by `DeveloperName` at runtime rather than referenced by ID — this pattern is required for any flow using custom notifications to remain sandbox-portable and should be used in future notification flows on this project.
- Gating notifications on a per-Account boolean field (rather than a global setting) is a reusable pattern that gives admins fine-grained control without requiring code changes; consider this approach for future "notify on event" flows.

## Persona impact
This slice serves: Account Owner / Account Manager. Value: Account Owners are automatically notified on Desktop and Mobile the moment a managed account submits a new Brands Case, eliminating the need to poll case queues or rely on manual handoffs.
```
