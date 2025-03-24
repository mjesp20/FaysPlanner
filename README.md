# FaysPlanner

Requires https://github.com/mjesp20/FaysPlannerAddon for outputting character names and classes from a WoW raid. Currently only optimized for Turtle WoW 1.12 client, but should work on other 1.12 private servers aswell

Each class is assigned a default role on import. To change this, simply click the correct role for the character.

The planner follows the following logic:

1. Assign 1 melee pr group
2. Assign 1 melee pr group
3. Assign 1 healer pr group
4. Assign remaining healers into random groups
5. Assign ranged dps to groups
6. Assign remaining melee (Considered "sitting out")

This means the melee in the first two rows are dps'ing, while melee in rows 3, 4 and 5 should be standing near the wall to avoid further chaining