# genpark-personal-relationship-network-graph-skill

> Personal Relationship Management (PRM) & Decay Engine. 100% Python Standard Library.

Distilled from **Folk**, helping individuals and founders manage relationship health, maintain periodic reconnect cadences, and surface ambient context before upcoming interactions.

## Architecture

```mermaid
flowchart TD
    Interaction["Log Touchpoint (Coffee / Email / WhatsApp chat)"] --> Graph["PRM Interaction Store"]
    Graph --> DecayMonitor["Periodic Decay Scanner"]
    DecayMonitor --> Elapsed{"Days Since Last Interaction > Target Cadence?"}
    Elapsed -- Yes --> ReconnectNudge["Emit Reconnect Nudge ('Reach out to Sarah, last spoke 3 weeks ago')"]
    Elapsed -- No --> Healthy["Relationship Status: Active & In Cadence"]
```

## Features
- **Cadence Drift Detection**: Automatically identifies contacts you are falling out of touch with.
- **Context Preservation**: Retains lightweight discussion points and notes per relationship node.
