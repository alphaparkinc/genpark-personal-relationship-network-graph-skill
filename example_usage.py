from client import PersonalRelationshipGraph
import time

prm = PersonalRelationshipGraph()
now = time.time()

# Add contacts with target cadences
prm.add_contact("CID_ALEX", "Alex Turner", "Close Collaborator", cadence_days=7)
prm.add_contact("CID_DANA", "Dana White", "Quarterly Advisory", cadence_days=90)

# Log meeting
prm.log_interaction("CID_ALEX", "Discussed Series A roadmap over lunch", epoch=now - 10 * 86400) # 10 days ago

# Check stale contacts
stale = prm.get_stale_contacts(current_epoch=now)
print("Contacts Requiring Reconnection:")
for s in stale:
    print(f" - {s['name']} (Inactive {s['days_inactive']} days / target {s['target_cadence_days']} days)")
