import os
import unittest

from checkov.runner_filter import RunnerFilter
from checkov.terraform.checks.resource.oci.SecurityGroupsIngressStatelessSecurityRules import check
from checkov.terraform.runner import Runner


class TestSecurityGroupsIngressStatelessSecurityRules(unittest.TestCase):
    def test(self):
        runner = Runner()
        current_dir = os.path.dirname(os.path.realpath(__file__))

        test_files_dir = current_dir + "/example_SecurityGroupsIngressStatelessSecurityRules"
        report = runner.run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[check.id]))
        summary = report.get_summary()

        passing_resources = {
            "oci_core_network_security_group_security_rule.pass",
        }

        failing_resources = {
            "oci_core_network_security_group_security_rule.fail",
            "oci_core_network_security_group_security_rule.fail1",
        }

        skipped_resources = {
            "oci_core_network_security_group_security_rule.skip",
            "oci_core_network_security_group_security_rule.skip1",
        }

        passed_check_resources = set([c.resource for c in report.passed_checks])
        failed_check_resources = set([c.resource for c in report.failed_checks])
        skipped_check_resources = set([c.resource for c in report.skipped_checks])

        self.assertEqual(summary["passed"], 1)
        self.assertEqual(summary["failed"], 2)
        self.assertEqual(summary["skipped"], 2)
        self.assertEqual(summary["parsing_errors"], 0)

        self.assertEqual(skipped_resources, skipped_check_resources)
        self.assertEqual(passing_resources, passed_check_resources)
        self.assertEqual(failing_resources, failed_check_resources)


if __name__ == "__main__":
    unittest.main()
