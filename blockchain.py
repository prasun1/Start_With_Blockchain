# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 11:03:49 2018

@author: I871175
"""
#Module 1: create a blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify


#part 1- Building a Blockcahin

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0') #genesis block
        
    #create and mine function is diff
    #mine function will get the POW that we have to solve mine will give us proof based on POW
    #create will apply after mine function
    def create_block(self,proof, previous_hash):
        block = {'index': len(self.chain) +1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }
        self.chain.append(block)
        return block
    
        
    def get_previous_block(self):
        return self.chain[-1]
    
    

        #proof of work: a number which is hard to find, easy to verify
      #non symmetrical is new_proof - prev_proof != prev_proof-new_proof  
    def proof_of_work(self, previous_proof):
         
        new_proof = 1 #increment this until we get a right proof, try and guess approach
        check_proof = False # to check proof
        while(check_proof is False):
            #problem to solve
            #it should be non symmetrical , we cannot take new_proof + prev_proof, as vice versa is true which will result in same hash every 2 blocks
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #non-symmetrical
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
            
    #take a block and return hash256 version of that block
    #to check whether blockchain is valid or not
    def hash_function(self,block):
         
         #make a dic into string
         encoded_block = json.dumps(block,sort_keys = True).encode() # takes a dic and convert that in string
         return hashlib.sha256(encoded_block).hexdigest()
            
            
    #checking whether chain is valid or not
    #check if each block in blockchain has a correct proof-of work
    # is prev_hash = hash of previous block
    def is_chain_valid(self,chain):
         previous_block = chain[0]
         block_index = 1
         while(block_index < len(chain)):
              block = chain[block_index]
              if block['previous_hash'] != self.hash_function(previous_block):
                  return False
              #check proof of each block is valid by checking value is '0000'
              previous_proof = previous_block['proof']
              proof = block['proof']
              hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() #non-symmetrical
              if hash_operation[:4] != '0000':
                  check_proof = False
              previous_block = block
              block_index += 1
         return True
             
         
     
                 
    #Part 2- Minning our Blockchain
    
    #create a webapp
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash_function(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message': 'Congratulation you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
                }
    return jsonify(response), 200
    

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
               'chain': blockchain.chain,
               'length': len(blockchain.chain)
               }
    return jsonify(response), 200
    
    
    
    
    
    
#Running the app
app.run(host = '0.0.0.0', port = 5000)
    
    
    