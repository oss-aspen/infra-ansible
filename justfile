
check-snapshot S:
	ansible-playbook playbooks/check_snapshot.yml -e "snapshot_id={{S}}"
