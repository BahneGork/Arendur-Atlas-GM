---
factionFilter: assumi
---

```dataviewjs

// A. Data Collection Functions with case-insensitive matching
function getAllFactions() {
    // Get all pages with faction relationship arrays, excluding the database file
    return dv.pages().where(p => {
        // Check if this is the database file to exclude
        if (p.file.name === "1. Faction database" || 
            p.file.name === "Faction Dashboard" ||
            p.file.path.includes("1. Faction database")) {
            return false;
        }
        
        // Check if it has faction relationship arrays
        return (p.allies !== undefined || 
                p.enemies !== undefined || 
                p.rivals !== undefined || 
                p.vassals !== undefined || 
                p.patrons !== undefined ||
                p.trading_partners !== undefined ||
                p.infiltrated_by !== undefined ||
                p.competing_with !== undefined ||
                p.neutral_toward !== undefined);
    });
}

function extractRelationships(factions) {
    let allRelationships = {};
    
    // Create a comprehensive mapping of possible names to actual names
    let nameMapping = {};
    for (let faction of factions) {
        let actualName = faction.file.name;
        let variations = [
            actualName.toLowerCase(),                    // "the ruby throne"
            actualName.toLowerCase().replace(/^the /, ''), // "ruby throne"
            actualName.toLowerCase().replace(/^a /, ''),   // in case of "a faction"
            actualName.toLowerCase().replace(/^an /, ''),  // in case of "an organization"
            actualName.toLowerCase().replace(/ the$/, ''), // "faction the" → "faction"
            actualName.toLowerCase().replace(/'/g, '').replace(/'/g, ''), // remove apostrophes
            actualName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim() // remove special chars
        ];
        
        // Add all variations to the mapping
        for (let variation of variations) {
            nameMapping[variation] = actualName;
        }
        
        // Also map the exact name
        nameMapping[actualName] = actualName;
    }
    
    // Enhanced normalize function with better matching and safety checks
    function normalizeRelationshipArray(arr) {
        if (!arr) return [];
        
        // Safety check: convert single strings to arrays
        if (typeof arr === 'string') {
            arr = [arr];
        }
        
        // Safety check: ensure it's an array
        if (!Array.isArray(arr)) {
            console.warn('Relationship data is not an array:', arr);
            return [];
        }
        
        return arr.map(relationshipName => {
            // Ensure relationshipName is a string
            if (typeof relationshipName !== 'string') {
                console.warn('Relationship name is not a string:', relationshipName);
                return String(relationshipName);
            }
            
            // Try multiple variations to find a match
            let testNames = [
                relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/^the /, ''),
                relationshipName.toLowerCase().replace(/^a /, ''),
                relationshipName.toLowerCase().replace(/^an /, ''),
                "the " + relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/'/g, '').replace(/'/g, ''),
                relationshipName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim()
            ];
            
            // Try to find a match
            for (let testName of testNames) {
                if (nameMapping[testName]) {
                    return nameMapping[testName];
                }
            }
            
            // If no match found, return original name
            return relationshipName;
        });
    }
    
    for (let faction of factions) {
        let name = faction.file.name;
        
        allRelationships[name] = {
            allies: normalizeRelationshipArray(faction.allies),
            enemies: normalizeRelationshipArray(faction.enemies),
            rivals: normalizeRelationshipArray(faction.rivals),
            vassals: normalizeRelationshipArray(faction.vassals),
            patrons: normalizeRelationshipArray(faction.patrons),
            trading_partners: normalizeRelationshipArray(faction.trading_partners),
            infiltrated_by: normalizeRelationshipArray(faction.infiltrated_by),
            competing_with: normalizeRelationshipArray(faction.competing_with),
            neutral_toward: normalizeRelationshipArray(faction.neutral_toward)
        };
    }
    
    return allRelationships;
}

function buildRelationshipMatrix(relationships) {
    let matrix = {};
    
    // Initialize matrix
    for (let faction in relationships) {
        matrix[faction] = {};
        for (let otherFaction in relationships) {
            if (faction !== otherFaction) {
                matrix[faction][otherFaction] = [];
            }
        }
    }
    
    // Fill matrix with relationships
    for (let faction in relationships) {
        for (let relType in relationships[faction]) {
            for (let target of relationships[faction][relType]) {
                if (matrix[faction] && matrix[faction][target]) {
                    matrix[faction][target].push(relType);
                }
            }
        }
    }
    
    return matrix;
}

function detectConflicts(matrix) {
    let conflicts = [];
    
    for (let factionA in matrix) {
        for (let factionB in matrix[factionA]) {
            let AtoB = matrix[factionA][factionB];
            let BtoA = matrix[factionB] ? matrix[factionB][factionA] : [];
            
            // Check for conflicting relationships
            if (AtoB.includes('allies') && BtoA.includes('enemies')) {
                conflicts.push(`${factionA} considers ${factionB} an ally, but ${factionB} considers ${factionA} an enemy`);
            }
            if (AtoB.includes('enemies') && BtoA.includes('allies')) {
                conflicts.push(`${factionA} considers ${factionB} an enemy, but ${factionB} considers ${factionA} an ally`);
            }
            if (AtoB.includes('patrons') && !BtoA.includes('vassals')) {
                conflicts.push(`${factionA} serves ${factionB} as patron, but ${factionB} doesn't list ${factionA} as vassal`);
            }
            if (AtoB.includes('vassals') && !BtoA.includes('patrons')) {
                conflicts.push(`${factionA} lists ${factionB} as vassal, but ${factionB} doesn't serve ${factionA} as patron`);
            }
        }
    }
    
    return conflicts;
}

