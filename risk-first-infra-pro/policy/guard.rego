package guard

default block = true

block { input.health.quality_status != "pass" }
block { input.health.drift_status != "pass" }
block { input.health.privacy_status != "pass" }
block { input.health.policy_status != "pass" }

allow { not block }

reason[msg] {
  block
  msg := sprintf("Blocked by guard: %v", [input.health])
}
