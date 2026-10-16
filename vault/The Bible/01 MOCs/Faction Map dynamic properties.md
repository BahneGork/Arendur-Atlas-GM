---
factionFilter: The Shadow Company
relationshipConfig:
  core:
    - allies
    - enemies
    - rivals
  extended:
    - patrons
    - vassals
    - infiltrated_by
    - competing_with
    - neutral_toward
    - trading_partners
    - Open_Warfare
    - Active_Intrigue
  custom: 
  active:
    - allies
    - enemies
    - rivals
    - patrons
    - vassals
    - trading_partners
    - Open_Warfare
    - Active_Intrigue
  display:
    allies:
      icon: 🤝
      color: green
      style: solid
      bidirectional: true
    enemies:
      icon: ⚔️
      color: red
      style: dotted
      bidirectional: false
    rivals:
      icon: 🥊
      color: purple
      style: dotted
      bidirectional: true
    patrons:
      icon: ⬆️
      color: blue
      style: thick
      bidirectional: false
      reverse_arrow: true
    vassals:
      icon: ⬇️
      color: blue
      style: thick
      bidirectional: false
    trading_partners:
      icon: 💰
      color: orange
      style: solid
      bidirectional: true
    infiltrated_by:
      icon: 🕵️
      color: red
      style: dotted
      bidirectional: false
      reverse_arrow: true
    competing_with:
      icon: 🏆
      color: yellow
      style: dotted
      bidirectional: true
    neutral_toward:
      icon: 🤷
      color: gray
      style: solid
      bidirectional: true
    Open_Warfare:
      icon: ⚔️
      color: red
      style: solid
      bidirectional: false
    Active_Intrigue:
      icon: 🔥
      color: orange
      style: solid
      bidirectional: false
---


# Dynamic Properties Management
```dataviewjs
// Dynamic Relationship Configuration Manager - COMPLETE FIXED VERSION

dv.header(2, "⚙️ Relationship Configuration Manager");

// Debug logging
console.log('Configuration Manager Loading...');
console.log('Current window.relationshipConfigDynamic:', window.relationshipConfigDynamic);
console.log('Current window.factionDataUnified:', !!window.factionDataUnified);

// FIXED: Configuration Loading with Debug
const currentConfigDynamic = dv.current().relationshipConfig || {};
console.log('LOADED YAML CONFIG:', currentConfigDynamic);

const defaultConfigDynamic = {
    core: ['allies', 'enemies', 'rivals'],
    extended: ['patrons', 'vassals', 'trading_partners', 'infiltrated_by', 'competing_with', 'neutral_toward'],
    custom: [],
    active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners'],
    display: {
        allies: { icon: "🤝", color: "green", style: "solid", bidirectional: true },
        enemies: { icon: "⚔️", color: "red", style: "dotted", bidirectional: false },
        rivals: { icon: "🥊", color: "purple", style: "dotted", bidirectional: true },
        patrons: { icon: "⬆️", color: "blue", style: "thick", bidirectional: false, reverse_arrow: true },
        vassals: { icon: "⬇️", color: "blue", style: "thick", bidirectional: false },
        trading_partners: { icon: "💰", color: "orange", style: "solid", bidirectional: true },
        infiltrated_by: { icon: "🕵️", color: "red", style: "dotted", bidirectional: false, reverse_arrow: true },
        competing_with: { icon: "🏆", color: "yellow", style: "dotted", bidirectional: true },
        neutral_toward: { icon: "🤷", color: "gray", style: "solid", bidirectional: true }
    }
};

// FIXED: Proper configuration merge that preserves YAML data
const configDynamic = {
    core: currentConfigDynamic.core || defaultConfigDynamic.core,
    extended: currentConfigDynamic.extended || defaultConfigDynamic.extended,
    custom: currentConfigDynamic.custom || defaultConfigDynamic.custom,
    active: currentConfigDynamic.active || defaultConfigDynamic.active,
    display: { ...defaultConfigDynamic.display, ...(currentConfigDynamic.display || {}) }
};

console.log('MERGED CONFIG:', configDynamic);

// FIXED: Validate configuration integrity and add missing display configs
const allTypesFromConfig = [
    ...configDynamic.core,
    ...configDynamic.extended,
    ...configDynamic.custom
];

allTypesFromConfig.forEach(relType => {
    if (!configDynamic.display[relType]) {
        console.warn(`Missing display config for relationship type: ${relType}`);
        configDynamic.display[relType] = { icon: "❓", color: "gray", style: "solid", bidirectional: false };
    }
});

// Store merged config globally
window.relationshipConfigDynamic = {
    ...configDynamic,
    version: Date.now()
};

// Create interactive configuration interface
const containerDynamic = dv.container;
containerDynamic.innerHTML = `
<div style="margin: 10px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
    <h3>🔧 Current Configuration</h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
        <div>
            <h4>📋 Available Relationship Types</h4>
            <div id="availableTypesDynamic" style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background: var(--background-primary);"></div>
        </div>
        
        <div>
            <h4>✅ Active Relationship Types</h4>
            <div id="activeTypesDynamic" style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background: var(--background-primary);"></div>
        </div>
    </div>
    
    <div style="margin-bottom: 15px;">
        <h4>➕ Add Custom Relationship Type</h4>
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <input type="text" id="customTypeNameDynamic" placeholder="e.g., branch_offices" style="width: 200px; padding: 5px;">
            
            <div style="display: flex; align-items: center; gap: 5px;">
                <select id="customTypeIconDropdownDynamic" style="padding: 5px; font-size: 16px; width: 120px;">
                    <option value="">Choose Icon...</option>
                    <option value="🏢">🏢 Building</option>
                    <option value="🤝">🤝 Partnership</option>
                    <option value="💼">💼 Business</option>
                    <option value="🎯">🎯 Target</option>
                    <option value="🔗">🔗 Connection</option>
                    <option value="⚖️">⚖️ Legal</option>
                    <option value="🗡️">🗡️ Military</option>
                    <option value="📜">📜 Contract</option>
                    <option value="👑">👑 Authority</option>
                    <option value="🔥">🔥 Conflict</option>
                </select>
                
                <span style="font-size: 12px;">OR</span>
                
                <input type="text" id="customTypeIconDynamic" placeholder="Custom emoji" style="width: 100px; padding: 5px; text-align: center;">
            </div>
            
            <select id="customTypeColorDynamic" style="padding: 5px;">
                <option value="red">Red</option>
                <option value="blue">Blue</option>
                <option value="green">Green</option>
                <option value="orange">Orange</option>
                <option value="purple">Purple</option>
                <option value="yellow">Yellow</option>
                <option value="gray">Gray</option>
                <option value="pink">Pink</option>
                <option value="brown">Brown</option>
            </select>
            
            <button id="addCustomTypeDynamic" style="padding: 5px 15px; background-color: #28a745; color: white; border: none; border-radius: 3px;">Add Type</button>
        </div>
        <div style="font-size: 11px; color: #666; margin-top: 5px;">
            Both name and icon are required.<br>
            🎯 <strong>Tip:</strong> After creating, use the "⬆️ Default" button to promote custom types to default detection - perfect for importing existing faction setups!
        </div>
    </div>
    
    <div style="margin-bottom: 15px;">
        <button id="resetConfigDynamic" style="padding: 8px 15px; background-color: #dc3545; color: white; border: none; border-radius: 3px; margin-right: 10px;">🔄 Reset to Default</button>
        <button id="undoResetDynamic" style="padding: 8px 15px; background-color: #6c757d; color: white; border: none; border-radius: 3px;" disabled>↶ Return to Last Known Configuration</button>
    </div>
</div>
`;

// Persist configuration to YAML frontmatter
async function persistConfigToYAMLDynamic() {
    try {
        const currentFile = app.workspace.getActiveFile();
        if (!currentFile) return;
        
        const fileContent = await app.vault.read(currentFile);
        const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
        const match = frontmatterRegex.exec(fileContent);
        
        if (match) {
            // Parse existing frontmatter
            const existingYaml = match[1];
            let newYaml = existingYaml;
            
            // Remove existing relationshipConfig section
            newYaml = newYaml.replace(/relationshipConfig:[\s\S]*?(?=\n[a-zA-Z]|\n---|\n$|$)/g, '');
            
            // Add updated relationshipConfig
            const yamlConfig = `relationshipConfig:
  core:
${configDynamic.core.map(t => `    - ${t}`).join('\n')}
  extended:
${configDynamic.extended.map(t => `    - ${t}`).join('\n')}
  custom:
${configDynamic.custom.map(t => `    - ${t}`).join('\n')}
  active:
${configDynamic.active.map(t => `    - ${t}`).join('\n')}
  display:
