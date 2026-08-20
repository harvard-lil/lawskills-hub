// Traces viewer — version-timeline bar chart with detail overlay.

const tracesApp = document.getElementById('traces-app');
const overlay = document.getElementById('traces-overlay');
const detailPanel = document.getElementById('traces-detail');

overlay.addEventListener('click', e => { if (e.target === overlay) closeDetail(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDetail(); });

function closeDetail() { overlay.classList.remove('open'); }

function scoreClass(s) { return s >= 75 ? 'score-high' : s >= 50 ? 'score-mid' : 'score-low'; }
function scoreColor(s) { return s >= 75 ? '#16a34a' : s >= 50 ? '#d97706' : '#dc2626'; }

function fmtTime(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + ' ' +
           d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

function sortVersions(versions) {
    return [...versions].sort((a, b) => {
        if (a === '_null') return -1;
        if (b === '_null') return 1;
        return a.localeCompare(b, undefined, { numeric: true });
    });
}

function fmtVersion(v) {
    return v === '_null' ? 'null' : 'v' + v;
}

// Group traces into persona → skill → { versions[], scenarios: { id: { version: [runs] } } }
function groupTraces(traces) {
    const personas = {};
    for (const t of traces) {
        // skill-eval writes this key as `group`; older traces use `persona`.
        const p = t.group || t.persona;
        if (!personas[p]) personas[p] = {};
        if (!personas[p][t.skill]) {
            personas[p][t.skill] = { versions: new Set(), scenarios: {} };
        }
        const sk = personas[p][t.skill];
        sk.versions.add(t.version);
        if (!sk.scenarios[t.scenario_id]) sk.scenarios[t.scenario_id] = {};
        if (!sk.scenarios[t.scenario_id][t.version]) sk.scenarios[t.scenario_id][t.version] = [];
        sk.scenarios[t.scenario_id][t.version].push(t);
    }
    for (const persona of Object.values(personas)) {
        for (const sk of Object.values(persona)) {
            sk.versions = sortVersions(sk.versions);
            for (const scn of Object.values(sk.scenarios)) {
                for (const runs of Object.values(scn)) {
                    runs.sort((a, b) => a.timestamp.localeCompare(b.timestamp));
                }
            }
        }
    }
    return personas;
}

const PERSONA_COLORS = {
    professor: 'var(--accent-purple)',
    student: 'var(--accent-blue)',
    'pro-se': 'var(--accent-yellow)',
    cle: 'var(--accent-green)',
    'skill-developer': '#ddd',
};

function personaColor(id) { return PERSONA_COLORS[id] || '#ddd'; }
function shortModel(m) { return m.includes('/') ? m.split('/').pop() : m; }
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function renderAll(personas) {
    if (Object.keys(personas).length === 0) {
        tracesApp.innerHTML = '<p class="traces-empty">No traces found. Run tests to generate traces.</p>';
        return;
    }

    let html = '';
    const sortedPersonas = Object.keys(personas).sort();

    for (const personaId of sortedPersonas) {
        const skills = personas[personaId];
        const sortedSkills = Object.keys(skills).sort();

        html += `<div class="trace-persona-section">`;
        html += `<div class="trace-persona-heading">
            <span class="trace-persona-tag" style="background-color: ${personaColor(personaId)}">${esc(personaId)}</span>
        </div>`;

        for (const skillName of sortedSkills) {
            const skillData = skills[skillName];
            const groupId = `skill-${skillName}`;

            html += `<div class="trace-skill-group" id="${esc(groupId)}">`;
            html += `<div class="trace-skill-header"><h3>${esc(skillName)}</h3></div>`;
            html += renderTimelineGrid(skillData);
            html += `</div>`;
        }

        html += `</div>`;
    }

    tracesApp.innerHTML = html;

    tracesApp.querySelectorAll('.tl-bar[data-path]').forEach(bar => {
        bar.addEventListener('click', () => loadDetail(bar.dataset.path));
    });

    applyDeepLink();
}

function renderTimelineGrid(skillData) {
    const versions = skillData.versions;
    const scenarios = Object.keys(skillData.scenarios).sort();
    const n = versions.length;

    let html = `<div class="timeline-grid" style="grid-template-columns: minmax(120px, auto) repeat(${n}, minmax(60px, 1fr))">`;

    // Version labels as header row
    html += `<div class="tl-corner"></div>`;
    for (const v of versions) {
        html += `<div class="tl-version">${esc(fmtVersion(v))}</div>`;
    }

    // Scenario rows
    for (const scnId of scenarios) {
        html += `<div class="tl-label">${esc(scnId)}</div>`;

        for (const v of versions) {
            const runs = skillData.scenarios[scnId][v] || [];
            html += `<div class="tl-cell">`;
            html += `<div class="tl-bar-area">`;
            for (const run of runs) {
                const pct = Math.max(run.score, 3);
                const color = scoreColor(run.score);
                const tip = `${Math.round(run.score)}/100 · ${shortModel(run.model)} · ${fmtTime(run.timestamp)}`;
                html += `<div class="tl-bar" style="height: ${pct}%; background-color: ${color}" data-path="${esc(run.path)}" title="${esc(tip)}"></div>`;
            }
            html += `</div>`;
            html += `<div class="tl-score-area">`;
            for (const run of runs) {
                html += `<span class="tl-bar-score" style="color: ${scoreColor(run.score)}">${Math.round(run.score)}</span>`;
            }
            html += `</div>`;
            html += `</div>`;
        }
    }

    html += `</div>`;
    return html;
}

// Detail panel

async function loadDetail(path) {
    detailPanel.innerHTML = '<p class="traces-empty">Loading trace…</p>';
    overlay.classList.add('open');
    try {
        const resp = await fetch(path);
        const data = await resp.json();
        renderDetail(data);
    } catch (e) {
        detailPanel.innerHTML = `<p class="traces-empty" style="color:#dc2626">Failed to load trace: ${esc(e.message)}</p>`;
    }
}

function renderDetail(data) {
    const m = data.meta;
    const ev = data.evaluation;
    let html = `<button class="detail-close" onclick="closeDetail()">&times;</button>`;
    html += `<h3>${esc(m.skill)} / ${esc(m.scenario_id)}</h3>`;
    html += `<dl class="detail-meta">
        <dt>Score</dt><dd class="${scoreClass(ev.score)}">${ev.score.toFixed(0)}/100</dd>
        <dt>Model</dt><dd>${esc(data.config.model_under_test.model)}</dd>
        <dt>Judge</dt><dd>${esc(data.config.judge_model.model)}</dd>
        <dt>Time</dt><dd>${fmtTime(m.timestamp)}</dd>
        <dt>Persona</dt><dd>${esc(m.group || m.persona)}</dd>
        <dt>Version</dt><dd>${esc(m.version)}</dd>
    </dl>`;

    if (ev.structural.length) {
        html += `<div class="detail-section"><h4>Structural (${ev.structural.filter(c=>c.result==='pass').length}/${ev.structural.length} pass)</h4>`;
        for (const c of ev.structural) {
            html += criterion(c.result, c.criterion_id, c.justification);
        }
        html += `</div>`;
    }
    if (ev.pedagogical.length) {
        html += `<div class="detail-section"><h4>Pedagogical</h4>`;
        for (const c of ev.pedagogical) {
            html += criterion(c.result, c.criterion_id, c.justification);
        }
        html += `</div>`;
    }
    if (ev.anti_patterns.length) {
        html += `<div class="detail-section"><h4>Anti-patterns</h4>`;
        for (const c of ev.anti_patterns) {
            html += criterion(c.result, c.criterion_id, c.justification);
        }
        html += `</div>`;
    }

    html += `<div class="detail-section"><h4>Conversation (${data.conversation.length} turns)</h4><div class="conversation">`;
    for (const turn of data.conversation) {
        html += `<div class="conv-turn ${turn.role}">
            <div class="conv-role">${turn.role}</div>
            <div class="conv-content">${esc(turn.content)}</div>
        </div>`;
    }
    html += `</div></div>`;

    if (data.scenario.expected && data.scenario.expected.length) {
        html += `<div class="detail-section"><h4>Expected behaviors</h4><ul>`;
        for (const e of data.scenario.expected) html += `<li>${esc(e)}</li>`;
        html += `</ul></div>`;
    }

    detailPanel.innerHTML = html;
}

function criterion(result, id, justification) {
    return `<div class="criterion">
        <span class="criterion-tag ${result}">${result}</span>
        <span class="criterion-body"><b>${esc(id)}</b> — ${esc(justification)}</span>
    </div>`;
}

function applyDeepLink() {
    const hash = location.hash;
    if (!hash) return;
    const m = hash.match(/^#skill=(.+)$/);
    if (!m) return;
    const target = document.getElementById(`skill-${m[1]}`);
    if (!target) return;
    target.classList.add('highlighted');
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Boot
fetch('index.json')
    .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); })
    .then(data => renderAll(groupTraces(data.traces)))
    .catch(() => {
        tracesApp.innerHTML = '<p class="traces-empty">No traces yet — run tests to generate data.</p>';
    });
