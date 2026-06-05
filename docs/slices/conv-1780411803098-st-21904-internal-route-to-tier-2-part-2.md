---
generator: cheese:slice-summary
generatedAt: 2026-06-02T16:06:15.383Z
generatorVersion: 1
sources:
  - "SF story ST-21904"
---

# ST-21904: Internal Route to Tier 2 (Part 2)

## What was done

- Updated the existing `Brands_Omni_Channel_Routing` flow to handle internal-user case routing to Tier 2 Queue
- Added logic to detect when a Case was created by an internal User belonging to a specific group
- Leveraged the `CreatedById` field already present on Case (set up in ST-21832) as the entry point for group membership checks
- Routed qualifying Cases to the Tier 2 Queue via Omni-Channel within the same flow
- Modified `/force-app/main/default/flows/Brands_Omni_Channel_Routing.flow-meta.xml` to incorporate the new routing branch

## What's pending

- Nothing pending.

## Key decisions

- **ST-21832 must complete before ST-21904 runs** — *Why:* The routing flow depends on `CreatedById` being populated by the ST-21832 flow; sequencing is required.
- **Tier 2 routing added to existing flow rather than a new flow** — *Why:* Consolidating routing logic in one flow prevents race conditions and duplicate Omni-Channel assignments.
- **Group membership check uses CreatedById field** — *Why:* Already available from ST-21832; avoids re-deriving user identity inside the routing flow.

## Files changed

- `force-app/main/default/flows/Brands_Omni_Channel_Routing.flow-meta.xml` — Primary flow file; extended with internal-user group detection and Tier 2 Queue routing branch

## Lessons

- ST-21832's `CreatedById` setup is a load-bearing prerequisite; any future routing stories that inspect case origin should confirm ST-21832 is deployed first.
- Extending the existing `Brands_Omni_Channel_Routing` flow keeps all routing decisions in one auditable place — prefer this over creating parallel routing flows for new conditions.

## Persona impact

This slice serves: Internal Service Agent / Tier 1 Support. Value: Cases created internally by specific user groups are automatically escalated to Tier 2 without manual triage.