// Execute data collection
const factions = getAllFactions();
const relationships = extractRelationships(factions);
const matrix = buildRelationshipMatrix(relationships);
const conflicts = detectConflicts(matrix);

// Display Faction Registry
dv.header(1, "📊 Faction Registry");
dv.paragraph(`**Total Factions Tracked**: ${Object.keys(relationships).length}`);

// Create faction summary table
let factionSummary = [];
for (let faction in relationships) {
    let totalRelationships = 0;
    let relationshipTypes = [];
    
    for (let relType in relationships[faction]) {
        if (relationships[faction][relType].length > 0) {
            totalRelationships += relationships[faction][relType].length;
            relationshipTypes.push(`${relType}: ${relationships[faction][relType].length}`);
        }
    }
    
    factionSummary.push([
        `[[${faction}]]`,
        totalRelationships,
        relationshipTypes.join(", ") || "None"
    ]);
}

// Sort by total relationships (most connected first)
factionSummary.sort((a, b) => b[1] - a[1]);

dv.table(["Faction", "Total Relationships", "Breakdown"], factionSummary);

// Display conflicts
if (conflicts.length > 0) {
    dv.header(2, "⚠️ Relationship Conflicts Detected");
    for (let conflict of conflicts) {
        dv.paragraph(`- ${conflict}`);
    }
} else {
    dv.paragraph("✅ **No relationship conflicts detected**");
}

