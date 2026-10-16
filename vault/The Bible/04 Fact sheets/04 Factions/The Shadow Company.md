---
factionFilter: The Shadow Company
face:  
leader:  
political_stance:  
neutral_towards: 
allies:
  - The Cautier School
  - Blue Guardians
  - Eyes of the Many Headed Snake
enemies:
  - Red Hand Horde
  - The Charnel House
  - Baron Hexton's Regime
rivals:
  - The Black Lilly Order
vassals: 
patrons:
  - The Lodge
trading_partners:
  - Ravenscrest Emporium
infiltrated_by: 
competing_with: 
neutral_toward:
  - House Omero
  - The Ruby Throne
---

# The Shadow Company

## Overview
The Shadow Company is the player faction in the Arendur Rising campaign - a reformed mercenary company operating from the Fallen Star Inn. Led by the player characters as Senior Officers, they have grown from a small group of adventurers into a recognized organization with political connections and military capabilities.

## Leadership Structure
- **Commander**: Cedric Belmonte (Paladin/Eldritch Knight)
- **Vicar (Resolve)**: Brumor Stålfod (War Cleric)
- **Chancellor Arcane**: Anton Keene (Time Wizard)
- **Castellan**: Frekka Flammehår (Bear Totem Barbarian)
- **Grand Castellan**: Aurilia Alonso (handles day-to-day operations)

## Current Status
- **Headquarters**: Fallen Star Inn Shadow Company HQ
- **Reputation**: 231 (well-regarded as goblin fighters and friends of the homeless)
- **Recent Activities**: Returned from expedition to Dead Mountain and the Far Realm
- **Immediate Concerns**: Charnel House preparing to attack their HQ


## Faction Relationships

```dataviewjs
var allies = dv.current().allies ?? [];
var enemies = dv.current().enemies ?? [];
var rivals = dv.current().rivals ?? [];
var vassals = dv.current().vassals ?? [];
var patrons = dv.current().patrons ?? [];
var trading_partners = dv.current().trading_partners ?? [];
var infiltrated_by = dv.current().infiltrated_by ?? [];
var competing_with = dv.current().competing_with ?? [];
var neutral_toward = dv.current().neutral_toward ?? [];
var current = dv.current().file.name;

dv.paragraph("```mermaid\nflowchart LR\n" +
  
  // Current faction node
  `Current["${current}"]:::current-faction\n` +
  
  // Patrons subgraph
  (patrons.length > 0 ? `subgraph PT ["⬆️ Patrons"]\n${patrons.map((patron, index) => `PT${index + 1}["${patron}"]:::internal-link\n`).join('')}end\nPT --> Current\n` : '') +
  
  // Allies subgraph
  (allies.length > 0 ? `subgraph AL ["🤝 Allies"]\n${allies.map((ally, index) => `AL${index + 1}["${ally}"]:::internal-link\n`).join('')}end\nCurrent --> AL\n` : '') +
  
  // Vassals subgraph
  (vassals.length > 0 ? `subgraph V ["⬇️ Vassals"]\n${vassals.map((vassal, index) => `V${index + 1}["${vassal}"]:::internal-link\n`).join('')}end\nCurrent --> V\n` : '') +
  
  // Trading Partners subgraph
  (trading_partners.length > 0 ? `subgraph TP ["💰 Trading Partners"]\n${trading_partners.map((partner, index) => `TP${index + 1}["${partner}"]:::internal-link\n`).join('')}end\nCurrent <--> TP\n` : '') +
  
  // Enemies subgraph
  (enemies.length > 0 ? `subgraph E ["⚔️ Enemies"]\n${enemies.map((enemy, index) => `E${index + 1}["${enemy}"]:::internal-link\n`).join('')}end\nCurrent -.-> E\n` : '') +
  
  // Rivals subgraph
  (rivals.length > 0 ? `subgraph R ["🥊 Rivals"]\n${rivals.map((rival, index) => `R${index + 1}["${rival}"]:::internal-link\n`).join('')}end\nCurrent <-.-> R\n` : '') +
  
  // Infiltrated By subgraph
  (infiltrated_by.length > 0 ? `subgraph IB ["🕵️ Infiltrated By"]\n${infiltrated_by.map((spy, index) => `IB${index + 1}["${spy}"]:::internal-link\n`).join('')}end\nIB -.-> Current\n` : '') +
  
  // Competing With subgraph
  (competing_with.length > 0 ? `subgraph CW ["🏆 Competing With"]\n${competing_with.map((competitor, index) => `CW${index + 1}["${competitor}"]:::internal-link\n`).join('')}end\nCurrent <-.-> CW\n` : '') +
  
  // Neutral Toward subgraph
  (neutral_toward.length > 0 ? `subgraph N ["😐 Neutral"]\n${neutral_toward.map((neutral, index) => `N${index + 1}["${neutral}"]:::internal-link\n`).join('')}end\nCurrent --- N\n` : '') +
  
  // Styling classes
  `classDef current-faction fill:#4a90e2,stroke:#2171b5,stroke-width:3px,color:#fff;\n` +
  `classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:1px;\n` +
  "```"
);
```

# Dynamic Faction Relationship Map
```dataviewjs
// Meta Bind + DataviewJS Filtered Faction Map with Relationship Grouping
dv.header(2, "📊 Faction Network (Grouped by Relationship)");

