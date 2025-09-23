.PHONY: demo seed checks drift privacy health
seed:
	python seeds/generate_txns.py && python seeds/generate_content.py && python features/build_features.py
checks:
	python quality/run_checks.py
drift:
	python drift/run_drift.py
privacy:
	python privacy/run_privacy.py
health:
	python state/aggregate_health.py
demo: seed checks drift privacy health