// Store data for other components
window.factionData = {
    factions: factions,
    relationships: relationships,
    matrix: matrix,
    conflicts: conflicts
}
```


```dataviewjs
// Lightweight relationship summary
if (window.factionData) {
    dv.header(3, "📋 Relationship Overview");
    
    const relationships = window.factionData.relationships;
    const factionCount = Object.keys(relationships).length;
    
    // Quick counts without heavy processing
    let counts = {
        allies: 0,
        enemies: 0,
        rivals: 0,
        patrons: 0,
        vassals: 0,
        trading_partners: 0,
        infiltrated_by: 0,
        competing_with: 0,
        neutral_toward: 0
    };
    
    // Simple count loop - much faster
    for (let faction in relationships) {
        for (let relType in relationships[faction]) {
            counts[relType] += relationships[faction][relType].length;
        }
    }
    
    // Display counts only
    dv.paragraph("**Relationship Type Counts:**");
    dv.list([
        `🤝 **Allies**: ${counts.allies}`,
        `⚔️ **Enemies**: ${counts.enemies}`,
        `🥊 **Rivals**: ${counts.rivals}`,
        `⬆️ **Patrons**: ${counts.patrons}`,
        `⬇️ **Vassals**: ${counts.vassals}`,
        `💰 **Trading Partners**: ${counts.trading_partners}`,
        `🕵️ **Infiltrated By**: ${counts.infiltrated_by}`,
        `🏆 **Competing With**: ${counts.competing_with}`,
        `😐 **Neutral**: ${counts.neutral_toward}`
    ]);
    
    dv.paragraph(`**Total Relationships**: ${Object.values(counts).reduce((a, b) => a + b, 0)}`);
    
} else {
    dv.paragraph("⏳ Loading faction data...");
}
```
# Static Faction Relationship Map
```dataviewjs
// B. Enhanced Visualization Generator with relationship type indicators
function generateNetworkDiagram(relationships) {
    let mermaidCode = "```mermaid\nflowchart LR\n";
    
   // Function to sanitize text for Mermaid (preserve Danish characters)
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
    
    // Collect ALL faction names mentioned in relationships
    let allFactionNames = new Set();
    
    // Add existing factions
    for (let faction in relationships) {
        allFactionNames.add(faction);
    }
    
    // Add all target factions (even if they don't have their own notes)
    for (let faction in relationships) {
        for (let relType in relationships[faction]) {
            for (let target of relationships[faction][relType]) {
                allFactionNames.add(target);
            }
        }
    }
    
    // Create nodes for ALL factions
let nodeIndex = 0;
let nodeMap = {};

for (let faction of allFactionNames) {
    let nodeId = `F${nodeIndex}`;
    let cleanName = sanitizeText(faction);
    nodeMap[faction] = nodeId;
    
    // All factions should be clickable links, but with different styling
    if (relationships[faction]) {
        // Faction has its own note - primary styling
        mermaidCode += `${nodeId}["${cleanName}"]:::internal-link\n`;
    } else {
        // Faction mentioned but no note exists - mentioned styling (also clickable)
        mermaidCode += `${nodeId}["${cleanName}"]:::mentioned-link\n`;
    }
    nodeIndex++;
}
    
    // Add ALL relationships with different styles and colors
    for (let faction in relationships) {
        let sourceNode = nodeMap[faction];
        
        // Allies (solid green arrows)
        for (let ally of relationships[faction].allies) {
            if (nodeMap[ally]) {
                mermaidCode += `${sourceNode} -->|🤝 ally| ${nodeMap[ally]}\n`;
            }
        }
        
        // Enemies (thick red dotted arrows)
        for (let enemy of relationships[faction].enemies) {
            if (nodeMap[enemy]) {
                mermaidCode += `${sourceNode} -.->|⚔️ enemy| ${nodeMap[enemy]}\n`;
            }
        }
        
        // Rivals (purple dotted bidirectional)
        for (let rival of relationships[faction].rivals) {
            if (nodeMap[rival]) {
                mermaidCode += `${sourceNode} <-.->|🥊 rival| ${nodeMap[rival]}\n`;
            }
        }
        
        // Patrons (thick blue arrows pointing TO faction)
        for (let patron of relationships[faction].patrons) {
            if (nodeMap[patron]) {
                mermaidCode += `${nodeMap[patron]} ==>|⬆️ patron| ${sourceNode}\n`;
            }
        }
        
        // Vassals (thick blue arrows pointing FROM faction)
        for (let vassal of relationships[faction].vassals) {
            if (nodeMap[vassal]) {
                mermaidCode += `${sourceNode} ==>|⬇️ vassal| ${nodeMap[vassal]}\n`;
            }
        }
        
        // Trading partners (orange bidirectional solid)
        for (let partner of relationships[faction].trading_partners) {
            if (nodeMap[partner]) {
                mermaidCode += `${sourceNode} <-->|💰 trade| ${nodeMap[partner]}\n`;
            }
        }
        
        // Infiltrated by (red dotted arrow TO faction)
        for (let spy of relationships[faction].infiltrated_by) {
            if (nodeMap[spy]) {
                mermaidCode += `${nodeMap[spy]} -.->|🕵️ spy| ${sourceNode}\n`;
            }
        }
        
        // Competing with (yellow dotted bidirectional)
        for (let competitor of relationships[faction].competing_with) {
            if (nodeMap[competitor]) {
                mermaidCode += `${sourceNode} <-.->|🏆 compete| ${nodeMap[competitor]}\n`;
            }
        }
        
        // Neutral (gray simple line)
        for (let neutral of relationships[faction].neutral_toward) {
            if (nodeMap[neutral]) {
                mermaidCode += `${sourceNode} ---|😐 neutral| ${nodeMap[neutral]}\n`;
            }
        }
    }
    
    // Add styling - both types should be clickable
mermaidCode += `classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:2px;\n`;
mermaidCode += `classDef mentioned-link fill:#FFE6E6,stroke:#FF6B6B,stroke-width:1px,stroke-dasharray: 5 5;\n`;
    mermaidCode += "```";
    
    return mermaidCode;
}

