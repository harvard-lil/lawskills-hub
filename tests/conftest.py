"""No local fixtures.

Fixtures, CLI options (--rerun, --skills-dir) and scenario parametrization
now come from skill_eval's pytest plugin, which registers itself via the
package's pytest11 entry point. This file must stay empty of pytest hooks,
otherwise it collides with that plugin's `pytest_addoption`.
"""
