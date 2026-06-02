---
generator: cheese:slice-summary
generatedAt: 2026-06-02T14:48:53.649Z
generatorVersion: 1
sources:
  - "SF story ST-21832"
---

# # ST-21832: Case Queues (Part 1)
**Statu

## What was done
- Created 5 Omni-Channel Case queues for the Brands team: `Brands Administration`, `Brands Tier 1`, `Brands Tier 1 Urgent`, `Brands Tier 2`, `Brands Tier 2 Urgent` — all configured with `Case` as the supported object (`force-app/main/default/queues/`)
- Created a paired `QueueRoutingConfig` for each queue using the `MOST_AVAILABLE` routing model with a 180-second push timeout (`force-app/main/default/queueRoutingConfigs/`)
- Assigned routing priorities: Tier 1 Urgent = 10, Tier 2 Urgent = 20, Administration = 30, Tier 1 = 40, Tier 2 = 50 — reflecting urgency-first escalation order
- Updated `manifest/package.xml` to include all 5 `Queue` and 5 `QueueRoutingConfig` members so the metadata is tracked for deployment
- Opened a PR on branch `feature/st-21832-case-queues-part-1-statu` targeting `main`

## What's pending
- Queue membership (agents/users assigned to each queue) is not defined in metadata and must be configured manually in the org or handled in a follow-on slice
- The automation that actually routes new Cases into these queues on creation (Flow or Assignment Rule) is not yet built — this slice only creates the queues themselves
- Omni-Channel presence configurations (Service Channel associations, agent capacity) were not part of this slice and may be needed before queues are live

## Key decisions
- **Urgent queues given lower priority numbers (10, 20) than standard queues (40, 50)** — *Why:* Lower `routingPriority` number = higher Omni-Channel precedence, ensuring urgent cases route first.
- **All queues use `MOST_AVAILABLE` routing model** — *Why:* Distributes work evenly across available agents rather than round-robin or least-active.
- **`doesSendEmailToMembers` set to false on all queues** — *Why:* Prevents email noise on every case assignment; agents use Omni-Channel console instead.
- **Each queue gets its own dedicated `QueueRoutingConfig`** — *Why:* Allows independent tuning of priority and timeout per tier without shared-config coupling.

## Files changed
- `force-app/main/default/queues/Brands_Administration.queue-meta.xml` — new queue, Case object, linked to Administration routing config
- `force-app/main/default/queues/Brands_Tier_1.queue-meta.xml`
- `force-app/main/default/queues/Brands_Tier_1_Urgent.queue-meta.xml`
- `force-app/main/default/queues/Brands_Tier_2.queue-meta.xml`
- `force-app/main/default/queues/Brands_Tier_2_Urgent.queue-meta.xml`
- `force-app/main/default/queueRoutingConfigs/Brands_Administration_Routing.queueRoutingConfig-meta.xml` — priority 30, 180s timeout
- `force-app/main/default/queueRoutingConfigs/Brands_Tier_1_Routing.queueRoutingConfig-meta.xml` — priority 40
- `force-app/main/default/queueRoutingConfigs/Brands_Tier_1_Urgent_Routing.queueRoutingConfig-meta.xml` — priority 10 (highest)
- `force-app/main/default/queueRoutingConfigs/Brands_Tier_2_Routing.queueRoutingConfig-meta.xml` — priority 50
- `force-app/main/default/queueRoutingConfigs/Brands_Tier_2_Urgent_Routing.queueRoutingConfig-meta.xml` — priority 20
- `manifest/package.xml` — added Queue and QueueRoutingConfig member entries for all 10 new files

## Lessons
- Queue metadata alone does not route cases — a Flow or Case Assignment Rule referencing these queues is a required companion deliverable; plan for it explicitly in the story estimate.
- `QueueRoutingConfig` priority is numeric-ascending (1 = highest), not labeled — document the intended tier mapping in a comment or decision log or the ordering will be opaque to the next developer.
- Queue member assignment (users/groups) cannot be tracked in SFDX metadata source format; flag this as a manual post-deploy step in the story acceptance criteria to avoid surprises during UAT.

## Persona impact
This slice serves: Support Agent (Brands). Value: Establishes the Omni-Channel queue structure that will route Brand support cases to the correct tier of agents automatically on creation.