// Generate and display network
if (window.factionData) {
   
    
    // Debug info
    const relationships = window.factionData.relationships;
    let totalConnections = 0;
    for (let faction in relationships) {
        for (let relType in relationships[faction]) {
            totalConnections += relationships[faction][relType].length;
        }
    }
    
    dv.paragraph(`Displaying ${Object.keys(relationships).length} factions with ${totalConnections} total relationships`);
    
       
    const networkDiagram = generateNetworkDiagram(relationships);
    dv.paragraph(networkDiagram);
} else {
    dv.paragraph("⏳ Loading faction data...");
}
```


### Debug: Faction Relationship Checker

```dataviewjs
// Interactive Debug Section - User Input
dv.header(3, "🔍 Debug: Faction Relationship Checker");

// Create input field and button
const container = dv.container;
container.innerHTML = `
<div style="margin: 10px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
    <label for="factionInput" style="display: block; margin-bottom: 5px; font-weight: bold;">Enter Faction Name to Debug:</label>
    <input type="text" id="factionInput" placeholder="e.g., The Ruby Throne" style="width: 300px; padding: 5px; margin-right: 10px; border: 1px solid #ccc; border-radius: 3px;">
    <button id="debugButton" style="padding: 5px 15px; background-color: var(--interactive-accent); color: white; border: none; border-radius: 3px; cursor: pointer;">Debug Faction</button>
    <div id="debugResults" style="margin-top: 15px; padding: 10px; background-color: var(--background-primary); border-radius: 3px; display: none;"></div>
</div>
`;

// Add click handler
const button = container.querySelector('#debugButton');
const input = container.querySelector('#factionInput');
const results = container.querySelector('#debugResults');

button.addEventListener('click', () => {
    const factionName = input.value.trim();
    if (!factionName) {
        results.style.display = 'block';
        results.innerHTML = '<p style="color: orange;">⚠️ Please enter a faction name</p>';
        return;
    }
    
    if (window.factionData) {
        const relationships = window.factionData.relationships;
        
        // Try to find the faction with fuzzy matching
        let foundFaction = null;
        let exactMatch = false;
        
        // First try exact match
        if (relationships[factionName]) {
            foundFaction = factionName;
            exactMatch = true;
        } else {
            // Try case-insensitive and "The" prefix variations
            const searchVariations = [
                factionName.toLowerCase(),
                factionName.toLowerCase().replace(/^the /, ''),
                "the " + factionName.toLowerCase(),
                factionName.toLowerCase().replace(/^a /, ''),
                factionName.toLowerCase().replace(/^an /, '')
            ];
            
            for (let faction in relationships) {
                const factionLower = faction.toLowerCase();
                if (searchVariations.includes(factionLower)) {
                    foundFaction = faction;
                    break;
                }
            }
        }
        
        results.style.display = 'block';
        
        if (foundFaction) {
            const factionData = relationships[foundFaction];
            
            let html = `<h4>✅ Found: ${foundFaction}${exactMatch ? ' (exact match)' : ' (fuzzy match)'}</h4>`;
            
            // Show relationships found
            html += '<p><strong>Relationships found:</strong></p><ul>';
            let hasRelationships = false;
            for (let relType in factionData) {
                if (factionData[relType].length > 0) {
                    hasRelationships = true;
                    html += `<li><strong>${relType}:</strong> ${factionData[relType].join(", ")}</li>`;
                }
            }
            if (!hasRelationships) {
                html += '<li style="color: orange;">No relationships defined</li>';
            }
            html += '</ul>';
            
            // Check if target factions exist
            html += '<p><strong>Checking if target factions exist:</strong></p><ul>';
            let allTargetsExist = true;
            for (let relType in factionData) {
                for (let target of factionData[relType]) {
                    if (relationships[target]) {
                        html += `<li>✅ ${target} exists as faction</li>`;
                    } else {
                        html += `<li>❌ ${target} NOT found as faction</li>`;
                        allTargetsExist = false;
                    }
                }
            }
            if (allTargetsExist && hasRelationships) {
                html += '<li style="color: green;">✅ All target factions exist!</li>';
            }
            html += '</ul>';
            
            results.innerHTML = html;
        } else {
            let html = `<h4>❌ Faction "${factionName}" not found</h4>`;
            html += '<p><strong>Available factions:</strong></p><ul>';
            const sortedFactions = Object.keys(relationships).sort();
            for (let faction of sortedFactions.slice(0, 10)) { // Show first 10 to avoid overwhelming
                html += `<li>${faction}</li>`;
            }
            if (sortedFactions.length > 10) {
                html += `<li><em>... and ${sortedFactions.length - 10} more</em></li>`;
            }
            html += '</ul>';
            
            results.innerHTML = html;
        }
    } else {
        results.style.display = 'block';
        results.innerHTML = '<p style="color: red;">❌ Faction data not loaded. Make sure the dashboard above has processed.</p>';
    }
});

