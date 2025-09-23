package contracts

default allow = false

deny[msg] {
  input.metric == "freshness_sec"
  input.value > input.sla
  msg := sprintf("Freshness %d > SLA %d", [input.value, input.sla])
}

deny[msg] {
  input.metric == "completeness_pct"
  input.value < input.sla
  msg := sprintf("Completeness %.2f < SLA %.2f", [input.value, input.sla])
}

allow { not deny[_] }
