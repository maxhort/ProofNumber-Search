from collections import defaultdict
class TranspositionTable():
    """Transposition table that saves move information about board states

    """
    def __init__(self):
        self.transposition_table = dict()
    def in_table(self,hashcode,hashkey):
        """Checks wheter hashcode and hashkey are stored
    
        Args:
            hashcode: Hashcode of entry, used as key in TranspositionTable
            haskey: Hashkey of entry, used to verify correctness

        Returns:
            bool: If entry exists
        """
        return hashcode in self.transposition_table and self.transposition_table[hashcode]["hashkey"] == hashkey
    def lookup(self, hashcode, hashkey):
        """Returns an entry by hashcode and hashkey
    
        Args:
            hashcode: Hashcode of entry
            hashkey: Hashkey of entry

        Returns:
            Object: value of entry
        """
        if hashcode in self.transposition_table and  self.transposition_table[hashcode]["hashkey"] == hashkey:
            return self.transposition_table[hashcode]
        return None

    def add_entry(self,hashcode,entry):
        """Adds entry to the TranspositionTable
    
        Args:
            hashcode: Hashcode of entry
            haskey: Hashkey of entry
            entry: Entry to be added
        """
        # Replacement scheme new
        self.transposition_table[hashcode] = entry

    def reset(self):
        self.transposition_table = dict()

    def size(self):
        return len(self.transposition_table)