// Persona accent colors
const PERSONA_COLORS = {
    professor: 'var(--accent-purple)',
    student: 'var(--accent-blue)',
    'pro-se': 'var(--accent-yellow)',
    cle: 'var(--accent-green)',
};

// DOM elements
const filtersContainer = document.querySelector('.filters');
const personasContainer = document.getElementById('personas-container');

// State
let allData = null;
let activeFilter = 'all';
let skillsWithTraces = new Set();
let repoUrl = '';

// Fetch inventory data
async function loadInventory() {
    try {
        const resp = await fetch('inventory/personas.json');
        if (!resp.ok) throw new Error(resp.statusText);
        const index = await resp.json();

        const inventories = await Promise.all(
            index.personas.map(async (p) => {
                const r = await fetch(p.inventory_url);
                if (!r.ok) throw new Error(r.statusText);
                return r.json();
            })
        );

        allData = { index: index.personas, inventories };
        repoUrl = index.repo_url || '';
        buildFilters();

        try {
            const tr = await fetch('traces/index.json');
            if (tr.ok) {
                const trData = await tr.json();
                for (const t of trData.traces || []) {
                    skillsWithTraces.add(t.skill);
                }
            }
        } catch (_) { /* no traces yet — silently skip */ }

        render();
    } catch (err) {
        personasContainer.innerHTML =
            '<p class="no-results">Could not load skills inventory.</p>';
        console.error('Inventory load failed:', err);
    }
}

// Build filter buttons from loaded personas
function buildFilters() {
    filtersContainer.innerHTML = '';

    const allBtn = makeFilterBtn('ALL', 'all');
    allBtn.classList.add('active');
    filtersContainer.appendChild(allBtn);

    for (const p of allData.index) {
        filtersContainer.appendChild(
            makeFilterBtn(p.label.toUpperCase(), p.id)
        );
    }
}

function makeFilterBtn(label, value) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.textContent = label;
    btn.dataset.filter = value;
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = value;
        render();
    });
    return btn;
}

// Render persona sections
function render() {
    personasContainer.innerHTML = '';

    const visible = activeFilter === 'all'
        ? allData.inventories
        : allData.inventories.filter((inv) => inv.persona === activeFilter);

    if (visible.length === 0) {
        personasContainer.innerHTML = '<p class="no-results">No skills found.</p>';
        return;
    }

    for (const inv of visible) {
        personasContainer.appendChild(renderPersona(inv));
    }
}

function renderPersona(inv) {
    const section = document.createElement('div');
    section.className = 'persona-section';

    const color = PERSONA_COLORS[inv.persona] || 'var(--accent-green)';
    const label = inv.label || PERSONA_META_LABELS[inv.persona] || inv.persona;

    // Meta skill callout — uses human-facing headline/pitch from persona.yaml
    if (inv.meta_skill) {
        const headline = `${label} Pack: ${inv.headline}`;
        const pitch = inv.pitch || inv.meta_skill.description;
        const objective = inv.design?.objective || '';

        const metaName = inv.meta_skill.name;
        const metaTracesLink = skillsWithTraces.has(metaName)
            ? `<a href="traces/#skill=${metaName}" class="traces-link">view traces</a>` : '';
        const metaEditLink = repoUrl && inv.meta_skill.source_path
            ? `<a href="${repoUrl}tree/main/${inv.meta_skill.source_path}" class="edit-link" target="_blank">edit</a>` : '';

        const callout = document.createElement('div');
        callout.className = 'meta-callout';
        callout.style.borderColor = color;
        const metaStatus = inv.meta_skill.status || 'preview';
        const metaStatusBadge = `<span class="skill-status-badge skill-status-${metaStatus}">${metaStatus.charAt(0).toUpperCase() + metaStatus.slice(1)}</span>`;
        callout.innerHTML = `
            <div class="meta-callout-body">
                <div class="meta-callout-text">
                    <div class="meta-callout-heading">
                        <h3>${headline}</h3>
                        ${metaStatusBadge}
                    </div>
                    ${objective ? `<p class="meta-objective">${objective}</p>` : ''}
                    <p class="meta-desc">${pitch}</p>
                    <div class="meta-links">${metaTracesLink}${metaEditLink}</div>
                </div>
                <a href="${inv.meta_skill.install_url}" class="btn btn-primary meta-install-btn" download>
                    Install Meta Skill
                </a>
            </div>
        `;
        section.appendChild(callout);
    }

    // Skill cards grid
    if (inv.skills.length > 0) {
        const grid = document.createElement('div');
        grid.className = 'skills-grid';

        for (const skill of inv.skills) {
            grid.appendChild(renderSkillCard(skill, label, color));
        }
        section.appendChild(grid);
    }

    return section;
}

function renderSkillCard(skill, personaLabel, color) {
    const card = document.createElement('div');
    card.className = 'skill-card';

    const label = personaLabel;
    const editLink = repoUrl && skill.source_path
        ? `<a href="${repoUrl}tree/main/${skill.source_path}" class="edit-link" target="_blank">edit</a>` : '';

    const status = skill.status || 'preview';
    const statusBadge = `<span class="skill-status-badge skill-status-${status}">${status.charAt(0).toUpperCase() + status.slice(1)}</span>`;
    card.innerHTML = `
        <div class="skill-header">
            <span class="skill-category" style="background-color: ${color}">${label}</span>
            ${statusBadge}
        </div>
        <h3 class="skill-title">${formatTitle(skill.name)}</h3>
        <p class="skill-desc">${truncate(skill.description, 180)}</p>
        <a href="${skill.install_url}" class="download-btn" download>Download Skill (.skill)</a>
        <div class="card-links">
            ${skillsWithTraces.has(skill.name) ? `<a href="traces/#skill=${skill.name}" class="traces-link">view traces</a>` : ''}
            ${editLink}
        </div>
    `;
    return card;
}

// Helpers
function formatTitle(name) {
    return name
        .split('-')
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ');
}

function truncate(str, max) {
    if (!str || str.length <= max) return str || '';
    return str.slice(0, max).replace(/\s+\S*$/, '') + '\u2026';
}

// Boot
document.addEventListener('DOMContentLoaded', loadInventory);
