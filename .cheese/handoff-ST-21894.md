# Handoff: ST-21894 Queue Assignment

**Branch:** developer/claresegrue-prft  
**Last commit:** 31600ea "wip: save before branch switch"  
**Org used:** rithum-uat

## What was built

Five Salesforce Case Queue metadata files were created under `force-app/main/default/queues/`:

| File | Queue Label | Role (DeveloperName) |
|---|---|---|
| `Brands_Tier_1.queue-meta.xml` | Brands Tier 1 | `Brands_Tier_1` |
| `Brands_Tier_1_Urgent.queue-meta.xml` | Brands Tier 1 Urgent | `Brands_Tier_1` |
| `Brands_Tier_2.queue-meta.xml` | Brands Tier 2 | `Brands_Tier_2` |
| `Brands_Tier_2_Urgent.queue-meta.xml` | Brands Tier 2 Urgent | `Brands_Tier_2` |
| `Brands_Administration.queue-meta.xml` | Brands Administration | `Brands_Administration` |

`manifest/package.xml` was updated to include a `Queue` types block with all 5 members. API version bumped to 62.0.

## ⚠️ Known risk before deploying

The three Brands **roles** (`Brands_Tier_1`, `Brands_Tier_2`, `Brands_Administration`) do **not exist** in `rithum-uat`. They were queried and returned zero results. The queue files reference them by expected DeveloperName.

Before the PR deploy to production succeeds, confirm:
1. The roles exist in production (or will be deployed first by a related story).
2. Their `DeveloperName` values exactly match: `Brands_Tier_1`, `Brands_Tier_2`, `Brands_Administration`.

To check production: `sf data query --query "SELECT Name, DeveloperName FROM UserRole WHERE Name LIKE 'Brands%'" --target-org ka-production`

## Next step

Open a PR from `developer/claresegrue-prft` → `main`. GitHub Actions handles the production deploy.