// Allow Enter key to trigger debug
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        button.click();
    }
});

dv.paragraph("Enter any faction name above to check its relationships and verify all target factions exist.");
```


# 🕸️ Interactive Faction Relationship Map

**Filter by Faction:** `INPUT[text:factionFilter]` `BUTTON[refreshB]`
```meta-bind-button
label: refresh
icon: ""
hidden: true
class: ""
tooltip: ""
id: refreshB
style: primary
actions:
  - type: command
    command: dataview:dataview-rebuild-current-view
```
**Clear Filter:** `BUTTON[clear-filter]`

> 💡 **How to use:** Enter a faction name above, then refresh the note (Ctrl+R) to see the filtered map. Leave empty to show all factions.

```meta-bind-button
label: Clear Filter
id: clear-filter
style: default
hidden: true
action:
  type: updateMetadata
  bindTarget: factionFilter
  evaluate: false
  value: ""

```

```dataviewjs
// Meta Bind + DataviewJS Filtered Faction Map
dv.header(2, "📊 Faction Network");

// Read the filter value from Meta Bind input
const filterValue = dv.current().factionFilter || "";

// Enhanced network diagram generator with filtering (same as before)
function generateFilteredNetworkDiagram(relationships, filterFaction = null) {
    let mermaidCode = "```mermaid\nflowchart LR\n";
    
    // Function to sanitize text for Mermaid (preserve Danish characters)
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
                
                // Strategy 4: Word-based matching (any word in the filter matches any word in faction)
                const filterWords = trimmedFilter.split(/\s+/);
                const factionWords = factionLower.split(/\s+/);
                
                for (let filterWord of filterWords) {
                    if (filterWord.length > 2) { // Only match words longer than 2 characters
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
    
    // Collect factions to include in the map
    let factionsToInclude = new Set();
    
    if (actualFilterFaction) {
        // Add the main faction
        factionsToInclude.add(actualFilterFaction);
        
        // Add all factions this faction has relationships with
        for (let relType in relationships[actualFilterFaction]) {
            for (let target of relationships[actualFilterFaction][relType]) {
                factionsToInclude.add(target);
            }
        }
        
        // Add all factions that have relationships with this faction
        for (let faction in relationships) {
            for (let relType in relationships[faction]) {
                if (relationships[faction][relType].includes(actualFilterFaction)) {
                    factionsToInclude.add(faction);
                }
            }
        }
    } else {
        // Include all factions if no filter
        for (let faction in relationships) {
            factionsToInclude.add(faction);
        }
        
        // Add all target factions (even if they don't have their own notes)
        for (let faction in relationships) {
            for (let relType in relationships[faction]) {
                for (let target of relationships[faction][relType]) {
                    factionsToInclude.add(target);
                }
            }
        }
    }
    
    // Create nodes for included factions
    let nodeIndex = 0;
    let nodeMap = {};
    
    for (let faction of factionsToInclude) {
        let nodeId = `F${nodeIndex}`;
        let cleanName = sanitizeText(faction);
        nodeMap[faction] = nodeId;
        
        // Special styling for the filtered faction
        if (actualFilterFaction && faction === actualFilterFaction) {
            mermaidCode += `${nodeId}["${cleanName}"]:::focus-faction\n`;
        } else if (relationships[faction]) {
            // Faction has its own note - primary styling
            mermaidCode += `${nodeId}["${cleanName}"]:::internal-link\n`;
        } else {
            // Faction mentioned but no note exists - mentioned styling
            mermaidCode += `${nodeId}["${cleanName}"]:::mentioned-link\n`;
        }
        
        // Add tooltip with full faction name and basic info
        let tooltipText = faction;
        if (relationships[faction]) {
            // Count relationships for tooltip
            let relCount = 0;
            for (let relType in relationships[faction]) {
                relCount += relationships[faction][relType].length;
            }
            if (relCount > 0) {
                tooltipText += ` (${relCount} relationships)`;
            }
        } else {
            tooltipText += " (mentioned only)";
        }
        
        // Add click event and tooltip
        mermaidCode += `click ${nodeId} href "obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(faction)}" "${tooltipText}"\n`;
        
        nodeIndex++;
    }
    
    // Add relationships - only include if both factions are in our set
    for (let faction in relationships) {
        if (!factionsToInclude.has(faction)) continue;
        
        let sourceNode = nodeMap[faction];
        
        // Allies (solid green arrows)
        for (let ally of relationships[faction].allies || []) {
            if (nodeMap[ally]) {
                mermaidCode += `${sourceNode} -->|🤝 ally| ${nodeMap[ally]}\n`;
            }
        }
        
        // Enemies (thick red dotted arrows)
        for (let enemy of relationships[faction].enemies || []) {
            if (nodeMap[enemy]) {
                mermaidCode += `${sourceNode} -.->|⚔️ enemy| ${nodeMap[enemy]}\n`;
            }
        }
        
        // Rivals (purple dotted bidirectional)
        for (let rival of relationships[faction].rivals || []) {
            if (nodeMap[rival]) {
                mermaidCode += `${sourceNode} <-.->|🥊 rival| ${nodeMap[rival]}\n`;
            }
        }
        
        // Patrons (thick blue arrows pointing TO faction)
        for (let patron of relationships[faction].patrons || []) {
            if (nodeMap[patron]) {
                mermaidCode += `${nodeMap[patron]} ==>|⬆️ patron| ${sourceNode}\n`;
            }
        }
        
        // Vassals (thick blue arrows pointing FROM faction)
        for (let vassal of relationships[faction].vassals || []) {
            if (nodeMap[vassal]) {
                mermaidCode += `${sourceNode} ==>|⬇️ vassal| ${nodeMap[vassal]}\n`;
            }
        }
        
        // Trading partners (orange bidirectional solid)
        for (let partner of relationships[faction].trading_partners || []) {
            if (nodeMap[partner]) {
                mermaidCode += `${sourceNode} <-->|💰 trade| ${nodeMap[partner]}\n`;
            }
        }
        
        // Infiltrated by (red dotted arrow TO faction)
        for (let spy of relationships[faction].infiltrated_by || []) {
            if (nodeMap[spy]) {
                mermaidCode += `${nodeMap[spy]} -.->|🕵️ spy| ${sourceNode}\n`;
            }
        }
        
        // Competing with (yellow dotted bidirectional)
        for (let competitor of relationships[faction].competing_with || []) {
            if (nodeMap[competitor]) {
                mermaidCode += `${sourceNode} <-.->|🏆 compete| ${nodeMap[competitor]}\n`;
            }
        }
        
        // Neutral (gray simple line)
        for (let neutral of relationships[faction].neutral_toward || []) {
            if (nodeMap[neutral]) {
                mermaidCode += `${sourceNode} ---|😐 neutral| ${nodeMap[neutral]}\n`;
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
        factionCount: factionsToInclude.size,
        filterMatched: actualFilterFaction
    };
}

// Main execution
if (window.factionData) {
    const relationships = window.factionData.relationships;
    const result = generateFilteredNetworkDiagram(relationships, filterValue);
    
    // Display status
    if (filterValue.trim()) {
        if (result.filterMatched) {
            dv.paragraph(`🎯 **Filtered View**: Showing relationships for "${result.filterMatched}" (${result.factionCount} factions)`);
        } else {
            dv.paragraph(`⚠️ **Filter Not Found**: "${filterValue}" not found - showing all factions instead (${result.factionCount} total)`);
        }
    } else {
        dv.paragraph(`🌐 **Full Network**: Showing all factions (${result.factionCount} total)`);
    }
    
    // Display the map
    dv.paragraph(result.code);
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```

```dataviewjs
// Faction Mindmap Generator
dv.header(2, "🕸️ Mindmap focus: `=this.factionfilter`");

// Read the filter value from YAML frontmatter
const filterValue = dv.current().factionFilter || "";

// Mindmap generator for focused faction view
function generateFactionMindmap(relationships, targetFaction) {
    // Enhanced fuzzy matching
    let actualFaction = null;
    const trimmedFilter = targetFaction.trim().toLowerCase();
    
    // Try exact match first
    if (relationships[targetFaction.trim()]) {
        actualFaction = targetFaction.trim();
    } else {
        // Enhanced fuzzy matching
        for (let faction in relationships) {
            const factionLower = faction.toLowerCase();
            
            if (factionLower === trimmedFilter ||
                factionLower.replace(/^the /, '') === trimmedFilter.replace(/^the /, '') ||
                factionLower === "the " + trimmedFilter ||
                factionLower.includes(trimmedFilter) ||
                trimmedFilter.includes(factionLower.replace(/^the /, ''))) {
                actualFaction = faction;
                break;
            }
            
            // Word-based matching
            const filterWords = trimmedFilter.split(/\s+/);
            const factionWords = factionLower.split(/\s+/);
            
            for (let filterWord of filterWords) {
                if (filterWord.length > 2) {
                    for (let factionWord of factionWords) {
                        if (factionWord.includes(filterWord) || filterWord.includes(factionWord)) {
                            actualFaction = faction;
                            break;
                        }
                    }
                    if (actualFaction) break;
                }
            }
            if (actualFaction) break;
        }
    }
    
    if (!actualFaction) {
        return { code: null, filterMatched: null };
    }
    
    function sanitizeForMindmap(text) {
        return text
            .replace(/[[\]]/g, '')
            .replace(/[()]/g, '')
            .replace(/"/g, '')
            .replace(/'/g, '')
            .replace(/'/g, '')
            .trim();
    }
    
    let mermaidCode = "```mermaid\nmindmap\n";
    mermaidCode += `  root((${sanitizeForMindmap(actualFaction)}))\n`;
    
    const factionData = relationships[actualFaction];
    let hasRelationships = false;
    
    // Collect all relationships - both outgoing AND incoming
    let allRelationships = {
        allies: new Set(factionData.allies || []),
        enemies: new Set(factionData.enemies || []),
        rivals: new Set(factionData.rivals || []),
        patrons: new Set(factionData.patrons || []),
        vassals: new Set(factionData.vassals || []),
        trading_partners: new Set(factionData.trading_partners || []),
        infiltrated_by: new Set(factionData.infiltrated_by || []),
        competing_with: new Set(factionData.competing_with || []),
        neutral_toward: new Set(factionData.neutral_toward || [])
    };
    
    // Add incoming relationships (other factions that mention this faction)
    for (let otherFaction in relationships) {
        if (otherFaction === actualFaction) continue;
        
        const otherData = relationships[otherFaction];
        
        // If they list us as ally, we should show them as ally too
        if (otherData.allies && otherData.allies.includes(actualFaction)) {
            allRelationships.allies.add(otherFaction);
        }
        if (otherData.enemies && otherData.enemies.includes(actualFaction)) {
            allRelationships.enemies.add(otherFaction);
        }
        if (otherData.rivals && otherData.rivals.includes(actualFaction)) {
            allRelationships.rivals.add(otherFaction);
        }
        // If they list us as patron, we should show them as vassal
        if (otherData.patrons && otherData.patrons.includes(actualFaction)) {
            allRelationships.vassals.add(otherFaction);
        }
        // If they list us as vassal, we should show them as patron
        if (otherData.vassals && otherData.vassals.includes(actualFaction)) {
            allRelationships.patrons.add(otherFaction);
        }
        if (otherData.trading_partners && otherData.trading_partners.includes(actualFaction)) {
            allRelationships.trading_partners.add(otherFaction);
        }
        if (otherData.infiltrated_by && otherData.infiltrated_by.includes(actualFaction)) {
            allRelationships.infiltrated_by.add(otherFaction);
        }
        if (otherData.competing_with && otherData.competing_with.includes(actualFaction)) {
            allRelationships.competing_with.add(otherFaction);
        }
        if (otherData.neutral_toward && otherData.neutral_toward.includes(actualFaction)) {
            allRelationships.neutral_toward.add(otherFaction);
        }
    }
    
    // Add each relationship type as a branch
    if (allRelationships.allies.size > 0) {
        hasRelationships = true;
        mermaidCode += `    🤝 Allies\n`;
        for (let ally of Array.from(allRelationships.allies).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(ally)}\n`;
        }
    }
    
    if (allRelationships.enemies.size > 0) {
        hasRelationships = true;
        mermaidCode += `    ⚔️ Enemies\n`;
        for (let enemy of Array.from(allRelationships.enemies).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(enemy)}\n`;
        }
    }
    
    if (allRelationships.rivals.size > 0) {
        hasRelationships = true;
        mermaidCode += `    🥊 Rivals\n`;
        for (let rival of Array.from(allRelationships.rivals).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(rival)}\n`;
        }
    }
    
    if (allRelationships.patrons.size > 0) {
        hasRelationships = true;
        mermaidCode += `    ⬆️ Patrons\n`;
        for (let patron of Array.from(allRelationships.patrons).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(patron)}\n`;
        }
    }
    
    if (allRelationships.vassals.size > 0) {
        hasRelationships = true;
        mermaidCode += `    ⬇️ Vassals\n`;
        for (let vassal of Array.from(allRelationships.vassals).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(vassal)}\n`;
        }
    }
    
    if (allRelationships.trading_partners.size > 0) {
        hasRelationships = true;
        mermaidCode += `    💰 Trading Partners\n`;
        for (let partner of Array.from(allRelationships.trading_partners).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(partner)}\n`;
        }
    }
    
    if (allRelationships.infiltrated_by.size > 0) {
        hasRelationships = true;
        mermaidCode += `    🕵️ Espionage Relations\n`;
        for (let spy of Array.from(allRelationships.infiltrated_by).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(spy)}\n`;
        }
    }
    
    if (allRelationships.competing_with.size > 0) {
        hasRelationships = true;
        mermaidCode += `    🏆 Competing With\n`;
        for (let competitor of Array.from(allRelationships.competing_with).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(competitor)}\n`;
        }
    }
    
    if (allRelationships.neutral_toward.size > 0) {
        hasRelationships = true;
        mermaidCode += `    😐 Neutral Relations\n`;
        for (let neutral of Array.from(allRelationships.neutral_toward).sort()) {
            mermaidCode += `      ${sanitizeForMindmap(neutral)}\n`;
        }
    }
    
    if (!hasRelationships) {
        mermaidCode += `    📝 No Relationships\n`;
        mermaidCode += `      Define relationships in faction YAML\n`;
    }
    
    mermaidCode += "```";
    
    return {
        code: mermaidCode,
        filterMatched: actualFaction,
        type: "mindmap",
        relationshipCount: Object.values(allRelationships).reduce((total, set) => total + set.size, 0)
    };
}

// Main execution
if (window.factionData) {
    const relationships = window.factionData.relationships;
    
    if (filterValue.trim()) {
        // Generate mindmap for specific faction
        const result = generateFactionMindmap(relationships, filterValue);
        
        if (result.filterMatched) {
            dv.paragraph(`🎯 **"${result.filterMatched}"** - ${result.relationshipCount} total relationships`);
            dv.paragraph(result.code);
        } else {
            dv.paragraph(`⚠️ **Faction Not Found**: "${filterValue}"`);
            dv.paragraph("**Available factions:**");
            
            // Show available factions as help
            const availableFactions = Object.keys(relationships).sort();
            for (let faction of availableFactions) {
                dv.paragraph(`- ${faction}`);
            }
        }
    } else {
        dv.paragraph("💡 **Set faction name** in the YAML frontmatter above to generate mindmap");
        dv.paragraph("**Available factions:**");
        
        // Show available factions as help  
        const availableFactions = Object.keys(relationships).sort();
        for (let faction of availableFactions.slice(0, 20)) {
            dv.paragraph(`- ${faction}`);
        }
        if (availableFactions.length > 20) {
            dv.paragraph(`*... and ${availableFactions.length - 20} more*`);
        }
    }
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```


## 🗺️ Relationship Legend
🤝 **Allies** | ⚔️ **Enemies** | 🥊 **Rivals** | ⬆️ **Patrons** | ⬇️ **Vassals**  
💰 **Trading Partners** | 🕵️ **Espionage Relations** | 🏆 **Competing With** | 😐 **Neutral Relations**

---

### 📝 How to Use This Mindmap Viewer

1. **Edit the YAML** at the top: Change `factionFilter: ""` to `factionFilter: "House Alvares"`
2. **Refresh the note** (Ctrl+R) to generate the mindmap
3. **Full faction names** are supported with fuzzy matching (e.g., "Cautier" finds "The Cautier School")
4. **Bidirectional relationships** are shown (includes all factions that reference this one)