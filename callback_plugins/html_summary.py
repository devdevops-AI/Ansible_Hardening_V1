from __future__ import annotations

import os
from ansible.plugins.callback import CallbackBase
from jinja2 import Environment, FileSystemLoader


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'html_summary'

    def __init__(self):
        super().__init__()
        self.hostvars = {}

    def v2_runner_on_ok(self, result):
        self._record_hostvars(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._record_hostvars(result)

    def v2_runner_on_skipped(self, result):
        self._record_hostvars(result)

    def v2_runner_on_unreachable(self, result):
        self._record_hostvars(result)

    def _record_hostvars(self, result):
        host = result._host.get_name()
        if host not in self.hostvars:
            vars_mgr = result._task._variable_manager
            vars = vars_mgr.get_vars(host=result._host)
            self.hostvars[host] = {
                'location': vars.get('location', 'unknown')
            }

    def v2_playbook_on_stats(self, stats):
        results = {}
        for host in stats.processed.keys():
            s = stats.summarize(host)
            results[host] = {
                'ok': s.get('ok', 0),
                'changed': s.get('changed', 0),
                'failures': s.get('failures', 0),
                'skipped': s.get('skipped', 0),
                'unreachable': s.get('unreachable', 0),
                'location': self.hostvars.get(host, {}).get('location', 'unknown'),
            }
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('report.html.j2')
        html = template.render(results=results)
        with open('hardening_report.html', 'w') as f:
            f.write(html)
