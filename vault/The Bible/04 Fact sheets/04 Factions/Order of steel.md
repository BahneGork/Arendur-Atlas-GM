---
face: 
leader: 
political_stance: 
neutral_towards: 
competing_with: 
infiltrated_by: 
trading_partners: []
patrons: []
vassals: []
rivals:
  - Knight order of the black lilly
enemies: []
allies: []
Reputation: "0"
area of operation:
  - borderlands of ursia
Symbol: 3 silver swords coming together at the points
Activ:
  - Cult of Oztt
Active_Intrigue:
  - Ghostlord
factionFilter: Order of steel
tags: [faction, Arendur]
---


# Order of Steel


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
            .replace(/[\[\]]/g, '') // Remove wiki-link brackets
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
            }
        }
    }
    
    // Note: This is a simplified version of the grouping logic
    // For brevity, including just the essential parts
    
    // Create basic faction network
    let factionsToIncludeDynamic = new Set();
    
    if (actualFilterFaction) {
        factionsToIncludeDynamic.add(actualFilterFaction);
        
        // Add related factions
        for (let relType of config.active) {
            const relArray = relationships[actualFilterFaction][relType] || [];
            for (let target of relArray) {
                factionsToIncludeDynamic.add(target);
            }
        }
    } else {
        for (let faction in relationships) {
            factionsToIncludeDynamic.add(faction);
        }
    }
    
    // Create nodes
    let nodeIndex = 0;
    let nodeMap = {};
    
    for (let faction of factionsToIncludeDynamic) {
        let nodeId = `F${nodeIndex}`;
        let cleanName = sanitizeText(faction);
        nodeMap[faction] = nodeId;
        
        if (faction === actualFilterFaction) {
            mermaidCode += `${nodeId}[\"${cleanName}\"]:::focus-faction\n`;
        } else if (relationships[faction]) {
            mermaidCode += `${nodeId}[\"${cleanName}\"]:::internal-link\n`;
        } else {
            mermaidCode += `${nodeId}[\"${cleanName}\"]:::mentioned-link\n`;
        }
        
        nodeIndex++;
    }
    
    // Add relationships
    for (let faction in relationships) {
        if (!factionsToIncludeDynamic.has(faction)) continue;
        
        let sourceNode = nodeMap[faction];
        
        for (let relType of config.active) {
            const relArray = relationships[faction][relType] || [];
            const displayConfig = config.display[relType] || { icon: '❓', style: 'solid' };
            
            for (let target of relArray) {
                if (nodeMap[target]) {
                    const icon = displayConfig.icon || "❓";
                    mermaidCode += `${sourceNode} -->|${icon} ${relType}| ${nodeMap[target]}\n`;
                }
            }
        }
    }
    
    // Add styling
    mermaidCode += "classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:2px;\n";
    mermaidCode += "classDef mentioned-link fill:#FFE6E6,stroke:#FF6B6B,stroke-width:1px,stroke-dasharray: 5 5;\n";
    mermaidCode += "classDef focus-faction fill:#90EE90,stroke:#228B22,stroke-width:3px;\n";
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
    
    const configType = window.factionDataUnified.usingDynamicConfig ? "Dynamic" : "Static";
    if (filterValueDynamic.trim()) {
        if (resultFilter.filterMatched) {
            dv.paragraph(`🎯 **Grouped View** (${configType}): Showing relationships for \"${resultFilter.filterMatched}\" (${resultFilter.factionCount} factions)`);
        } else {
            dv.paragraph(`⚠️ **Filter Not Found**: \"${filterValueDynamic}\" not found - showing all factions instead (${resultFilter.factionCount} total)`);
        }
    } else {
        dv.paragraph(`🌐 **Full Grouped Network** (${configType}): Showing all factions (${resultFilter.factionCount} total)`);
    }
    
    dv.paragraph(resultFilter.code);
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```

Faction description goes here...



#faction #Arendur