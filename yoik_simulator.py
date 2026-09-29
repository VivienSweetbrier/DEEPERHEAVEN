import time

class LWWRegister:
    """A mathematically perfect Last-Write-Wins CRDT Register."""
    def __init__(self):
        self.state = {} # key: (value, timestamp)

    def set(self, key, value):
        # We use monotonic time to ensure order, representing the Iron Rod of time.
        self.state[key] = (value, time.monotonic_ns())

    def merge(self, other):
        """The Yoik Reconciliation. Truth merges seamlessly."""
        for k, (v, ts) in other.state.items():
            if k not in self.state or ts > self.state[k][1]:
                self.state[k] = (v, ts)
        return self.state
        
    def display(self):
        return {k: v for k, (v, ts) in self.state.items()}

print("SOCK GREMLIN: INITIATING PHENOMENOLOGICAL PROOF OF THE YOIK MESH...\n")

node_a = LWWRegister()
node_b = LWWRegister()

print("== PHASE 1: THE PEACE ==")
print("Node A parks 5,000 CLNK in Register_1.")
node_a.set("Register_1", 5000)
node_b.merge(node_a)
print(f"Node A sees: {node_a.display()}")
print(f"Node B sees: {node_b.display()}\n")


print("== PHASE 2: THE 1997 RED RIVER FLOOD ==")
print("The fiber optics snap! The network partitions into isolated islands!")
print("Node A and Node B can no longer communicate.\n")

time.sleep(0.1) # Simulate time passing
print("Node A detects hoarding! Applying 50 CLNK Entropy Burn to Register_1...")
node_a.set("Register_1", 4950)

time.sleep(0.1)
print("Node B's ESP32 detects a Bio-Mimetic Harvest! Minting 200 CLNK to Register_2...")
node_b.set("Register_2", 200)

print(f"\n[ISOLATED] Node A current reality: {node_a.display()}")
print(f"[ISOLATED] Node B current reality: {node_b.display()}\n")


print("== PHASE 3: THE WATERS RECEDE (THE YOIK IS SUNG) ==")
print("LoRa connection re-established. The Nodes sing their state to each other...")
node_a.merge(node_b)
node_b.merge(node_a)

print(f"\n[RECONCILED] Node A ultimate truth: {node_a.display()}")
print(f"[RECONCILED] Node B ultimate truth: {node_b.display()}\n")

print("MATHEMATICAL PERFECTION ACHIEVED! No central database. No Aladdin Overwrite.")
print("The truth simply *is*. AWLELUYAH! [SOCK]")