${Object.entries(configDynamic.display).map(([type, settings]) => {
    return `    ${type}:
      icon: "${settings.icon}"
      color: "${settings.color}"
      style: "${settings.style}"
      bidirectional: ${settings.bidirectional}${settings.reverse_arrow ?
'\n      reverse_arrow: true' : ''}`;
}).join('\n')}`;
            
            // Clean up and add new config
            newYaml = newYaml.trim();
            if (newYaml) {
                newYaml += '\n' + yamlConfig;
            } else {
                newYaml = yamlConfig;
            }
            
            // Update file content
            const newContent = fileContent.replace(frontmatterRegex, `---\n${newYaml}\n---`);
            await app.vault.modify(currentFile, newContent);
            
            console.log('Configuration persisted to YAML frontmatter');
        }
    } catch (error) {
        console.error('Failed to persist config to YAML:', error);
    }
}

// FIXED: updateTypeDisplaysDynamic function that includes ALL types
function updateTypeDisplaysDynamic() {
    const availableDiv = containerDynamic.querySelector('#availableTypesDynamic');
    const activeDiv = containerDynamic.querySelector('#activeTypesDynamic');
    
    // FIXED: Get ALL unique relationship types including those in active array
    const allTypesSet = new Set([
        ...configDynamic.core,
        ...configDynamic.extended,
        ...configDynamic.custom,
        ...configDynamic.active  // ADDED: Include types from active array
    ]);
    const allTypesDynamic = Array.from(allTypesSet);
    
    console.log('ALL TYPES TO DISPLAY:', allTypesDynamic);
    console.log('ACTIVE TYPES:', configDynamic.active);
    console.log('CORE TYPES:', configDynamic.core);
    console.log('EXTENDED TYPES:', configDynamic.extended);
    console.log('CUSTOM TYPES:', configDynamic.custom);
    
    availableDiv.innerHTML = '';
    activeDiv.innerHTML = '';
    
    allTypesDynamic.forEach(type => {
        const displayInfo = configDynamic.display[type] || { icon: "❓", color: "gray" };
        const isActive = configDynamic.active.includes(type);
        const isCore = configDynamic.core.includes(type);
        const isExtended = configDynamic.extended.includes(type);
        const isCustom = configDynamic.custom.includes(type);
        
        // FIXED: Determine ACTUAL category with proper logic for orphaned types
        let actualCategory;
        let categoryBadge = '';
        let specialButtons = '';
        
        if (isCore) {
            actualCategory = 'core';
            categoryBadge = '<span style="font-size: 9px; background: #007bff; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">CORE</span>';
        } else if (isExtended && defaultConfigDynamic.extended.includes(type)) {
            // Default extended type
            actualCategory = 'extended';
            categoryBadge = '<span style="font-size: 9px; background: #17a2b8; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">DEFAULT</span>';
            specialButtons = `<button onclick="demoteExtendedTypeDynamic('${type}')" style="padding: 2px 6px; font-size: 10px; background: #ffc107; color: black; border: none; border-radius: 2px; margin-left: 3px;" title="Demote to custom">⬇️ Custom</button>`;
        } else if (isExtended && !defaultConfigDynamic.extended.includes(type)) {
            // Promoted custom type
            actualCategory = 'promoted';
            categoryBadge = '<span style="font-size: 9px; background: #28a745; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">PROMOTED</span>';
            specialButtons = `<button onclick="demoteExtendedTypeDynamic('${type}')" style="padding: 2px 6px; font-size: 10px; background: #ffc107; color: black; border: none; border-radius: 2px; margin-left: 3px;" title="Demote to custom">⬇️ Custom</button>`;
        } else if (isCustom) {
            // Regular custom type
            actualCategory = 'custom';
            categoryBadge = '<span style="font-size: 9px; background: #6f42c1; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">CUSTOM</span>';
            specialButtons = `<button onclick="promoteCustomTypeDynamic('${type}')" style="padding: 2px 6px; font-size: 10px; background: #28a745; color: white; border: none; border-radius: 2px; margin-left: 3px;" title="Promote to default detection">⬆️ Default</button>`;
        } else if (isActive && !isCore && !isExtended && !isCustom) {
            // ADDED: Type exists in active but not in any category - this is the case for your missing types
            actualCategory = 'orphaned';
            categoryBadge = '<span style="font-size: 9px; background: #dc3545; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">ORPHANED</span>';
            specialButtons = `<button onclick="adoptOrphanedType('${type}')" style="padding: 2px 6px; font-size: 10px; background: #17a2b8; color: white; border: none; border-radius: 2px; margin-left: 3px;" title="Add to custom category">Fix</button>`;
        } else {
            // Fallback
            actualCategory = 'unknown';
            categoryBadge = '<span style="font-size: 9px; background: #6c757d; color: white; padding: 1px 4px; border-radius: 2px; margin-left: 5px;">UNKNOWN</span>';
            specialButtons = `<button onclick="adoptOrphanedType('${type}')" style="padding: 2px 6px; font-size: 10px; background: #17a2b8; color: white; border: none; border-radius: 2px; margin-left: 3px;">Fix</button>`;
        }
        
        const typeElement = `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; margin: 3px 0; border-radius: 4px; background: ${isActive ? '#d4edda' : '#f8f9fa'}; border-left: 3px solid ${actualCategory === 'core' ? '#007bff' : actualCategory === 'extended' ? '#17a2b8' : actualCategory === 'promoted' ? '#28a745' : actualCategory === 'custom' ? '#6f42c1' : '#dc3545'};">
                <div style="display: flex; align-items: center; flex: 1;">
                    <span style="font-weight: ${isActive ? 'bold' : 'normal'};">${displayInfo.icon} ${type}</span>
                    ${categoryBadge}
                </div>
                <div style="display: flex; align-items: center; gap: 3px;">
                    ${isActive ? 
                        `<button onclick="toggleTypeDynamic('${type}', false)" style="padding: 3px 8px; font-size: 11px; background: #dc3545; color: white; border: none; border-radius: 2px;">Remove</button>` :
                        `<button onclick="toggleTypeDynamic('${type}', true)" style="padding: 3px 8px; font-size: 11px; background: #28a745; color: white; border: none; border-radius: 2px;">Add</button>`
                    }
                    ${specialButtons}
                    ${(actualCategory === 'custom' || actualCategory === 'promoted' || actualCategory === 'orphaned') ? 
                        `<button onclick="removeCustomTypeDynamic('${type}')" style="padding: 3px 8px; font-size: 11px; background: #dc3545; color: white; border: none; border-radius: 2px;" title="Permanently delete this type">🗑️ Delete</button>` : ''
                    }
                </div>
            </div>
        `;
        
        if (isActive) {
            activeDiv.innerHTML += typeElement;
        } else {
            availableDiv.innerHTML += typeElement;
        }
    });
}

// Global functions for buttons with unique names
let configVersionDynamic = Date.now();
let lastKnownConfigDynamic = null; // Store backup before reset

// FIXED: Centralized config update function
function updateGlobalConfigAndPersist() {
    // Update with versioning
    configVersionDynamic = Date.now();
    window.relationshipConfigDynamic = {
        ...configDynamic,
        version: Date.now()
    };
    
    // Clear cached data
    if (window.factionDataUnified) {
        delete window.factionDataUnified;
    }
    if (window.factionDataVersion) {
        delete window.factionDataVersion;
    }
    
    // Persist to YAML
    persistConfigToYAMLDynamic();
    
    console.log('Configuration updated and persisted, version:', configVersionDynamic);
}

// FIXED: Toggle relationship type active/inactive
window.toggleTypeDynamic = function(type, add) {
    if (add && !configDynamic.active.includes(type)) {
        configDynamic.active.push(type);
    } else if (!add) {
        configDynamic.active = configDynamic.active.filter(t => t !== type);
    }
    updateTypeDisplaysDynamic();
    updateGlobalConfigAndPersist();
};

// FIXED: Promote/Demote functions with proper array management
window.promoteCustomTypeDynamic = function(type) {
    console.log(`Promoting ${type} from custom to extended`);
    
    if (configDynamic.custom.includes(type)) {
        // FIXED: Proper array management - remove from custom first
        configDynamic.custom = configDynamic.custom.filter(t => t !== type);
        
        // Add to extended (avoid duplicates)
        if (!configDynamic.extended.includes(type)) {
            configDynamic.extended.push(type);
        }
        
        // Ensure it's active
        if (!configDynamic.active.includes(type)) {
            configDynamic.active.push(type);
        }
        
        console.log('Post-promotion config:', {
            custom: configDynamic.custom,
            extended: configDynamic.extended,
            active: configDynamic.active
        });
        
        updateTypeDisplaysDynamic();
        updateGlobalConfigAndPersist();
        
        // Show success message
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            background: #28a745; color: white; padding: 10px 20px;
            border-radius: 5px; font-weight: bold;
        `;
        notification.textContent = `✅ "${type}" promoted! Faction data rebuilding...`;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
};

window.demoteExtendedTypeDynamic = function(type) {
    console.log(`Demoting ${type} from extended to custom`);
    
    if (configDynamic.extended.includes(type) && !configDynamic.core.includes(type)) {
        if (confirm(`Demote "${type}" to custom? This will remove it from default faction detection.`)) {
            // FIXED: Proper array management - remove from extended first
            configDynamic.extended = configDynamic.extended.filter(t => t !== type);
            
            // Add to custom (avoid duplicates)
            if (!configDynamic.custom.includes(type)) {
                configDynamic.custom.push(type);
            }
            
            console.log('Post-demotion config:', {
                extended: configDynamic.extended,
                custom: configDynamic.custom,
                active: configDynamic.active
            });
            
            updateTypeDisplaysDynamic();
            updateGlobalConfigAndPersist();
        }
    }
};

// NEW: Fix orphaned types
window.adoptOrphanedType = function(type) {
    console.log(`Adopting orphaned type: ${type}`);
    
    // Add to custom if not already there
    if (!configDynamic.custom.includes(type)) {
        configDynamic.custom.push(type);
    }
    
    // Ensure it has display config
    if (!configDynamic.display[type]) {
        configDynamic.display[type] = { icon: "❓", color: "gray", style: "solid", bidirectional: false };
    }
    
    updateTypeDisplaysDynamic();
    updateGlobalConfigAndPersist();
};

// FIXED: Remove custom relationship type
window.removeCustomTypeDynamic = function(type) {
    if (confirm(`Permanently delete "${type}"? This cannot be undone.`)) {
        // Remove from ALL arrays
        configDynamic.custom = configDynamic.custom.filter(t => t !== type);
        configDynamic.extended = configDynamic.extended.filter(t => t !== type);
        configDynamic.active = configDynamic.active.filter(t => t !== type);
        delete configDynamic.display[type];
        
        updateTypeDisplaysDynamic();
        updateGlobalConfigAndPersist();
        
        console.log('Custom type removed:', type);
    }
};

// Add custom type functionality
const addButton = containerDynamic.querySelector('#addCustomTypeDynamic');
const nameInput = containerDynamic.querySelector('#customTypeNameDynamic');
const iconDropdown = containerDynamic.querySelector('#customTypeIconDropdownDynamic');
const iconCustom = containerDynamic.querySelector('#customTypeIconDynamic');
const colorSelect = containerDynamic.querySelector('#customTypeColorDynamic');

if (addButton && nameInput && iconDropdown && iconCustom && colorSelect) {
    addButton.addEventListener('click', () => {
        console.log('Add custom type button clicked'); // Debug
        
        const name = nameInput.value.trim();
        const iconDropdownValue = iconDropdown.value;
        const iconCustomValue = iconCustom.value.trim();
        const color = colorSelect.value;
        
        console.log('Input values:', { name, iconDropdownValue, iconCustomValue, color }); // Debug
        
        // Use dropdown icon if selected, otherwise use custom input
        const icon = iconDropdownValue || iconCustomValue;
        
        if (name && icon) {
            if (!configDynamic.custom.includes(name)) {
                try {
                    configDynamic.custom.push(name);
                    configDynamic.display[name] = {
                        icon: icon,
                        color: color,
                        style: "solid",
                        bidirectional: false
                    };
                    
                    // Clear inputs
                    nameInput.value = '';
                    iconDropdown.value = '';
                    iconCustom.value = '';
                    colorSelect.value = 'red';
                    
                    updateTypeDisplaysDynamic();
                    updateGlobalConfigAndPersist();
                    
                    console.log('Custom type added:', name, icon, color);
                } catch (error) {
                    console.error('Error adding custom type:', error);
                    alert(`Error adding custom type: ${error.message}`);
                }
            } else {
                alert('A relationship type with that name already exists!');
            }
        } else {
            alert('Please provide both name and icon (select from dropdown OR enter custom emoji)!');
        }
    });

    // Add change handler for dropdown to clear custom input when dropdown is used
    iconDropdown.addEventListener('change', function() {
        console.log('Dropdown changed:', this.value); // Debug
        if (this.value) {
            iconCustom.value = '';
        }
    });

    // Add change handler for custom input to clear dropdown when custom is used
    iconCustom.addEventListener('input', function() {
        console.log('Custom input changed:', this.value); // Debug
        if (this.value.trim()) {
            iconDropdown.value = '';
        }
    });
    
    // Add debug handler for name input
    nameInput.addEventListener('input', function() {
        console.log('Name input changed:', this.value); // Debug
    });
    
} else {
    console.error('One or more custom type elements not found:', {
        addButton: !!addButton,
        nameInput: !!nameInput,
        iconDropdown: !!iconDropdown,
        iconCustom: !!iconCustom,
        colorSelect: !!colorSelect
    });
}

