This comparison document outlines the structural and strategic alignment between the **Office of Career Services (OCS)** and the **Office of Public Interest Advising (OPIA)**. It is designed to be ingested by an agent to determine when to trigger specific branching logic or templates within the `resume-review` skill.

### Comparative Analysis: OCS vs. OPIA Resume Standards

| Feature | OCS (Private Sector/Clerkships) | OPIA (Public Interest/Government) |
| :--- | :--- | :--- |
| **Primary Goal** | Demonstrate efficiency, analytical rigor, and professional polish for firm/corporate environments. | Demonstrate "public interest heart," substantive commitment to a cause, and advocacy skills. |
| **Page Length** | **Strictly one page** for J.D. candidates. | **Two pages are acceptable** if the candidate has substantial pre-law or public interest experience. |
| **Degree Name** | Must use "Juris Doctor" (not "Juris Doctorate"). | Same; consistency in degree terminology is a shared HLS standard. |
| **Header** | Name (14-16pt), Cambridge address (optional), phone, and HLS email. | Similar; can include a "Permanent Address" to signal geographic ties to a specific market. |
| **Clinics & SPOs** | Often listed under **Activities** unless highly substantive. | Strongly encouraged to be listed under **Experience** to show hands-on advocacy. |
| **Relevant Coursework**| Generally discouraged or kept to a single line to save space. | Recommended to signal specific expertise (e.g., "Immigration Law") to employers. |
| **Action Verbs** | Focused on "analyzed," "researched," and "managed". | Focused on "advocated," "represented," "organized," and "empowered". |
| **Skills Section** | Discourages listing "Westlaw/Lexis" or basic office software. | Values language proficiency and community outreach tools more highly. |

### Core Similarities (The "HLS Baseline")
* **Mechanical Basics**: Both offices require the same "clean lines" formatting: no periods at the end of bullets, italicized Latin honors (lowercase), and italicized journal names.
* **Transparency**: Avoidance of jargon and emphasis on "Action + Result" bullet points.
* **Education Order**: Harvard Law School always appears first, followed by undergraduate institutions in reverse-chronological order.

### Strategic Branching Logic for Agents
When the `resume-review` skill identifies a **Public Interest/OPIA** profile, it must:
1.  **Relax the Length Constraint**: Do not flag a 1.5-page resume as a "critical error" if the content is relevant to public service.
2.  **Reposition Clinics**: Suggest moving Clinical work from the "Education" or "Activities" section into "Experience" to maximize its impact.
3.  **Audit the "Commitment Narrative"**: Look for a "Relevant Coursework" section or a "Pro Bono/Community Service" header to ensure the student's dedication is visible.
