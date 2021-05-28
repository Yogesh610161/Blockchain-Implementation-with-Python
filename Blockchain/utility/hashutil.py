import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()
def hashedblock(block):
    hashable_block=block.__dict__.copy()
    hashable_block['transaction']=[tx.to_ordered_dict() for tx in hashable_block['transaction']]
    return hash_string_256(json.dumps(hashable_block,sort_keys=True).encode())