// Reset to default configuration
const resetButton = containerDynamic.querySelector('#resetConfigDynamic');
const undoButton = containerDynamic.querySelector('#undoResetDynamic');

if (resetButton) {
    resetButton.addEventListener('click', () => {
        console.log('Reset button clicked'); // Debug log
        if (confirm('Are you sure you want to reset to default configuration? This will remove all custom relationship types.')) {
            console.log('Reset confirmed'); // Debug log
            
            // BACKUP CURRENT CONFIG before reset
            lastKnownConfigDynamic = {
                core: [...configDynamic.core],
                extended: [...configDynamic.extended],
                custom: [...configDynamic.custom],
                active: [...configDynamic.active],
                display: JSON.parse(JSON.stringify(configDynamic.display)) // Deep copy
            };
            
            // Reset to defaults
            Object.assign(configDynamic, {
                core: [...defaultConfigDynamic.core],
                extended: [...defaultConfigDynamic.extended],
                custom: [],
                active: [...defaultConfigDynamic.active],
                display: { ...defaultConfigDynamic.display }
            });
            
            updateTypeDisplaysDynamic();
            updateGlobalConfigAndPersist();
            
            // Enable undo button
            if (undoButton) {
                undoButton.disabled = false;
                undoButton.style.backgroundColor = '#17a2b8';
                undoButton.style.cursor = 'pointer';
            }
            
            // Visual feedback
            resetButton.textContent = '✅ Reset Complete!';
            resetButton.style.backgroundColor = '#28a745';
            
            setTimeout(() => {
                resetButton.textContent = '🔄 Reset to Default';
                resetButton.style.backgroundColor = '#dc3545';
            }, 2000);
            
            console.log('Configuration reset to default and persisted');
        }
    });
} else {
    console.error('Reset button not found in DOM');
}

// Undo reset functionality
if (undoButton) {
    undoButton.addEventListener('click', () => {
        console.log('Undo button clicked'); // Debug log
        
        if (!lastKnownConfigDynamic) {
            alert('No previous configuration to restore!');
            return;
        }
        
        if (confirm('Restore your previous configuration? This will undo the reset.')) {
            console.log('Undo confirmed'); // Debug log
            
            // Restore from backup
            Object.assign(configDynamic, {
                core: [...lastKnownConfigDynamic.core],
                extended: [...lastKnownConfigDynamic.extended],
                custom: [...lastKnownConfigDynamic.custom],
                active: [...lastKnownConfigDynamic.active],
                display: JSON.parse(JSON.stringify(lastKnownConfigDynamic.display))
            });
            
            updateTypeDisplaysDynamic();
            updateGlobalConfigAndPersist();
            
            // Disable undo button (can only undo once)
            undoButton.disabled = true;
            undoButton.style.backgroundColor = '#6c757d';
            undoButton.style.cursor = 'not-allowed';
            
            // Clear the backup (prevent multiple undos)
            lastKnownConfigDynamic = null;
            
            // Visual feedback
            undoButton.textContent = '✅ Configuration Restored!';
            
            setTimeout(() => {
                undoButton.textContent = '↶ Return to Last Known Configuration';
            }, 2000);
            
            console.log('Configuration restored from backup and persisted');
        }
    });
} else {
    console.error('Undo button not found in DOM');
}

// Initial display
updateTypeDisplaysDynamic();

dv.paragraph(`**Currently Active**: ${configDynamic.active.length} relationship types | **Available**: ${configDynamic.core.length + configDynamic.extended.length + configDynamic.custom.length} total types`);
```


```meta-bind-button
label: refresh
icon: ""
hidden: false
class: ""
tooltip: ""
id: refreshB
style: primary
actions:
  - type: command
    command: dataview:dataview-rebuild-current-view

```

```dataviewjs
// Configuration Sharing Utilities - With Close Buttons
dv.header(3, "📤 Configuration Sharing");

const shareContainerDynamic = dv.container;
shareContainerDynamic.innerHTML = `
<div style="margin: 10px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
    <h4>🔗 Quick Share Links</h4>
    <div style="margin-bottom: 15px;">
        <button id="generateShareLinkDynamic" style="padding: 8px 15px; background-color: #17a2b8; color: white; border: none; border-radius: 3px; margin-right: 10px;">Generate Share Code</button>
        <button id="loadFromCodeDynamic" style="padding: 8px 15px; background-color: #28a745; color: white; border: none; border-radius: 3px; margin-right: 10px;">Load from Code</button>
        <button id="debugConfigDynamic" style="padding: 8px 15px; background-color: #ffc107; color: black; border: none; border-radius: 3px; margin-right: 10px;">Debug Config</button>
        <button id="hideAllAreasDynamic" style="padding: 8px 15px; background-color: #6c757d; color: white; border: none; border-radius: 3px;">Hide All</button>
    </div>
    
    <div id="debugInfoDynamic" style="margin-top: 15px; padding: 0; background-color: var(--background-primary); border-radius: 3px; border: 1px solid #ddd; display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: var(--background-modifier-border); border-radius: 3px 3px 0 0; border-bottom: 1px solid #ddd;">
            <h4 style="margin: 0;">Debug Information</h4>
            <button id="closeDebugDynamic" style="padding: 4px 8px; background-color: #dc3545; color: white; border: none; border-radius: 2px; font-size: 12px; cursor: pointer;">✕ Close</button>
        </div>
        <div style="padding: 10px;">
            <pre id="debugTextDynamic" style="font-size: 11px; color: var(--text-muted); margin: 0;"></pre>
        </div>
    </div>
    
    <div id="shareCodeAreaDynamic" style="margin-top: 15px; padding: 0; background-color: var(--background-primary); border-radius: 3px; border: 1px solid #ddd; display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: var(--background-modifier-border); border-radius: 3px 3px 0 0; border-bottom: 1px solid #ddd;">
            <h4 style="margin: 0;">Share Code</h4>
            <button id="closeShareDynamic" style="padding: 4px 8px; background-color: #dc3545; color: white; border: none; border-radius: 2px; font-size: 12px; cursor: pointer;">✕ Close</button>
        </div>
        <div style="padding: 10px;">
            <label for="shareCodeDynamic" style="display: block; margin-bottom: 5px; font-weight: bold;">Copy and share this code:</label>
            <textarea id="shareCodeDynamic" style="width: 100%; height: 120px; font-family: monospace; font-size: 12px; resize: vertical;" readonly></textarea>
            <div style="margin-top: 5px; font-size: 11px; color: var(--text-muted);">
                💡 Copy this code and share with other GMs. They can paste it using "Load from Code" button.
            </div>
        </div>
    </div>
    
    <div id="loadCodeAreaDynamic" style="margin-top: 15px; padding: 0; background-color: var(--background-primary); border-radius: 3px; border: 1px solid #ddd; display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: var(--background-modifier-border); border-radius: 3px 3px 0 0; border-bottom: 1px solid #ddd;">
            <h4 style="margin: 0;">Load Configuration</h4>
            <button id="closeLoadDynamic" style="padding: 4px 8px; background-color: #dc3545; color: white; border: none; border-radius: 2px; font-size: 12px; cursor: pointer;">✕ Close</button>
        </div>
        <div style="padding: 10px;">
            <label for="loadCodeDynamic" style="display: block; margin-bottom: 5px; font-weight: bold;">Paste Share Code:</label>
            <textarea id="loadCodeDynamic" style="width: 100%; height: 120px; font-family: monospace; font-size: 12px; resize: vertical;" placeholder="Paste configuration code here..."></textarea>
            <button id="applyCodeDynamic" style="margin-top: 10px; padding: 8px 15px; background-color: #dc3545; color: white; border: none; border-radius: 3px;">Apply Configuration</button>
        </div>
    </div>
</div>
`;

// UTF-8 safe base64 encoding functions
function utf8ToBase64(str) {
    try {
        return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
            return String.fromCharCode(parseInt(p1, 16));
        }));
    } catch (error) {
        console.error('UTF-8 to Base64 encoding error:', error);
        throw new Error(`Encoding failed: ${error.message}`);
    }
}

