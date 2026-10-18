class KnowledgeBase:
    """A declarative Knowledge Base storing facts and rules (Horn Clauses) 
    with a Data-Driven Forward Chaining inference engine."""

    def __init__(self):
        self.facts = set()  # Set of unique string facts
        self.rules = []     # List of tuples: (premise_list, conclusion_string)

    def tell_fact(self, fact_string: str):
        """Adds a atomic fact to the Knowledge Base."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list, conclusion_string: str):
        """Adds a Horn Clause rule (premise_list -> conclusion_string) to the Knowledge Base."""
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        """Clears all facts while preserving domain rules."""
        self.facts.clear()

    def forward_chain(self):
        """Data-Driven Forward Chaining algorithm executing Modus Ponens 
        until no new facts can be deduced."""
        new_facts_added = True
        while new_facts_added:
            new_facts_added = False
            for premises, conclusion in self.rules:
                if conclusion not in self.facts:
                    # Modus Ponens Check: If all premises exist in facts
                    if all(p in self.facts for p in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True