# INSIGHTS.md - Three Data-Driven Insights from LILA BLACK

Derived from 796 matches across 5 days of production gameplay data (Feb 10-14, 2026).

---

## INSIGHT 01: Traffic Is Highly Skewed Toward a Single Mid-Map Band

### What Caught My Eye

When I aggregated all Position and BotPosition events and binned them into a 4x4 grid per map, one mid-map sector consistently dominated traffic.

### The Evidence

Across all maps combined (73,059 position samples):

- **Hottest sector share:** 18.8% of all traffic (13,739 samples)
- **Coldest sector share:** 0.09% of traffic (63 samples)
- **Traffic disparity:** **218x** more movement in the hottest sector than the coldest
- **Corner sectors combined:** 7.0% of total traffic

### Actionable Items

1. **Add pull incentives** to underused corners (high-tier loot, unique objective, extraction bonus).
2. **Route the storm path** to occasionally end near a low-traffic corner to force rotations.

**Metrics to track:**
- Dead Zone Engagement Rate (player-seconds per sector)
- Player Distribution Entropy (how evenly traffic spreads)

### Why a Level Designer Should Care

Large parts of the map are underutilized. This is a signal that the risk/reward layout is not pulling players into those areas.

---

## INSIGHT 02: Combat Is Almost Entirely Human-vs-Bot

### What Caught My Eye

Kill events are overwhelmingly dominated by BotKill events (human kills bot), while true human-vs-human kills are almost absent.

### The Evidence

Combat events across all data:

| Event Type | Count | Share of Kills |
|---|---:|---:|
| Kill (human killed human) | 3 | 0.1% |
| BotKill (human killed bot) | 2,415 | 99.9% |

Human-vs-human kills are effectively **non-existent** in this dataset.

### Actionable Items

1. **Increase PvP encounter probability** by relocating high-value loot into mid-traffic collision zones.
2. **Adjust bot density** so bots do not dilute human encounters.
3. **Add contested objectives** that require multiple teams to rotate into the same space.

**Metrics to track:**
- PvP Kill Rate (human kills human / total kills)
- Encounter Density (human-vs-human proximity events)

### Why a Level Designer Should Care

If PvP fights are rare, map geometry isn’t being stress-tested for player-versus-player pressure. Chokepoints, sight lines, and cover balance remain unvalidated.

---

## INSIGHT 03: Storm Deaths Are a Small Minority of Total Deaths

### What Caught My Eye

Storm deaths occur, but they are not a dominant elimination source.

### The Evidence

- Total deaths (Killed + BotKilled + KilledByStorm): **742**
- Storm deaths (KilledByStorm): **39**
- **Storm death rate:** **5.3%**

### Actionable Items

1. **Increase storm lethality** or tighten storm speed to make it a more meaningful threat.
2. **Add storm-avoidance incentives** (late-game rewards, extraction bonuses) to shape player movement.

**Metrics to track:**
- Storm Death Rate (storm deaths / total deaths)
- Late Game Survival Rate

### Why a Level Designer Should Care

If the storm is not a strong eliminator, it might not be shaping player flow as intended. This impacts pacing and late-game rotations.

---

## Summary Table

| Insight | Area | Primary Metric | Priority |
|---|---|---|---|
| Traffic skew (218x disparity) | Map Layout | Dead Zone Engagement Rate | High |
| PvP scarcity (99.9% bot kills) | Encounter Design | PvP Kill Rate | High |
| Storm deaths low (5.3%) | Game Systems | Storm Death Rate | Medium |
