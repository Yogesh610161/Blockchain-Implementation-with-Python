import functools
import json
import hashlib
from block import Block
from transaction import Tansaction
from utility.hashutil import hash_string_256,hashedblock
from wallet import Wallet
class Verification:
    @staticmethod
    def valid_proof(transactions, previoushash, proof):
        guess=(str([tx.to_ordered_dict for tx in transactions])+str(previoushash)+str(proof)).encode()
        guess_hash=hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2]=='00'

    @classmethod
    def verify_chain(cls,blockchain):
        valid=True
        for (index,block) in enumerate(blockchain):
            if index==0:
                continue
            if block.previoushash!=hashedblock(blockchain[index-1]):
                valid= False
            if not cls.valid_proof(block.transaction[:-1 ],block.previoushash,block.proof)  :
                print("proof of work is invalid")
                return False
        return valid
    @staticmethod
    def verifytransaction(transaction,getbalance,check_funds=True):
        if check_funds:
            userbalance=getbalance(transaction.sender)
            return userbalance >= transaction.amount and Wallet.verify_transactions1(transaction)
        else:
            return Wallet.verify_transactions1(transaction)    

    @classmethod
    def verifytransactions(cls,opentransactions,getbalance):
        return all([cls.verifytransaction(tx,getbalance,False) for tx in opentransactions])
