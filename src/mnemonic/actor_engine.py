from .imagery_engine import AbsurdImageryEngine

class ActorEngine:
    # Simple keyword mapping for actors
    KEYWORD_ACTORS = {
        "network": "The Neon Spider",
        "protocol": "The Diplomat",
        "security": "The Iron Golem",
        "firewall": "The Burning Knight",
        "router": "The Traffic Controller",
        "switch": "The Train Conductor",
        "wireless": "The Invisible Ghost",
        "cloud": "The Sky Captain",
        "server": "The Butler",
        "database": "The Librarian",
        "policy": "The Judge",
        "attack": "The Assassin",
        "malware": "The Plague Doctor",
        "encryption": "The Cipher Mage",
        "intro": "The Guide",
        "troubleshoot": "The Detective"
    }

    @staticmethod
    def get_actor(topic):
        """Returns an Actor based on keywords in the topic."""
        topic_lower = topic.lower()
        
        for keyword, actor in ActorEngine.KEYWORD_ACTORS.items():
            if keyword in topic_lower:
                return actor
        
        # Fallback: Use imagery engine but frame it as an "Entity"
        # or just return a generic one
        return "The Stranger"