function base64ToUtf8(str) {
    try {
        return decodeURIComponent(Array.prototype.map.call(atob(str), function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    } catch (error) {
        console.error('Base64 to UTF-8 decoding error:', error);
        throw new Error(`Decoding failed: ${error.message}`);
    }
}

// Helper function to hide all areas
function hideAllAreasDynamic() {
    shareContainerDynamic.querySelector('#debugInfoDynamic').style.display = 'none';
    shareContainerDynamic.querySelector('#shareCodeAreaDynamic').style.display = 'none';
    shareContainerDynamic.querySelector('#loadCodeAreaDynamic').style.display = 'none';
}

// Close button event listeners
shareContainerDynamic.querySelector('#closeDebugDynamic').addEventListener('click', () => {
    shareContainerDynamic.querySelector('#debugInfoDynamic').style.display = 'none';
});

shareContainerDynamic.querySelector('#closeShareDynamic').addEventListener('click', () => {
    shareContainerDynamic.querySelector('#shareCodeAreaDynamic').style.display = 'none';
});

shareContainerDynamic.querySelector('#closeLoadDynamic').addEventListener('click', () => {
    shareContainerDynamic.querySelector('#loadCodeAreaDynamic').style.display = 'none';
});

// Hide All button
shareContainerDynamic.querySelector('#hideAllAreasDynamic').addEventListener('click', hideAllAreasDynamic);

// Debug button
shareContainerDynamic.querySelector('#debugConfigDynamic').addEventListener('click', () => {
    const debugInfo = shareContainerDynamic.querySelector('#debugInfoDynamic');
    const debugText = shareContainerDynamic.querySelector('#debugTextDynamic');
    
    const info = {
        'window.relationshipConfigDynamic exists': !!window.relationshipConfigDynamic,
        'Config content': window.relationshipConfigDynamic ? 'Available' : 'Missing'
    };
    
    if (window.relationshipConfigDynamic) {
        info['Config active types'] = window.relationshipConfigDynamic.active;
        info['Config display types'] = Object.keys(window.relationshipConfigDynamic.display);
        info['Sample emoji icons'] = Object.values(window.relationshipConfigDynamic.display).map(d => d.icon).slice(0, 5);
        
        // Test JSON.stringify
        try {
            const jsonString = JSON.stringify(window.relationshipConfigDynamic);
            info['JSON stringify test'] = `SUCCESS (${jsonString.length} chars)`;
            
            // Test UTF-8 encoding
            try {
                const encoded = utf8ToBase64(jsonString);
                info['UTF-8 Base64 encoding test'] = `SUCCESS (${encoded.length} chars)`;
                
                // Test round trip
                try {
                    const decoded = base64ToUtf8(encoded);
                    const parsed = JSON.parse(decoded);
                    info['Round trip test'] = 'SUCCESS';
                } catch (roundTripError) {
                    info['Round trip test'] = `ERROR: ${roundTripError.message}`;
                }
            } catch (encodeError) {
                info['UTF-8 Base64 encoding test'] = `ERROR: ${encodeError.message}`;
            }
        } catch (stringifyError) {
            info['JSON stringify test'] = `ERROR: ${stringifyError.message}`;
        }
    }
    
    debugText.textContent = JSON.stringify(info, null, 2);
    debugInfo.style.display = 'block';
    
    // Hide other areas
    shareContainerDynamic.querySelector('#shareCodeAreaDynamic').style.display = 'none';
    shareContainerDynamic.querySelector('#loadCodeAreaDynamic').style.display = 'none';
});

// Generate share code
shareContainerDynamic.querySelector('#generateShareLinkDynamic').addEventListener('click', () => {
    console.log('Generate share code button clicked');
    
    try {
        if (!window.relationshipConfigDynamic) {
            alert('❌ No configuration available to share!\n\nThe configuration manager above needs to load first. Try:\n1. Refresh the page\n2. Use the configuration manager above\n3. Click "Debug Config" to see what\'s missing');
            return;
        }
        
        console.log('Config found, attempting to stringify...');
        
        let jsonString;
        try {
            jsonString = JSON.stringify(window.relationshipConfigDynamic);
            console.log('JSON stringify successful, length:', jsonString.length);
        } catch (stringifyError) {
            console.error('JSON stringify error:', stringifyError);
            alert(`❌ Error converting configuration to JSON:\n${stringifyError.message}`);
            return;
        }
        
        let compressed;
        try {
            compressed = utf8ToBase64(jsonString);
            console.log('UTF-8 Base64 encoding successful, compressed length:', compressed.length);
        } catch (encodeError) {
            console.error('UTF-8 encoding error:', encodeError);
            alert(`❌ Error encoding configuration:\n${encodeError.message}\n\nThis may be due to special characters in the configuration.`);
            return;
        }
        
        const shareCodeArea = shareContainerDynamic.querySelector('#shareCodeAreaDynamic');
        const shareCodeTextarea = shareContainerDynamic.querySelector('#shareCodeDynamic');
        
        if (!shareCodeArea || !shareCodeTextarea) {
            console.error('UI elements not found');
            alert('❌ Error: UI elements not found. Try refreshing the page.');
            return;
        }
        
        shareCodeTextarea.value = compressed;
        shareCodeArea.style.display = 'block';
        
        // Hide other areas
        shareContainerDynamic.querySelector('#loadCodeAreaDynamic').style.display = 'none';
        shareContainerDynamic.querySelector('#debugInfoDynamic').style.display = 'none';
        
        console.log('Share code generated successfully');
        
        // Visual feedback
        const button = shareContainerDynamic.querySelector('#generateShareLinkDynamic');
        const originalText = button.textContent;
        const originalColor = button.style.backgroundColor;
        
        button.textContent = '✅ Generated!';
        button.style.backgroundColor = '#28a745';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = originalColor;
        }, 2000);
        
    } catch (error) {
        console.error('Unexpected error in generate share code:', error);
        alert(`❌ Unexpected error:\n${error.message}\n\nCheck browser console for details.`);
    }
});

// Show load interface
shareContainerDynamic.querySelector('#loadFromCodeDynamic').addEventListener('click', () => {
    const loadCodeArea = shareContainerDynamic.querySelector('#loadCodeAreaDynamic');
    
    loadCodeArea.style.display = 'block';
    
    // Hide other areas
    shareContainerDynamic.querySelector('#shareCodeAreaDynamic').style.display = 'none';
    shareContainerDynamic.querySelector('#debugInfoDynamic').style.display = 'none';
});

// Apply loaded configuration
shareContainerDynamic.querySelector('#applyCodeDynamic').addEventListener('click', async () => {
    const code = shareContainerDynamic.querySelector('#loadCodeDynamic').value.trim();
    
    if (!code) {
        alert('⚠️ Please paste a share code first!');
        return;
    }
    
    try {
        console.log('Attempting to decode share code...');
        
        let decodedJson;
        try {
            decodedJson = base64ToUtf8(code);
        } catch (decodeError) {
            console.error('UTF-8 decode error:', decodeError);
            alert('❌ Invalid share code format! The code appears to be corrupted or from an incompatible version.');
            return;
        }
        
        let config;
        try {
            config = JSON.parse(decodedJson);
        } catch (parseError) {
            console.error('JSON parse error:', parseError);
            alert('❌ Invalid configuration data! The share code contains invalid JSON.');
            return;
        }
        
        if (!config.active || !config.display) {
            alert('❌ Invalid configuration! Missing required properties (active, display).');
            return;
        }
        
        window.relationshipConfigDynamic = {
            ...config,
            version: Date.now()
        };
        
        if (window.factionDataUnified) {
            delete window.factionDataUnified;
        }
        
        console.log('Configuration loaded successfully:', config);
        
        try {
            const currentFile = app.workspace.getActiveFile();
            if (currentFile) {
                await app.fileManager.processFrontMatter(currentFile, (frontmatter) => {
                    frontmatter.relationshipConfig = config;
                });
            }
        } catch (persistError) {
            console.warn('Could not persist to YAML:', persistError);
        }
        
        alert('✅ Configuration loaded successfully!\n\nRefresh the page to see the changes applied.');
        
    } catch (error) {
        console.error('Error applying configuration:', error);
        alert(`❌ Error applying configuration:\n${error.message}`);
    }
});

dv.paragraph("**💡 Tips**: Click any area's ✕ close button or use 'Hide All' to clean up the interface. This version supports Unicode characters (emojis) in relationship configurations.");
```

# Registered Factions
```dataviewjs
// A. Unified Data Collection Functions with ALL function definitions
function getAllFactionsWithDynamicConfigUnified() {
    const config = window.relationshipConfigDynamic || {
        active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners']
    };
    
    return dv.pages().where(p => {
        if (p.file.name === "1. Faction database" || 
            p.file.name === "Faction Dashboard" ||
            p.file.path.includes("1. Faction database")) {
            return false;
        }
        
        // FIXED: Use active types directly for detection
        return config.active.some(relType => p[relType] !== undefined);
    });
}

function extractDynamicRelationshipsUnified(factions) {
    const config = window.relationshipConfigDynamic || {
        active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners']
    };
    
    let allRelationshipsDynamic = {};
    
    // Create name mapping
    let nameMappingDynamic = {};
    for (let faction of factions) {
        let actualName = faction.file.name;
        let variations = [
            actualName.toLowerCase(),
            actualName.toLowerCase().replace(/^the /, ''),
            actualName.toLowerCase().replace(/^a /, ''),
            actualName.toLowerCase().replace(/^an /, ''),
            actualName.toLowerCase().replace(/ the$/, ''),
            actualName.toLowerCase().replace(/'/g, '').replace(/'/g, ''),
            actualName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim()
        ];
        
        for (let variation of variations) {
            nameMappingDynamic[variation] = actualName;
        }
        nameMappingDynamic[actualName] = actualName;
    }
    
    function normalizeRelationshipArrayDynamic(arr) {
        if (!arr) return [];
        if (typeof arr === 'string') arr = [arr];
        if (!Array.isArray(arr)) return [];
        
        return arr.map(relationshipName => {
            if (typeof relationshipName !== 'string') {
                return String(relationshipName);
            }
            
            let testNames = [
                relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/^the /, ''),
                relationshipName.toLowerCase().replace(/^a /, ''),
                relationshipName.toLowerCase().replace(/^an /, ''),
                "the " + relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/'/g, '').replace(/'/g, ''),
                relationshipName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim()
            ];
            
            for (let testName of testNames) {
                if (nameMappingDynamic[testName]) {
                    return nameMappingDynamic[testName];
                }
            }
            
            return relationshipName;
        });
    }
    
    for (let faction of factions) {
        let name = faction.file.name;
        
        // Initialize with empty arrays for all active relationship types
        allRelationshipsDynamic[name] = {};
        // FIXED: Use active types directly
        config.active.forEach(relType => {
            allRelationshipsDynamic[name][relType] = normalizeRelationshipArrayDynamic(faction[relType]);
        });
    }
    
    return allRelationshipsDynamic;
}

