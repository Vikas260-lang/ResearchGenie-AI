def build_knowledge_graph(claims, debates=None):

    # ---------------- SAFETY ----------------
    if not claims or len(claims) == 0:
        return {"nodes": [], "edges": []}

    nodes = []
    edges = []

    # ---------------- CLAIM NODES ----------------
    for c in claims:
        cid = c.get("claim_id", "")
        label = c.get("statement", "")

        if cid:
            nodes.append({
                "id": cid,
                "label": f"{cid}: {label[:30]}" if label else cid
            })

    # ---------------- CONNECT CLAIMS ----------------
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            edges.append({
                "source": claims[i]["claim_id"],
                "target": claims[j]["claim_id"]
            })

    # ---------------- ADD DEBATE NODES ----------------
    if debates:
        for d in debates:
            claim_id = d.get("claim_id", "")
            debate_id = f"D_{claim_id}"

            # Debate node
            nodes.append({
                "id": debate_id,
                "label": f"Debate on {claim_id}"
            })

            # Connect claim → debate
            edges.append({
                "source": claim_id,
                "target": debate_id
            })

            # Add PRO / CON nodes
            for idx, arg in enumerate(d.get("arguments", [])):
                arg_id = f"{debate_id}_{idx}"

                label = f"{arg.get('side', '').upper()}: {arg.get('reasoning', '')[:25]}"

                nodes.append({
                    "id": arg_id,
                    "label": label
                })

                # Connect debate → argument
                edges.append({
                    "source": debate_id,
                    "target": arg_id
                })

    return {
        "nodes": nodes,
        "edges": edges
    }