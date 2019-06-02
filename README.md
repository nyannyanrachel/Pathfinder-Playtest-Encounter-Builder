# Pathfinder Playtest Encounter Creator

## Overview
This is a python based tool for DMs to design encounters for the Pathfinder Playtest Rulset. The goal is to be able to quickly and efficiently design encounters with minimal input from the user.

___

## Plan and Implementation
To achieve this goal, my approach is to use stepwise design in an implementation similar to the "rod-cutting" dynamic programming problem where all costs for each "length" are equal. That is, the minimum viable product goal is to naievely find all possible permutations of creatures that match our parameters.

The algorithm should take several parameters. 
- Party Level
- Party Size
- Encounter Severirty
- (Optional) The maximum number of creatures for the encounter.
- (Optional) The minimum number of creatures for the encounter.
- (Optional) An XP Budget

### The Algorithm
The algorithm itself will try to attain a combination of creatures that is equal to or under the cost of the encounter severity OR an XP budget if provided. 
To do this it will use top-down greedy programming by first choosing the largest XP cost creature that fits the budget. Once found it will store that local solution into a database and then recurse finding the next highest costing creature that fits. When a creature is found and there is still a remaning budget left, it will then use that new remaining budget and recurse down again choosing the local maximum until the base case where the remaining budget is 0.

### Stretch Goals

 - __Themed Encounters__: I want the application to be able to design encounters based on themes such as "Undead" or "Jungle" or some arbitrary theme. On a napkin, I imagine this being implemented by creatures being associated with something like traits, attributes, or creature types. This allows most of the filtering to be done in the data wrangling portion of the application so that the algorithm doesn't need much changing.
 
 - __DM "Encounter Cheat Sheet"__: This originally started as a small project to make it easier for me as a DM to make an encounter on the fly. As most of we DMs know, all the planning in the world doesn't mean you're fully prepared and I wanted an quick and easy tool to create encounters in the events where it would narritively make sense when I didn't have something prepared. To that end, I'd like the application to be able to make a "cheat sheet". Essentially a quick reference sheet that I can use to reference their monster cards and maybe as an extra feature even further into the future, the ability to track their health.

___

## Project Notes

While attempting to develop the algorithm I had initially intended to design, I ran into a lot of issues where I felt like the approach didn't match what I was trying to achieve. Specifically, I modeled the problem on paper like a rod-cutting algorithm. I imagined the length of the rod that I needed to cut being the xp budget for the given encounter. Early on however I realized that the rod-cutting problem is fundamentally different than what I was trying to achieve. 

The rod-cutting algorithm's goal is to maximize how much "money" you can sell the rod for if you were to sell smaller parts of it individually. That is, the rod can be cut up into different sizes and each one of those sizes is worth a certain amount of money. The goal of the algorithm is to compare the combinations of different sized cuts to come out with a series of cuts that maximizes the money earned.

The is fundamentally different to what I am trying to acheive in two ways. The first is that by building an encounter, I am not trying to maximize anything. While the rod-cutting algorithm seeks to find a "best" solution, I am trying to find "all" or multiple solutions. The second is that the rod-cutting algorithm seeks to use as much of the "rod" as possible. The encounter designer is similar however it should allow for some leeway into allowing encounters that do not meet the full budget but meet the maximum number of creatures desired.

To that note, instead of immediately looking into optimal solutions, I created a naive approach algorithm that seeks to produce what I want. The way the naive algorithm works is that it loops through all mosnters in the bestiary. For every monster, it attempts to build an encounter by first putting that monster into an encounter if it is within the xp budget and calculates the remaining budget. From there it will then loop through the monster list again to put the next monster that it comes across that is within budget into the encoutner and recalculates the remaining budget. It will do this until it either does not find a monster, or the remaning budget is 0. In that case it will "publish" the encounter to a _global_ list of _possible_ encounters and delete the last monster that made no other combinations possible from the current encounter. It will then continue onto the next monster that meets requirements and repeats ad nauseum. 

This approach is significantly inefficient since the effiency is in an O(n<sup>c</sup>) class. In this case the n is the bestiary size and the c refers to the maximum amount of monsters you want in the encounter.

---
### Improvements

For my next version, I want to try figure out what ways I can make the algorithm more efficient. Specifically, the things I want to look at are limiting the search space by doing things such as:

- Stopping after finding X amount of solutions.
- In addition to that trying random combinations of monsters so that we potentially search for < N amount of monsters. 
- Using filtering for thigns such as traits, monster type, locations, etc to narrow down the size of N.
- Implementing arbitrary rules such as "First monster must meet at least 50% of total cost."
- Using a stop condition in cases where no matches were found after looping through the whole list of possible monsters. 
- Changing the base case so that if the amount of experience left is < the lowest possible xp value the algorithm stops.

For a more complex way to increase efficiency, I want to look at way the algorithm could be multi-threaded so that two different possibilities of encouners can be built at the same time. Or, while one monster is being found, another thread could be finding the next monster with an estimated remaining budget. Due to the way multithreading works in python however, I believe there wwould be some potential difficulty in maintaining data integrity and ensuring there are no race conditions.
