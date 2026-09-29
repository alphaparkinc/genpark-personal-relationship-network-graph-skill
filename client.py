"""Personal Relationship Network Graph.
100% Python Standard Library.
"""

import time

class PersonalRelationshipGraph:
    """Manages personal social graph, touchpoint history, and relationship decay alerts."""
    def __init__(self, decay_days_threshold=30):
        self.contacts = {}
        self.decay_seconds = decay_days_threshold * 86400

    def add_contact(self, contact_id, name, relationship_tag, cadence_days=14):
        self.contacts[contact_id] = {
            "name": name,
            "relationship_tag": relationship_tag,
            "cadence_days": cadence_days,
            "interactions": [],
            "last_interaction": time.time(),
            "notes": []
        }

    def log_interaction(self, contact_id, note, epoch=None):
        if contact_id not in self.contacts:
            raise KeyError(f"Contact {contact_id} not found")
        now = epoch or time.time()
        self.contacts[contact_id]["interactions"].append({"note": note, "timestamp": now})
        self.contacts[contact_id]["last_interaction"] = now

    def get_stale_contacts(self, current_epoch):
        stale = []
        for cid, c in self.contacts.items():
            threshold = c["cadence_days"] * 86400
            elapsed = current_epoch - c["last_interaction"]
            if elapsed > threshold:
                stale.append({
                    "contact_id": cid,
                    "name": c["name"],
                    "days_inactive": int(elapsed // 86400),
                    "target_cadence_days": c["cadence_days"]
                })
        stale.sort(key=lambda x: x["days_inactive"], reverse=True)
        return stale