function getAllFactionsUnified() {
    // Use dynamic config if available, otherwise fall back to static
    if (window.relationshipConfigDynamic) {
        return getAllFactionsWithDynamicConfigUnified();
    }
    
    // Fallback static version
    return dv.pages().where(p => {
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

function extractRelationshipsUnified(factions) {
    // Use dynamic config if available
    if (window.relationshipConfigDynamic) {
        return extractDynamicRelationshipsUnified(factions);
    }
    
    // Fallback static version
    let allRelationshipsStatic = {};
    
    // Create name mapping
    let nameMappingStatic = {};
    for (let faction of factions) {
        let actualName = faction.file.name;
        let variations = [
            actualName.toLowerCase(),
            actualName.toLowerCase().replace(/^the /, ''),
            actualName.toLowerCase().replace(/^a /, ''),
            actualName.toLowerCase().replace(/^an /, ''),
            actualName.toLowerCase().replace(/ the$/, ''),
            actualName.toLowerCase().replace(/'/g, '').replace(/'/g, ''),
            actualName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim()
        ];
        
        for (let variation of variations) {
            nameMappingStatic[variation] = actualName;
        }
        nameMappingStatic[actualName] = actualName;
    }
    
    function normalizeRelationshipArrayStatic(arr) {
        if (!arr) return [];
        if (typeof arr === 'string') arr = [arr];
        if (!Array.isArray(arr)) return []; // FIXED: Added missing closing parenthesis
        
        return arr.map(relationshipName => {
            if (typeof relationshipName !== 'string') {
                return String(relationshipName);
            }
            
            let testNames = [
                relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/^the /, ''),
                relationshipName.toLowerCase().replace(/^a /, ''),
                relationshipName.toLowerCase().replace(/^an /, ''),
                "the " + relationshipName.toLowerCase(),
                relationshipName.toLowerCase().replace(/'/g, '').replace(/'/g, ''),
                relationshipName.toLowerCase().replace(/[^a-zA-ZæøåÆØÅ\s]/g, '').trim()
            ];
            
            for (let testName of testNames) {
                if (nameMappingStatic[testName]) {
                    return nameMappingStatic[testName];
                }
            }
            
            return relationshipName;
        });
    }
    
    for (let faction of factions) {
        let name = faction.file.name;
        
        allRelationshipsStatic[name] = {
            allies: normalizeRelationshipArrayStatic(faction.allies),
            enemies: normalizeRelationshipArrayStatic(faction.enemies),
            rivals: normalizeRelationshipArrayStatic(faction.rivals),
            vassals: normalizeRelationshipArrayStatic(faction.vassals),
            patrons: normalizeRelationshipArrayStatic(faction.patrons),
            trading_partners: normalizeRelationshipArrayStatic(faction.trading_partners),
            infiltrated_by: normalizeRelationshipArrayStatic(faction.infiltrated_by),
            competing_with: normalizeRelationshipArrayStatic(faction.competing_with),
            neutral_toward: normalizeRelationshipArrayStatic(faction.neutral_toward)
        };
    }
    
    return allRelationshipsStatic;
}

function buildRelationshipMatrixDynamic(relationships) {
    let matrixUnified = {};
    
    // Initialize matrix
    for (let faction in relationships) {
        matrixUnified[faction] = {};
        for (let otherFaction in relationships) {
            if (faction !== otherFaction) {
                matrixUnified[faction][otherFaction] = [];
            }
        }
    }
    
    // Fill matrix with relationships
    for (let faction in relationships) {
        for (let relType in relationships[faction]) {
            for (let target of relationships[faction][relType]) {
                if (matrixUnified[faction] && matrixUnified[faction][target]) {
                    matrixUnified[faction][target].push(relType);
                }
            }
        }
    }
    
    return matrixUnified;
}

function detectConflictsDynamic(matrix) {
    let conflictsUnified = [];
    
    for (let factionA in matrix) {
        for (let factionB in matrix[factionA]) {
            let AtoB = matrix[factionA][factionB];
            let BtoA = matrix[factionB] ? matrix[factionB][factionA] : [];
            
            // Check for conflicting relationships
            if (AtoB.includes('allies') && BtoA.includes('enemies')) {
                conflictsUnified.push(`${factionA} considers ${factionB} an ally, but ${factionB} considers ${factionA} an enemy`);
            }
            if (AtoB.includes('enemies') && BtoA.includes('allies')) {
                conflictsUnified.push(`${factionA} considers ${factionB} an enemy, but ${factionB} considers ${factionA} an ally`);
            }
            if (AtoB.includes('patrons') && !BtoA.includes('vassals')) {
                conflictsUnified.push(`${factionA} serves ${factionB} as patron, but ${factionB} doesn't list ${factionA} as vassal`);
            }
            if (AtoB.includes('vassals') && !BtoA.includes('patrons')) {
                conflictsUnified.push(`${factionA} lists ${factionB} as vassal, but ${factionB} doesn't serve ${factionA} as patron`);
            }
        }
    }
    
    return conflictsUnified;
}

// NEW CODE WITH VERSION CHECKING:
// Check if we need to rebuild data based on configuration version
const lastKnownVersion = window.factionDataVersion || 0;
const currentVersion = window.relationshipConfigDynamic?.version || 0;

let factionsUnified, relationshipsUnified, matrixUnified, conflictsUnified;

if (!window.factionDataUnified || currentVersion > lastKnownVersion) {
    console.log('Rebuilding faction data, version:', currentVersion);
    
    // Rebuild data
    factionsUnified = getAllFactionsUnified();
    relationshipsUnified = extractRelationshipsUnified(factionsUnified);
    matrixUnified = buildRelationshipMatrixDynamic(relationshipsUnified);
    conflictsUnified = detectConflictsDynamic(matrixUnified);
    
    // Store unified data with version tracking
    window.factionDataUnified = {
        factions: factionsUnified,
        relationships: relationshipsUnified,
        matrix: matrixUnified,
        conflicts: conflictsUnified,
        usingDynamicConfig: !!window.relationshipConfigDynamic
    };
    
    window.factionDataVersion = currentVersion;
} else {
    console.log('Using cached faction data, version:', lastKnownVersion);
    
    // Use cached data
    const cached = window.factionDataUnified;
    factionsUnified = cached.factions;
    relationshipsUnified = cached.relationships;
    matrixUnified = cached.matrix;
    conflictsUnified = cached.conflicts;
} //end of revised versioning code 

// Store unified data - prioritize dynamic if available
window.factionDataUnified = {
    factions: factionsUnified,
    relationships: relationshipsUnified,
    matrix: matrixUnified,
    conflicts: conflictsUnified,
    usingDynamicConfig: !!window.relationshipConfigDynamic
};

// Display Faction Registry
dv.header(2, "📊 Faction Registry");

const configStatusUnified = window.relationshipConfigDynamic ? 
    `🔄 **Dynamic Configuration Active** (${window.relationshipConfigDynamic.active.length} relationship types)` : 
    `📋 **Static Configuration** (9 default relationship types)`;

dv.paragraph(`**Total Factions Tracked**: ${Object.keys(relationshipsUnified).length} | ${configStatusUnified}`);

// Create faction summary table with dynamic relationship types
let factionSummaryUnified = [];
const activeRelTypes = window.relationshipConfigDynamic ? 
    window.relationshipConfigDynamic.active : 
    ['allies', 'enemies', 'rivals', 'vassals', 'patrons', 'trading_partners', 'infiltrated_by', 'competing_with', 'neutral_toward'];

for (let faction in relationshipsUnified) {
    let totalRelationships = 0;
    let relationshipTypesArray = [];
    
    for (let relType of activeRelTypes) {
        const relArray = relationshipsUnified[faction][relType] || [];
        if (relArray.length > 0) {
            totalRelationships += relArray.length;
            const displayInfo = window.relationshipConfigDynamic?.display[relType] || { icon: "❓" };
            relationshipTypesArray.push(`${displayInfo.icon} ${relType}: ${relArray.length}`);
        }
    }
    
    factionSummaryUnified.push([
        `[[${faction}]]`,
        totalRelationships,
        relationshipTypesArray.join(", ") || "None"
    ]);
}

// Sort by total relationships (most connected first)
factionSummaryUnified.sort((a, b) => b[1] - a[1]);

dv.table(["Faction", "Total Relationships", "Breakdown"], factionSummaryUnified);

// Dynamic relationship summary with configuration awareness
if (window.factionDataUnified) {
    //dv.header(3, "📋 Relationship Overview");
    
    const relationshipsData = window.factionDataUnified.relationships;
    const factionCountData = Object.keys(relationshipsData).length;
    const activeRelTypesData = window.relationshipConfigDynamic ? 
        window.relationshipConfigDynamic.active : 
        ['allies', 'enemies', 'rivals', 'vassals', 'patrons', 'trading_partners', 'infiltrated_by', 'competing_with', 'neutral_toward'];
    
    // Dynamic counts based on active configuration
    let countsData = {};
    activeRelTypesData.forEach(relType => {
        countsData[relType] = 0;
    });
    
    // Count factions with relationships
    let factionsWithRelationships = 0;
    
    // Simple count loop - much faster
    for (let faction in relationshipsData) {
        let factionHasRelationships = false;
        for (let relType of activeRelTypesData) {
            const relArray = relationshipsData[faction][relType] || [];
            countsData[relType] += relArray.length;
            if (relArray.length > 0) {
                factionHasRelationships = true;
            }
        }
        if (factionHasRelationships) {
            factionsWithRelationships++;
        }
    }
    // this block of code displays the counted relationships in a bullet list. 
    // It is commented out to take up less realestate by instead displaying on a single line.
    // Display counts with dynamic icons
    //dv.paragraph("**Relationship Type Counts:**");
    //const countsList = [];
    //for (let relType of activeRelTypesData) {
    //    const displayInfo = window.relationshipConfigDynamic?.display[relType] || { icon: "❓" };
    //    const formattedType = relType.split('_').map(word => 
    //        word.charAt(0).toUpperCase() + word.slice(1)
    //    ).join(' ');
    //    countsList.push(`${displayInfo.icon} **${formattedType}**: ${countsData[relType]}`);
    // }
    //dv.list(countsList);
    
    // Display counts with dynamic icons on a single line
    // dv.paragraph("**Relationship Type Counts:**");
   	const countsList = [];
    for (let relType of activeRelTypesData) {
        const displayInfo = window.relationshipConfigDynamic?.display[relType] || { icon: "❓" };
        const formattedType = relType.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        countsList.push(`${displayInfo.icon} **${formattedType}**: ${countsData[relType]}`);
    }
    dv.paragraph(countsList.join(" | "));
    
    const totalRelationships = Object.values(countsData).reduce((a, b) => a + b, 0);
    dv.paragraph(`**Total Relationships**: ${totalRelationships} (across ${factionsWithRelationships} factions)`);
    
} else {
    dv.paragraph("⏳ Loading faction data...");
}
// Display conflicts
if (conflictsUnified.length > 0) {
    dv.header(2, "⚠️ Relationship Conflicts Detected");
    for (let conflict of conflictsUnified) {
        dv.paragraph(`- ${conflict}`);
    }
} else {
    dv.paragraph("✅ **No relationship conflicts detected**");
}
```

```dataviewjs

```


# Static Faction Relationship Map
```dataviewjs
// Enhanced Visualization Generator with dynamic relationship type support
function generateNetworkDiagramDynamic(relationships) {
    let mermaidCode = "```mermaid\nflowchart LR\n";
    
    // Get active relationship types from config
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
    let allFactionNamesDynamic = new Set();
    
    // Add existing factions
    for (let faction in relationships) {
        allFactionNamesDynamic.add(faction);
    }
    
    // Add all target factions (even if they don't have their own notes)
    for (let faction in relationships) {
        for (let relType of config.active) {
            const relArray = relationships[faction][relType] || [];
            for (let target of relArray) {
                allFactionNamesDynamic.add(target);
            }
        }
    }
    
    // Create nodes for ALL factions
    let nodeIndexDynamic = 0;
    let nodeMapDynamic = {};

    for (let faction of allFactionNamesDynamic) {
        let nodeId = `F${nodeIndexDynamic}`;
        let cleanName = sanitizeText(faction);
        nodeMapDynamic[faction] = nodeId;
        
        // All factions should be clickable links, but with different styling
        // if (relationships[faction]) {
            // Faction has its own note - primary styling
        //    mermaidCode += `${nodeId}["${cleanName}"]:::internal-link\n`;
        // } else {
            // Faction mentioned but no note exists - mentioned styling (also clickable)
        //    mermaidCode += `${nodeId}["${cleanName}"]:::mentioned-link\n`;
        //}
        //nodeIndexDynamic++;
	//FIXED mermaid boxes to pills to avoid text truncation
if (relationships[faction]) {
    mermaidCode += `${nodeId}{{${cleanName}}}:::internal-link\n`;
} else {
    mermaidCode += `${nodeId}["${cleanName}"]:::mentioned-link\n`;
}

    
	    nodeIndexDynamic++;
    }
    
    // Generate relationship arrows based on display configuration
    function generateRelationshipArrow(relType, sourceNode, targetNode, displayConfig) {
        const icon = displayConfig.icon || "❓";
        const label = `|${icon} ${relType}|`;
        
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
    
    // Add ALL relationships dynamically based on active config
    for (let faction in relationships) {
        let sourceNode = nodeMapDynamic[faction];
        
        for (let relType of config.active) {
            const relArray = relationships[faction][relType] || [];
            const displayConfig = config.display[relType] || { 
                icon: "❓", 
                color: "gray", 
                style: "solid", 
                bidirectional: false 
            };
            
            for (let target of relArray) {
                if (nodeMapDynamic[target]) {
                    mermaidCode += generateRelationshipArrow(relType, sourceNode, nodeMapDynamic[target], displayConfig);
                }
            }
        }
    }
    
    // Add styling - both types should be clickable
    //mermaidCode += `classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:2px;\n`;
    //mermaidCode += `classDef mentioned-link fill:#FFE6E6,stroke:#FF6B6B,stroke-width:1px,stroke-dasharray: 5 5;\n`;
    mermaidCode += `classDef internal-link fill:#E6F3FF,stroke:#4a90e2,stroke-width:2px;\n`;
    mermaidCode += `classDef mentioned-link fill:#FFE6E6,stroke:#FF6B6B,stroke-width:1px,stroke-dasharray: 5 5;\n`;
    
    mermaidCode += "```";
    
    return mermaidCode;
}

// Generate and display network
if (window.factionDataUnified) {
    const relationshipsDisplay = window.factionDataUnified.relationships;
    let totalConnectionsDisplay = 0;
    const activeRelTypesDisplay = window.relationshipConfigDynamic ? 
        window.relationshipConfigDynamic.active : 
        ['allies', 'enemies', 'rivals', 'vassals', 'patrons', 'trading_partners', 'infiltrated_by', 'competing_with', 'neutral_toward'];
    
    for (let faction in relationshipsDisplay) {
        for (let relType of activeRelTypesDisplay) {
            const relArray = relationshipsDisplay[faction][relType] || [];
            totalConnectionsDisplay += relArray.length;
        }
    }
    
    const configStatus = window.factionDataUnified.usingDynamicConfig ? "Dynamic Config" : "Static Config";
    dv.paragraph(`**${configStatus}**: Displaying ${Object.keys(relationshipsDisplay).length} factions with ${totalConnectionsDisplay} total relationships`);
    
    const networkDiagramDynamic = generateNetworkDiagramDynamic(relationshipsDisplay);
    dv.paragraph(networkDiagramDynamic);
} else {
    dv.paragraph("⏳ Loading faction data...");
}
```

--- 
#
> [!bug]-  # Debug: Faction Relationship Checker
> 
> ```dataviewjs
> // Interactive Debug Section - User Input
> 
> // Create input field and button
> const container = dv.container;
> container.innerHTML = `
> <div style="margin: 10px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
>     <label for="factionInput" style="display: block; margin-bottom: 5px; font-weight: bold;">Enter Faction Name to Debug:</label>
>     <input type="text" id="factionInput" placeholder="e.g., The Ruby Throne" style="width: 300px; padding: 5px; margin-right: 10px; border: 1px solid #ccc; border-radius: 3px;">
>     <button id="debugButton" style="padding: 5px 15px; background-color: var(--interactive-accent); color: white; border: none; border-radius: 3px; cursor: pointer;">Debug Faction</button>
>     <div id="debugResults" style="margin-top: 15px; padding: 10px; background-color: var(--background-primary); border-radius: 3px; display: none;"></div>
> </div>
> `;
> 
> // Add click handler
> const button = container.querySelector('#debugButton');
> const input = container.querySelector('#factionInput');
> const results = container.querySelector('#debugResults');
> 
> button.addEventListener('click', () => {
>     const factionName = input.value.trim();
>     if (!factionName) {
>         results.style.display = 'block';
>         results.innerHTML = '<p style="color: orange;">⚠️ Please enter a faction name</p>';
>         return;
>     }
>     
>     if (window.factionDataUnified) {
>         const relationships = window.factionDataUnified.relationships;
>         
>         // Try to find the faction with fuzzy matching
>         let foundFaction = null;
>         let exactMatch = false;
>         
>         // First try exact match
>         if (relationships[factionName]) {
>             foundFaction = factionName;
>             exactMatch = true;
>         } else {
>             // Try case-insensitive and "The" prefix variations
>             const searchVariations = [
>                 factionName.toLowerCase(),
>                 factionName.toLowerCase().replace(/^the /, ''),
>                 "the " + factionName.toLowerCase(),
>                 factionName.toLowerCase().replace(/^a /, ''),
>                 factionName.toLowerCase().replace(/^an /, '')
>             ];
>             
>             for (let faction in relationships) {
>                 const factionLower = faction.toLowerCase();
>                 if (searchVariations.includes(factionLower)) {
>                     foundFaction = faction;
>                     break;
>                 }
>             }
>         }
>         
>         results.style.display = 'block';
>         
>         if (foundFaction) {
>             const factionData = relationships[foundFaction];
>             
>             let html = `<h4>✅ Found: ${foundFaction}${exactMatch ? ' (exact match)' : ' (fuzzy match)'}</h4>`;
>             
>             // Show relationships found
>             html += '<p><strong>Relationships found:</strong></p><ul>';
>             let hasRelationships = false;
>             for (let relType in factionData) {
>                 if (factionData[relType].length > 0) {
>                     hasRelationships = true;
>                     html += `<li><strong>${relType}:</strong> ${factionData[relType].join(", ")}</li>`;
>                 }
>             }
>             if (!hasRelationships) {
>                 html += '<li style="color: orange;">No relationships defined</li>';
>             }
>             html += '</ul>';
>             
>             // Check if target factions exist
>             html += '<p><strong>Checking if target factions exist:</strong></p><ul>';
>             let allTargetsExist = true;
>             for (let relType in factionData) {
>                 for (let target of factionData[relType]) {
>                     if (relationships[target]) {
>                         html += `<li>✅ ${target} exists as faction</li>`;
>                     } else {
>                         html += `<li>❌ ${target} NOT found as faction</li>`;
>                         allTargetsExist = false;
>                     }
>                 }
>             }
>             if (allTargetsExist && hasRelationships) {
>                 html += '<li style="color: green;">✅ All target factions exist!</li>';
>             }
>             html += '</ul>';
>             
>             results.innerHTML = html;
>         } else {
>             let html = `<h4>❌ Faction "${factionName}" not found</h4>`;
>             html += '<p><strong>Available factions:</strong></p><ul>';
>             const sortedFactions = Object.keys(relationships).sort();
>             for (let faction of sortedFactions.slice(0, 10)) { // Show first 10 to avoid overwhelming
>                 html += `<li>${faction}</li>`;
>             }
>             if (sortedFactions.length > 10) {
>                 html += `<li><em>... and ${sortedFactions.length - 10} more</em></li>`;
>             }
>             html += '</ul>';
>             
>             results.innerHTML = html;
>         }
>     } else {
>         results.style.display = 'block';
>         results.innerHTML = '<p style="color: red;">❌ Faction data not loaded. Make sure the dashboard above has processed.</p>';
>     }
> });
> 
> // Allow Enter key to trigger debug
> input.addEventListener('keypress', (e) => {
>     if (e.key === 'Enter') {
>         button.click();
>     }
> });
> 
> dv.paragraph("Enter any faction name above to check its relationships and verify all target factions exist.");
> ```





# 🕸️ Interactive Faction Relationship Map

>💡 **How to use:** Select a faction using the radio buttons above, then click "Focus on Selected Faction" to update the two maps below.
> 	The system will always show a focused view.
## 🎯 Select Faction to Focus

```dataviewjs
// Dynamic Radio Button Generator for Faction Selection
dv.header(3, "📍 Choose Faction to Focus");

// Get all factions from the existing data
if (window.factionDataUnified) {
    // Get faction names from the actual files
    const factionPages = dv.pages().where(p => {
        if (p.file.name === "1. Faction database" || 
            p.file.name === "Faction Dashboard" ||
            p.file.path.includes("1. Faction database")) {
            return false;
        }
        
        // Check if it has any faction relationship arrays
        const config = window.relationshipConfigDynamic || {
            active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners']
        };
        
        return config.active.some(relType => p[relType] !== undefined);
    });
    
    // CHANGED: Filter to only include factions with relationships > 0
    const allFactions = factionPages.map(p => p.file.name);
    const factionsWithRelationships = allFactions.filter(faction => {
        const relationshipData = window.factionDataUnified.relationships[faction];
        if (!relationshipData) return false;
        
        // Count total relationships for this faction
        const config = window.relationshipConfigDynamic || {
            active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners']
        };
        
        const totalRelationships = config.active.reduce((count, relType) => {
            const relArray = relationshipData[relType] || [];
            return count + relArray.length;
        }, 0);
        
        return totalRelationships > 0;
    }).sort();
    
    const currentFilter = dv.current().factionFilter || "";
    
    // If no filter is set, set it to the first faction with relationships
    const defaultFaction = factionsWithRelationships[0] || "";
    let selectedFaction = currentFilter || defaultFaction;
    
    // CHANGED: If current filter has no relationships, reset to default
    if (currentFilter && !factionsWithRelationships.includes(currentFilter)) {
        selectedFaction = defaultFaction;
        
        // Update YAML to the new default
        const currentFile = app.workspace.getActiveFile();
        if (currentFile && defaultFaction) {
            app.fileManager.processFrontMatter(currentFile, (frontmatter) => {
                frontmatter.factionFilter = defaultFaction;
            });
        }
    }
    
    // Set default faction if none selected
    if (!currentFilter && defaultFaction) {
        const currentFile = app.workspace.getActiveFile();
        if (currentFile) {
            app.fileManager.processFrontMatter(currentFile, (frontmatter) => {
                frontmatter.factionFilter = defaultFaction;
            });
        }
    }
    
    // Create radio button container
    const radioContainer = dv.container;
    radioContainer.innerHTML = `
    <div style="margin: 15px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px; margin-bottom: 15px;" id="factionRadioGrid">
        </div>
        <div style="margin-top: 15px;">
            <button id="applyFactionSelection" style="padding: 8px 20px; background-color: var(--interactive-accent); color: white; border: none; border-radius: 3px; margin-right: 10px;">🎯 Focus on Selected Faction</button>
            <span id="currentSelection" style="font-weight: bold; color: var(--text-accent);">Current: ${selectedFaction}</span>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: var(--text-muted);">
            💡 Showing only factions with relationships (${factionsWithRelationships.length} of ${allFactions.length} total)
        </div>
    </div>
    `;
    
    const gridContainer = radioContainer.querySelector('#factionRadioGrid');
    let selectedRadio = selectedFaction;
    
    // Generate radio buttons only for factions with relationships
    factionsWithRelationships.forEach((faction, index) => {
        const isSelected = faction === selectedFaction;
        const radioId = `faction_${index}`;
        
        // Calculate relationship count (we know it's > 0)
        const relationshipData = window.factionDataUnified.relationships[faction];
        const config = window.relationshipConfigDynamic || {
            active: ['allies', 'enemies', 'rivals', 'patrons', 'vassals', 'trading_partners']
        };
        
        const relationshipCount = config.active.reduce((count, relType) => {
            const relArray = relationshipData[relType] || [];
            return count + relArray.length;
        }, 0);
        
        const radioItem = document.createElement('div');
        radioItem.style.cssText = 'display: flex; align-items: center; padding: 8px; border-radius: 3px; cursor: pointer; background: var(--background-primary);';
        
        radioItem.innerHTML = `
            <input type="radio" 
                   id="${radioId}" 
                   name="factionSelection" 
                   value="${faction}" 
                   ${isSelected ? 'checked' : ''}
                   style="margin-right: 8px;">
            <label for="${radioId}" 
                   style="cursor: pointer; font-size: 14px; flex: 1;"
                   title="File: ${faction} | ${relationshipCount} relationships">
                ${faction}
                <span style="font-size: 11px; color: var(--text-accent); margin-left: 5px; font-weight: bold;">(${relationshipCount})</span>
            </label>
        `;
        
        // Add click handler for the entire item
        radioItem.addEventListener('click', (e) => {
            if (e.target.type !== 'radio') {
                const radio = radioItem.querySelector('input[type="radio"]');
                radio.checked = true;
                selectedRadio = faction;
                
                // Update visual feedback
                document.querySelectorAll('#factionRadioGrid > div').forEach(item => {
                    item.style.backgroundColor = 'var(--background-primary)';
                });
                radioItem.style.backgroundColor = 'var(--background-modifier-border)';
                
                radioContainer.querySelector('#currentSelection').textContent = `Selected Faction: ${faction}`;
            }
        });
        
        // Add change handler for the radio button
        const radio = radioItem.querySelector('input[type="radio"]');
        radio.addEventListener('change', () => {
            if (radio.checked) {
                selectedRadio = faction;
                radioContainer.querySelector('#currentSelection').textContent = `Selected Faction: ${faction}`;
            }
        });
        
        // Set initial visual state
        if (isSelected) {
            radioItem.style.backgroundColor = 'var(--background-modifier-border)';
        }
        
        gridContainer.appendChild(radioItem);
    });
    
    // Apply selection button handler (unchanged)
    radioContainer.querySelector('#applyFactionSelection').addEventListener('click', async () => {
        const currentFile = app.workspace.getActiveFile();
        if (currentFile && selectedRadio) {
            try {
                await app.fileManager.processFrontMatter(currentFile, (frontmatter) => {
                    frontmatter.factionFilter = selectedRadio;
                });
                
                setTimeout(() => {
                    if (app.plugins.plugins.dataview) {
                        app.plugins.plugins.dataview.api.page.refreshCurrentView();
                    }
                }, 100);
                
                const button = radioContainer.querySelector('#applyFactionSelection');
                const originalText = button.textContent;
                button.textContent = '✅ Applied!';
                button.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.backgroundColor = 'var(--interactive-accent)';
                }, 1500);
                
            } catch (error) {
                console.error('Failed to update faction filter:', error);
                alert('Failed to update faction selection. Please try again.');
            }
        }
    });
    
    dv.paragraph(`**📊 Factions with Relationships**: ${factionsWithRelationships.length} | **🎯 Selected**: ${selectedFaction || 'None'}`);
    
// CHANGED: Enhanced excluded factions display with clickable links in callout
const factionsWithoutRelationships = allFactions.filter(f => !factionsWithRelationships.includes(f));
if (factionsWithoutRelationships.length > 0) {
    // Create callout-style container for excluded factions
    const excludedDiv = document.createElement('div');
    excludedDiv.style.cssText = `
        margin-top: 20px; 
        padding: 0;
        border: 1px solid var(--callout-border);
        border-radius: 8px;
        background-color: var(--callout-bg);
        border-left: 4px solid var(--callout-info);
    `;
    
    excludedDiv.innerHTML = `
        <div style="
            padding: 12px 16px 8px 16px;
            border-bottom: 1px solid var(--callout-border);
            background-color: var(--callout-title-bg);
            border-radius: 8px 8px 0 0;
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        " id="excludedCalloutHeader">
            <span style="
                margin-right: 8px;
                font-size: 16px;
                color: var(--callout-info);
            ">ℹ️</span>
            <span style="
                font-weight: 600;
                color: var(--callout-title-color);
                font-size: 14px;
                flex: 1;
            ">Excluded Factions</span>
            <span style="
                font-size: 11px;
                color: var(--text-muted);
                font-style: italic;
                margin-right: 8px;
            ">(${factionsWithoutRelationships.length} factions with no relationships)</span>
            <span id="excludedToggleIcon" style="
                color: var(--text-muted);
                font-size: 12px;
                transition: transform 0.2s ease;
            ">▼</span>
        </div>
        <div id="excludedCalloutContent" style="
            padding: 12px 16px;
            display: block;
        ">
            <div style="
                font-size: 11px; 
                font-style: italic; 
                color: var(--text-muted); 
                margin-bottom: 12px;
            ">
                Click faction names below to open and add relationships:
            </div>
            <div id="excludedFactionsList" style="
                display: flex; 
                flex-wrap: wrap; 
                gap: 8px; 
                align-items: center;
                margin-bottom: 12px;
            "></div>
            <div style="
                font-size: 9px; 
                font-style: italic; 
                color: var(--text-faint);
                padding-top: 8px;
                border-top: 1px solid var(--background-modifier-border);
            ">
                💡 <em>Add relationship arrays (allies, enemies, etc.) to faction frontmatter to include them in network maps</em>
            </div>
        </div>
    `;
    
    // Add toggle functionality to the callout header
    const header = excludedDiv.querySelector('#excludedCalloutHeader');
    const content = excludedDiv.querySelector('#excludedCalloutContent');
    const toggleIcon = excludedDiv.querySelector('#excludedToggleIcon');
    let isCollapsed = false;
    
    header.addEventListener('click', () => {
        isCollapsed = !isCollapsed;
        if (isCollapsed) {
            content.style.display = 'none';
            toggleIcon.textContent = '▶';
            toggleIcon.style.transform = 'rotate(0deg)';
        } else {
            content.style.display = 'block';
            toggleIcon.textContent = '▼';
            toggleIcon.style.transform = 'rotate(0deg)';
        }
    });
    
    // Add hover effect to header
    header.addEventListener('mouseenter', () => {
        header.style.backgroundColor = 'var(--background-modifier-hover)';
    });
    
    header.addEventListener('mouseleave', () => {
        header.style.backgroundColor = 'var(--callout-title-bg)';
    });
    
    const excludedList = excludedDiv.querySelector('#excludedFactionsList');
    
    // Create clickable links for each excluded faction
    factionsWithoutRelationships.forEach((faction, index) => {
        const factionLink = document.createElement('a');
        factionLink.href = `obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(faction)}`;
        factionLink.style.cssText = `
            font-size: 10px;
            font-style: italic;
            color: var(--text-muted);
            text-decoration: none;
            padding: 4px 8px;
            background-color: var(--background-modifier-border);
            border-radius: 12px;
            border: 1px solid var(--background-modifier-border-hover);
            transition: all 0.2s ease;
            cursor: pointer;
            white-space: nowrap;
        `;
        factionLink.textContent = faction;
        factionLink.title = `Click to open "${faction}" and add relationships`;
        
        // Enhanced hover effects
        factionLink.addEventListener('mouseenter', () => {
            factionLink.style.backgroundColor = 'var(--interactive-accent)';
            factionLink.style.color = 'white';
            factionLink.style.transform = 'translateY(-1px)';
            factionLink.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        });
        
        factionLink.addEventListener('mouseleave', () => {
            factionLink.style.backgroundColor = 'var(--background-modifier-border)';
            factionLink.style.color = 'var(--text-muted)';
            factionLink.style.transform = 'translateY(0)';
            factionLink.style.boxShadow = 'none';
        });
        
        // Add click handler for Obsidian navigation
        factionLink.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Use Obsidian's internal navigation
            const file = app.vault.getAbstractFileByPath(faction + '.md') || 
                       app.vault.getAbstractFileByPath(faction);
            
            if (file) {
                app.workspace.openLinkText(faction, '', true);
            } else {
                // Fallback to obsidian URI
                window.open(factionLink.href, '_blank');
            }
            
            // Visual feedback
            factionLink.style.backgroundColor = 'var(--color-green)';
            factionLink.style.color = 'white';
            setTimeout(() => {
                factionLink.style.backgroundColor = 'var(--background-modifier-border)';
                factionLink.style.color = 'var(--text-muted)';
            }, 200);
        });
        
        excludedList.appendChild(factionLink);
    });
    
    // Add the entire excluded section to the radio container
    radioContainer.appendChild(excludedDiv);
}
    } else {
    dv.paragraph("⏳ Loading factions... Please wait for the main dashboard to process.");
}
```

## Focused Network Maps
```dataviewjs
// Meta Bind + DataviewJS Filtered Faction Map with Dynamic Config Support
dv.header(2, "📊 Faction Network");

