from collections import defaultdict
class DualEntry():
    def __init__(self):
        self.entry1 = dict()
        self.entry2 = dict()
    
    def hashkey_in_entry(self,hashkey):
        return self.entry1 and self.entry1["hashkey"] == hashkey or self.entry2 and self.entry2["hashkey"] == hashkey

    def lookup_hashkey(self,hashkey):
        if self.entry1 and self.entry1["hashkey"] == hashkey: return self.entry1
        if self.entry2 and self.entry2["hashkey"] == hashkey: return self.entry2
        return None

    def add_entry(self,entry): 
        add_double = 1 if self.entry1 and not self.entry2 else 0
        if not self.entry2 or self.entry1["size"]>=self.entry2["size"]:
            self.entry2 = self.entry1
        self.entry1 = entry
        return add_double
class TT_TwoBig():
    """Transposition table that saves move information about board states
    replacement scheme two big

    """
    def __init__(self):
        self.transposition_table = defaultdict(DualEntry)
        self.double_entries = 0
    def in_table(self,hashcode,hashkey):
        """Checks wheter hashcode and hashkey are stored
    
        Args:
            hashcode: Hashcode of entry, used as key in TranspositionTable
            haskey: Hashkey of entry, used to verify correctness

        Returns:
            bool: If entry exists
        """
        return hashcode in self.transposition_table and self.transposition_table[hashcode].hashkey_in_entry(hashkey)
    def lookup(self, hashcode, hashkey):
        """Returns an entry by hashcode and hashkey
    
        Args:
            hashcode: Hashcode of entry
            hashkey: Hashkey of entry

        Returns:
            Object: value of entry
        """
        if hashcode in self.transposition_table:
            return self.transposition_table[hashcode].lookup_hashkey(hashkey)
        return None

    def add_entry(self,hashcode,entry):
        """Adds entry to the TranspositionTable
    
        Args:
            hashcode: Hashcode of entry
            entry: Entry to be added
        """
        # Replacement scheme big
        self.double_entries += self.transposition_table[hashcode].add_entry(entry)

    def reset(self):
        self.transposition_table = defaultdict(DualEntry)

    def size(self):
        return len(self.transposition_table)+self.double_entries