// Read the filter value from Meta Bind input
const filterValueDynamic = dv.current().factionFilter || "";

// Enhanced network diagram generator with relationship grouping
function generateGroupedNetworkDiagramDynamic(relationships, filterFaction = null) {
    let mermaidCode = "```mermaid\nflowchart LR\n";
    
    // Get configuration
    const config = window.relationshipConfigDynamic || {
        active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners'],
        display: {
            allies: { icon: "🤝", color: "green", style: "solid", bidirectional: true },
            enemies: { icon: "⚔️", color: "red", style: "dotted", bidirectional: false },
            rivals: { icon: "🥊", color: "purple", style: "dotted", bidirectional: true },
            patrons: { icon: "⬆️", color: "blue", style: "thick", bidirectional: false, reverse_arrow: true },
            vassals: { icon: "⬇️", color: "blue", style: "thick", bidirectional: false },
            trading_partners: { icon: "💰", color: "orange", style: "solid", bidirectional: true }
        }
    };
    
    // Function to sanitize text for Mermaid
    function sanitizeText(text) {
        return text
            .replace(/[[\]]/g, '') // Remove wiki-link brackets
            .replace(/[*_~`]/g, '') // Remove markdown formatting
            .replace(/[#]/g, '') // Remove hash symbols
            .replace(/[|]/g, '') // Remove pipes
            .replace(/\n/g, ' ') // Replace newlines with spaces
            .replace(/"/g, '') // Remove quotes entirely
            .replace(/'/g, '') // Remove apostrophes entirely
            .replace(/'/g, '') // Remove smart apostrophes too
            .replace(/&/g, 'and') // Replace ampersands with 'and'
            .replace(/<>/g, '') // Remove angle brackets
            .trim();
    }
    
    // Enhanced fuzzy matching - find faction name if filtering
    let actualFilterFaction = null;
    if (filterFaction && filterFaction.trim()) {
        const trimmedFilter = filterFaction.trim().toLowerCase();
        
        // Try exact match first
        if (relationships[filterFaction.trim()]) {
            actualFilterFaction = filterFaction.trim();
        } else {
            // Enhanced fuzzy matching with multiple strategies
            for (let faction in relationships) {
                const factionLower = faction.toLowerCase();
                
                // Strategy 1: Exact match (case insensitive)
                if (factionLower === trimmedFilter) {
                    actualFilterFaction = faction;
                    break;
                }
                
                // Strategy 2: Handle "The" prefix variations
                const factionWithoutThe = factionLower.replace(/^the /, '');
                const filterWithoutThe = trimmedFilter.replace(/^the /, '');
                if (factionWithoutThe === filterWithoutThe || 
                    factionLower === "the " + trimmedFilter ||
                    factionWithoutThe === trimmedFilter) {
                    actualFilterFaction = faction;
                    break;
                }
                
                // Strategy 3: Substring matching (partial match)
                if (factionLower.includes(trimmedFilter) || trimmedFilter.includes(factionWithoutThe)) {
                    actualFilterFaction = faction;
                    break;
                }
                
                // Strategy 4: Word-based matching
                const filterWords = trimmedFilter.split(/\s+/);
                const factionWords = factionLower.split(/\s+/);
                
                for (let filterWord of filterWords) {
                    if (filterWord.length > 2) {
                        for (let factionWord of factionWords) {
                            if (factionWord.includes(filterWord) || filterWord.includes(factionWord)) {
                                actualFilterFaction = faction;
                                break;
                            }
                        }
                        if (actualFilterFaction) break;
                    }
                }
                if (actualFilterFaction) break;
            }
        }
    }
    
    // Collect factions to include and organize by relationship type
    let factionsToIncludeDynamic = new Set();
    let relationshipGroups = {};
    
    // Initialize relationship groups
    for (let relType of config.active) {
        relationshipGroups[relType] = new Set();
    }
    relationshipGroups['focus'] = new Set(); // Special group for focused faction
    relationshipGroups['mentioned'] = new Set(); // For mentioned but not existing factions
    
    if (actualFilterFaction) {
        // Add the main faction to focus group
        factionsToIncludeDynamic.add(actualFilterFaction);
        relationshipGroups['focus'].add(actualFilterFaction);
        
        // Add all factions this faction has relationships with (organize by type)
        for (let relType of config.active) {
            const relArray = relationships[actualFilterFaction][relType] || [];
            for (let target of relArray) {
                factionsToIncludeDynamic.add(target);
                relationshipGroups[relType].add(target);
            }
        }
        
        // Add all factions that have relationships with this faction
        for (let faction in relationships) {
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                if (relArray.includes(actualFilterFaction)) {
                    factionsToIncludeDynamic.add(faction);
                    // Put reverse relationships in appropriate groups
                    if (relType === 'patrons') {
                        relationshipGroups['vassals'].add(faction);
                    } else if (relType === 'vassals') {
                        relationshipGroups['patrons'].add(faction);
                    } else {
                        relationshipGroups[relType].add(faction);
                    }
                }
            }
        }
    } else {
        // Include all factions if no filter - organize by their primary relationships
        for (let faction in relationships) {
            factionsToIncludeDynamic.add(faction);
            
            // Determine primary relationship type for grouping
            let primaryRelType = null;
            let maxRels = 0;
            
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                if (relArray.length > maxRels) {
                    maxRels = relArray.length;
                    primaryRelType = relType;
                }
            }
            
            if (primaryRelType && maxRels > 0) {
                relationshipGroups[primaryRelType].add(faction);
            } else {
                relationshipGroups['mentioned'].add(faction);
            }
        }
        
        // Add all target factions (even if they don't have their own notes)
        for (let faction in relationships) {
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                for (let target of relArray) {
                    if (!relationships[target]) {
                        factionsToIncludeDynamic.add(target);
                        relationshipGroups['mentioned'].add(target);
                    }
                }
            }
        }
    }
    
    // Create subgraphs for each relationship type
    let nodeIndexFilter = 0;
    let nodeMapFilter = {};
    
    // Helper function to create formatted relationship type name
    function formatRelType(relType) {
        if (relType === 'focus') return 'Focus Faction';
        if (relType === 'mentioned') return 'Mentioned Factions';
        
        const displayInfo = config.display[relType] || { icon: "❓" };
        const formattedType = relType.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        return `${displayInfo.icon} ${formattedType}`;
    }
    
    // Create subgraphs for each relationship type with factions
    for (let relType of ['focus', ...config.active, 'mentioned']) {
        const factionsInGroup = relationshipGroups[relType];
        
        if (factionsInGroup.size > 0) {
            const groupTitle = formatRelType(relType);
            mermaidCode += `subgraph ${relType}_group["${groupTitle}"]\n`;
            
            for (let faction of factionsInGroup) {
                let nodeId = `F${nodeIndexFilter}`;
                let cleanName = sanitizeText(faction);
                nodeMapFilter[faction] = nodeId;
                
                // Apply appropriate styling based on faction type
                if (relType === 'focus') {
                    mermaidCode += `    ${nodeId}["${cleanName}"]:::focus-faction\n`;
                } else if (relationships[faction]) {
                    mermaidCode += `    ${nodeId}["${cleanName}"]:::internal-link\n`;
                } else {
                    mermaidCode += `    ${nodeId}["${cleanName}"]:::mentioned-link\n`;
                }
                
                // Add click event and tooltip
                let tooltipText = faction;
                if (relationships[faction]) {
                    let relCount = 0;
                    for (let rt of config.active) {
                        const relArray = relationships[faction][rt] || [];
                        relCount += relArray.length;
                    }
                    if (relCount > 0) {
                        tooltipText += ` (${relCount} relationships)`;
                    }
                } else {
                    tooltipText += " (mentioned only)";
                }
                
                mermaidCode += `    click ${nodeId} href "obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(faction)}" "${tooltipText}"\n`;
                
                nodeIndexFilter++;
            }
            
            mermaidCode += `end\n`;
        }
    }
    
    // Generate relationship arrows dynamically
    function generateRelationshipArrowFilter(relType, sourceNode, targetNode, displayConfig, isToFocusFaction = false) {
        // If connecting to focus faction, don't show label since subgraph provides context
        const label = isToFocusFaction ? "" : `|${displayConfig.icon || "❓"} ${relType}|`;
        
        switch (displayConfig.style) {
            case "thick":
                if (displayConfig.reverse_arrow) {
                    return `${targetNode} ==>${label} ${sourceNode}\n`;
                } else if (displayConfig.bidirectional) {
                    return `${sourceNode} <==>${label} ${targetNode}\n`;
                } else {
                    return `${sourceNode} ==>${label} ${targetNode}\n`;
                }
            case "dotted":
                if (displayConfig.bidirectional) {
                    return `${sourceNode} <-.->${label} ${targetNode}\n`;
                } else {
                    return `${sourceNode} -.->${label} ${targetNode}\n`;
                }
            case "simple":
                return `${sourceNode} ---${label} ${targetNode}\n`;
            default: // solid
                if (displayConfig.bidirectional) {
                    return `${sourceNode} <-->${label} ${targetNode}\n`;
                } else {
                    return `${sourceNode} -->${label} ${targetNode}\n`;
                }
        }
    }
    
    // Add relationships - only include if both factions are in our set
    for (let faction in relationships) {
        if (!factionsToIncludeDynamic.has(faction)) continue;
        
        let sourceNode = nodeMapFilter[faction];
        
        // Add relationships dynamically based on active config
        for (let relType of config.active) {
            const relArray = relationships[faction][relType] || [];
            const displayConfig = config.display[relType] || { 
                icon: "❓", 
                color: "gray", 
                style: "solid", 
                bidirectional: false 
            };
            
            for (let target of relArray) {
                if (nodeMapFilter[target]) {
                    // Check if this connection involves the focus faction
                    const isToFocusFaction = actualFilterFaction && (faction === actualFilterFaction || target === actualFilterFaction);
                    mermaidCode += generateRelationshipArrowFilter(relType, sourceNode, nodeMapFilter[target], displayConfig, isToFocusFaction);
                }
            }
        }
    }
    
    // Add styling
    mermaidCode += `classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:2px;\n`;
    mermaidCode += `classDef mentioned-link fill:#FFE6E6,stroke:#FF6B6B,stroke-width:1px,stroke-dasharray: 5 5;\n`;
    mermaidCode += `classDef focus-faction fill:#90EE90,stroke:#228B22,stroke-width:3px;\n`;
    mermaidCode += "```";
    
    return {
        code: mermaidCode,
        factionCount: factionsToIncludeDynamic.size,
        filterMatched: actualFilterFaction
    };
}

// Main execution
if (window.factionDataUnified) {
    const relationshipsFilter = window.factionDataUnified.relationships;
    const resultFilter = generateGroupedNetworkDiagramDynamic(relationshipsFilter, filterValueDynamic);
    
    // Display status
    const configType = window.factionDataUnified.usingDynamicConfig ? "Dynamic" : "Static";
    if (filterValueDynamic.trim()) {
        if (resultFilter.filterMatched) {
            dv.paragraph(`🎯 **Grouped View** (${configType}): Showing relationships for "${resultFilter.filterMatched}" (${resultFilter.factionCount} factions)`);
        } else {
            dv.paragraph(`⚠️ **Filter Not Found**: "${filterValueDynamic}" not found - showing all factions instead (${resultFilter.factionCount} total)`);
        }
    } else {
        dv.paragraph(`🌐 **Full Grouped Network** (${configType}): Showing all factions (${resultFilter.factionCount} total)`);
    }
    
    // Display the map
    dv.paragraph(resultFilter.code);
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```