// Read the filter value from Meta Bind input
const filterValueDynamic = dv.current().factionFilter || "";

// Enhanced network diagram generator with filtering and dynamic config
function generateFilteredNetworkDiagramDynamic(relationships, filterFaction = null) {
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
    
    // Collect factions to include in the map
    let factionsToIncludeDynamic = new Set();
    
    if (actualFilterFaction) {
        // Add the main faction
        factionsToIncludeDynamic.add(actualFilterFaction);
        
        // Add all factions this faction has relationships with (based on active config)
        for (let relType of config.active) {
            const relArray = relationships[actualFilterFaction][relType] || [];
            for (let target of relArray) {
                factionsToIncludeDynamic.add(target);
            }
        }
        
        // Add all factions that have relationships with this faction
        for (let faction in relationships) {
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                if (relArray.includes(actualFilterFaction)) {
                    factionsToIncludeDynamic.add(faction);
                }
            }
        }
    } else {
        // Include all factions if no filter
        for (let faction in relationships) {
            factionsToIncludeDynamic.add(faction);
        }
        
        // Add all target factions (even if they don't have their own notes)
        for (let faction in relationships) {
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                for (let target of relArray) {
                    factionsToIncludeDynamic.add(target);
                }
            }
        }
    }
    
    // Create nodes for included factions
    let nodeIndexFilter = 0;
    let nodeMapFilter = {};
    
    for (let faction of factionsToIncludeDynamic) {
        let nodeId = `F${nodeIndexFilter}`;
        let cleanName = sanitizeText(faction);
        nodeMapFilter[faction] = nodeId;
        
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
            // Count relationships for tooltip (only active types)
            let relCount = 0;
            for (let relType of config.active) {
                const relArray = relationships[faction][relType] || [];
                relCount += relArray.length;
            }
            if (relCount > 0) {
                tooltipText += ` (${relCount} relationships)`;
            }
        } else {
            tooltipText += " (mentioned only)";
        }
        
        // Add click event and tooltip
        mermaidCode += `click ${nodeId} href "obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(faction)}" "${tooltipText}"\n`;
        
        nodeIndexFilter++;
    }
    
    // Generate relationship arrows dynamically
    function generateRelationshipArrowFilter(relType, sourceNode, targetNode, displayConfig) {
        const icon = displayConfig.icon || "❓";
        const label = `|${icon} ${relType}|`;
        
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
                    mermaidCode += generateRelationshipArrowFilter(relType, sourceNode, nodeMapFilter[target], displayConfig);
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
    const resultFilter = generateFilteredNetworkDiagramDynamic(relationshipsFilter, filterValueDynamic);
    
    // Display status
    const configType = window.factionDataUnified.usingDynamicConfig ? "Dynamic" : "Static";
    if (filterValueDynamic.trim()) {
        if (resultFilter.filterMatched) {
            dv.paragraph(`🎯 **Filtered View** (${configType}): Showing relationships for "${resultFilter.filterMatched}" (${resultFilter.factionCount} factions)`);
        } else {
            dv.paragraph(`⚠️ **Filter Not Found**: "${filterValueDynamic}" not found - showing all factions instead (${resultFilter.factionCount} total)`);
        }
    } else {
        dv.paragraph(`🌐 **Full Network** (${configType}): Showing all factions (${resultFilter.factionCount} total)`);
    }
    
    // Display the map
    dv.paragraph(resultFilter.code);
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```

```dataviewjs
// Dynamic Faction Mindmap Generator with Configuration Support
dv.header(2, "🕸️ Mindmap focus: `=this.factionfilter`");

// Read the filter value from YAML frontmatter
const filterValueMindmap = dv.current().factionFilter || "";

// Mindmap generator for focused faction view with dynamic config support
function generateFactionMindmapDynamic(relationships, targetFaction) {
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
    
    // Collect all relationships - both outgoing AND incoming based on active config
    let allRelationshipsMindmap = {};
    config.active.forEach(relType => {
        allRelationshipsMindmap[relType] = new Set(factionData[relType] || []);
    });
    
    // Add incoming relationships (other factions that mention this faction)
    for (let otherFaction in relationships) {
        if (otherFaction === actualFaction) continue;
        
        const otherData = relationships[otherFaction];
        
        for (let relType of config.active) {
            const relArray = otherData[relType] || [];
            if (relArray.includes(actualFaction)) {
                // Handle reciprocal relationships
                if (relType === 'allies' || relType === 'rivals' || relType === 'trading_partners' || relType === 'competing_with') {
                    // Bidirectional relationships
                    allRelationshipsMindmap[relType].add(otherFaction);
                } else if (relType === 'patrons') {
                    // If they list us as patron, we should show them as vassal
                    if (allRelationshipsMindmap['vassals']) {
                        allRelationshipsMindmap['vassals'].add(otherFaction);
                    }
                } else if (relType === 'vassals') {
                    // If they list us as vassal, we should show them as patron
                    if (allRelationshipsMindmap['patrons']) {
                        allRelationshipsMindmap['patrons'].add(otherFaction);
                    }
                } else {
                    // For other relationships, add them as the same type
                    allRelationshipsMindmap[relType].add(otherFaction);
                }
            }
        }
    }
    
    // Add each relationship type as a branch (only active types)
    for (let relType of config.active) {
        if (allRelationshipsMindmap[relType] && allRelationshipsMindmap[relType].size > 0) {
            hasRelationships = true;
            const displayInfo = config.display[relType] || { icon: "❓" };
            const formattedType = relType.split('_').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
            
            mermaidCode += `    ${displayInfo.icon} ${formattedType}\n`;
            for (let target of Array.from(allRelationshipsMindmap[relType]).sort()) {
                mermaidCode += `      ${sanitizeForMindmap(target)}\n`;
            }
        }
    }
    
    if (!hasRelationships) {
        mermaidCode += `    📝 No Relationships\n`;
        mermaidCode += `      Define relationships in faction YAML\n`;
    }
    
    mermaidCode += "```";
    
    // Calculate total relationships
    const relationshipCount = Object.values(allRelationshipsMindmap).reduce((total, set) => total + set.size, 0);
    
    return {
        code: mermaidCode,
        filterMatched: actualFaction,
        type: "mindmap",
        relationshipCount: relationshipCount
    };
}

// Main execution
if (window.factionDataUnified) {
    const relationshipsMindmap = window.factionDataUnified.relationships;
    const configTypeMindmap = window.factionDataUnified.usingDynamicConfig ? "Dynamic Config" : "Static Config";
    
    if (filterValueMindmap.trim()) {
        // Generate mindmap for specific faction
        const resultMindmap = generateFactionMindmapDynamic(relationshipsMindmap, filterValueMindmap);
        
        if (resultMindmap.filterMatched) {
            dv.paragraph(`🎯 **"${resultMindmap.filterMatched}"** (${configTypeMindmap}) - ${resultMindmap.relationshipCount} total relationships`);
            dv.paragraph(resultMindmap.code);
        } else {
            dv.paragraph(`⚠️ **Faction Not Found**: "${filterValueMindmap}"`);
            dv.paragraph("**Available factions:**");
            
            // Show available factions as help
            const availableFactionsMindmap = Object.keys(relationshipsMindmap).sort();
            for (let faction of availableFactionsMindmap) {
                dv.paragraph(`- ${faction}`);
            }
        }
    } else {
        dv.paragraph(`💡 **Set faction name** in the filter above to generate mindmap (${configTypeMindmap})`);
        dv.paragraph("**Available factions:**");
        
        // Show available factions as help  
        const availableFactionsMindmap = Object.keys(relationshipsMindmap).sort();
        for (let faction of availableFactionsMindmap.slice(0, 20)) {
            dv.paragraph(`- ${faction}`);
        }
        if (availableFactionsMindmap.length > 20) {
            dv.paragraph(`*... and ${availableFactionsMindmap.length - 20} more*`);
        }
    }
    
} else {
    dv.paragraph("⏳ Loading faction data... Make sure the main dashboard has run first.");
}
```

## 🗺️ Dynamic Relationship Legend

```dataviewjs
// Dynamic Legend Generator
dv.header(3, "🗺️ Relationship Legend");

if (window.relationshipConfigDynamic) {
    const config = window.relationshipConfigDynamic;
    
    let legendItems = [];
    for (let relType of config.active) {
        const displayInfo = config.display[relType] || { icon: "❓", color: "gray" };
        const formattedType = relType.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        
        legendItems.push(`${displayInfo.icon} **${formattedType}**`);
    }
    
    // Display in rows of 5
    let legendText = "";
    for (let i = 0; i < legendItems.length; i += 5) {
        const row = legendItems.slice(i, i + 5);
        legendText += row.join(" | ") + "  \n";
    }
    
    dv.paragraph(legendText);
    
    dv.paragraph(`**Configuration**: ${config.active.length} active relationship types | ${config.core.length + config.extended.length + config.custom.length} total available`);
} else {
    // Fallback static legend
    dv.paragraph("🤝 **Allies** | ⚔️ **Enemies** | 🥊 **Rivals** | ⬆️ **Patrons** | ⬇️ **Vassals**  ");
    dv.paragraph("💰 **Trading Partners** | 🕵️ **Espionage Relations** | 🏆 **Competing With** | 😐 **Neutral Relations**");
    dv.paragraph("**Configuration**: Static (9 default relationship types)");
}
```

---

# 📝 How to Use This Dynamic Relationship Viewer

1. **Configure relationships** using the Configuration Manager at the top
2. **Add custom relationship types** for your specific campaign needs  
3. **Filter by faction** using the input field above the network diagram
4. **Generate mindmaps** by setting the factionFilter and refreshing
5. **Export/Import configs** to share with other GMs
6. **Debug relationships** using the relationship checker tool

The system automatically detects whether you're using dynamic configuration and adapts all visualizations accordingly. All relationship types, icons, and connection styles respect your configuration settings.


# Optional Graph view
```dataviewjs
// Graph View Integration Section for Faction Dashboard
// Create interactive controls for graph view
const graphContainer = dv.container;
graphContainer.innerHTML = `
<div style="margin: 10px 0; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background-color: var(--background-secondary);">
    
    
    <div style="display: grid; grid-template-columns: 1fr; gap: 15px; margin-bottom: 15px;">
        <div>
            <h4>🎯 Faction Navigation</h4>
            <select id="factionSelector" style="width: 100%; padding: 6px; margin: 3px 0; border: 1px solid var(--background-modifier-border); border-radius: 3px; background-color: var(--background-primary); color: var(--text-normal);">
                <option value="">Select a faction...</option>
            </select>
            <button id="openFactionGraph" style="width: 100%; padding: 8px; margin: 3px 0; background-color: #fd7e14; color: white; border: none; border-radius: 3px; cursor: pointer;">Open Note + Local Graph Split</button>
        </div>
    </div>
</div>
`;

// Add functionality to buttons
const factionSelector = graphContainer.querySelector('#factionSelector');
const openFactionGraphBtn = graphContainer.querySelector('#openFactionGraph');

// Open note + local graph in split view for selected faction
openFactionGraphBtn.addEventListener('click', () => {
    const selectedFaction = factionSelector.value;
    if (selectedFaction) {
        // Split the workspace to the right
        app.workspace.getLeaf('split', 'vertical').openFile(
            app.vault.getAbstractFileByPath(selectedFaction + '.md') || 
            app.metadataCache.getFirstLinkpathDest(selectedFaction, '')
        ).then(() => {
            // Small delay to ensure the file opens, then open local graph in the original pane
            setTimeout(() => {
                app.commands.executeCommandById('graph:open-local');
            }, 200);
        }).catch(() => {
            // Fallback: just open the file normally then graph
            app.workspace.openLinkText(selectedFaction, '', false).then(() => {
                setTimeout(() => {
                    app.commands.executeCommandById('graph:open-local');
                }, 100);
            });
        });
        new Notice('Opening ' + selectedFaction + ' with local graph split view', 2000);
    } else {
        new Notice('Please select a faction first', 3000);
    }
});

// Populate faction selector
if (window.factionDataUnified) {
    const factionNames = Object.keys(window.factionDataUnified.relationships).sort();
    
    // Populate dropdown
    factionNames.forEach(faction => {
        const option = document.createElement('option');
        option.value = faction;
        option.textContent = faction;
        factionSelector.appendChild(option);
    });
}
```