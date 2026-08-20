"""Skill evaluation tests.

This file re-exports the generic test module from skill-eval. Discovery and
parametrization (rubric.yaml files under skills/, scenarios, null baselines)
are handled by skill_eval's pytest plugin; configuration comes from eval.yaml.

Run with:
    uv run pytest tests/ -v -s          # skip scenarios that already have traces
    uv run pytest tests/ -v -s --rerun  # force re-run everything

Requires OPENROUTER_API_KEY in .env (or the env var configured in eval.yaml).
"""

from skill_eval.test_skills import *  # noqa: F401, F403
