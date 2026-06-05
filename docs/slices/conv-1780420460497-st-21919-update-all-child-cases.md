---
generator: cheese:slice-summary
generatedAt: 2026-06-02T18:39:28.058Z
generatorVersion: 1
sources:
  - "SF story ST-21919"
---

# ST-21919: Update all Child Cases

## What was done
- Created Screen Flow `Brands_Case_Update_Child_Cases` (`flows/Brands_Case_Update_Child_Cases.flow-meta.xml`) that agents launch from a quick action button on a Case record.
- Flow screen exposes three inputs: free-text "Send Comment to Child Cases" (`txtComment`), "Comment is Public" checkbox (`chkIsPublic`), and "Update Child Case Statuses" picklist (`pickNewStatus`) driven by the live `Case.Status` picklist.
- When a comment is provided, the flow posts a Chatter `FeedItem` to the parent case, loops through all child cases (`ParentId = recordId`), builds a collection of `FeedItem` records, then inserts them in a single bulk DML call (`Create_Child_Chatter_Posts`).
- Comment visibility (`AllUsers` vs `InternalUsers`) is set on both the parent and all child posts based on the `chkIsPublic` checkbox.
- When a status is selected, the flow uses a filter-based `recordUpdate` on all cases where `ParentId = recordId`, updating `Status` in one DML operation.
- Created Quick Action `Case.Update_Child_Cases` (`quickActions/Case.Update_Child_Cases.quickAction-meta.xml`) of type `Flow` pointing to the new flow; added the action to the `Case-Production Support Layout`.

## What's pending
- `manifest/package.xml` does not yet include `Brands_Case_Update_Child_Cases` (Flow) or `Case.Update_Child_Cases` (QuickAction) — these need to be added before any manifest-driven deployment.
- No validation guard if an agent clicks Save without entering a comment or selecting a status; the flow silently no-ops. Confirm with product whether an error/warning is expected in that case.

## Key decisions
- **Chatter posts to child cases are batched into a single collection insert, not one create per loop iteration** — *Why:* Avoids per-record DML calls that would hit governor limits on cases with many children.
- **Status update uses a filter-based `recordUpdate` rather than a per-record loop** — *Why:* Single DML operation regardless of child-case count; simpler and governor-safe.
- **Visibility for child posts mirrors the parent post via a shared `varFeedVisibility` variable** — *Why:* Consistency — agents set public/internal once and it applies to all posts uniformly.
- **Comment path and status path are fully independent branches** — *Why:* Agents can post a comment only, update statuses only, or do both in the same action without coupling the two operations.

## Files changed
- `force-app/main/default/flows/Brands_Case_Update_Child_Cases.flow-meta.xml` — new Screen Flow implementing the full child-case update logic
- `force-app/main/default/quickActions/Case.Update_Child_Cases.quickAction-meta.xml` — new Quick Action wiring the button to the flow
- `force-app/main/default/layouts/Case-Production Support Layout.layout-meta.xml` — added the `Update Child Cases` quick action button to the Production Support Case layout
- `manifest/package.xml` — modified (note: Flow and QuickAction entries for this ticket appear to be missing; see pending items)

## Lessons
- Batch child record Chatter posts via a collection variable + single `recordCreate` rather than calling `Create Records` inside the loop — this is the pattern to reach for any time you're posting to an unbounded child collection.
- Filter-based `recordUpdate` (set field on all records matching a `WHERE` clause) outperforms loop-then-update for bulk child status changes; prefer it whenever the same value is written to all matched records.

## Persona impact
This slice serves: Case Agent (Tier 1 / Tier 2 support rep). Value: Agents can broadcast a comment and/or bulk-update the status of all child cases in one action instead of opening each child case individually.
```
