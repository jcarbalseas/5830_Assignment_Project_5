# from web3 import Web3
# from web3.contract import Contract
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware #Necessary for POA chains
# import json
# import sys
# from pathlib import Path

# source_chain = 'avax'
# destination_chain = 'bsc'
# contract_info = "contract_info.json"

# def connectTo(chain):
#     if chain == 'avax':
#         api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

#     if chain == 'bsc':
#         api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

#     if chain in ['avax','bsc']:
#         w3 = Web3(Web3.HTTPProvider(api_url))
#         # inject the poa compatibility middleware to the innermost layer
#         w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#     return w3

# def getContractInfo(chain):
#     """
#         Load the contract_info file into a dictinary
#         This function is used by the autograder and will likely be useful to you
#     """
#     p = Path(__file__).with_name(contract_info)
#     try:
#         with p.open('r')  as f:
#             contracts = json.load(f)
#     except Exception as e:
#         print( "Failed to read contract info" )
#         print( "Please contact your instructor" )
#         print( e )
#         sys.exit(1)

#     return contracts[chain]



# def scanBlocks(chain):
#     """
#         chain - (string) should be either "source" or "destination"
#         Scan the last 5 blocks of the source and destination chains
#         Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
#         When Deposit events are found on the source chain, call the 'wrap' function the destination chain
#         When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
#     """

#     if chain not in ['source','destination']:
#         print( f"Invalid chain: {chain}" )
#         return
    
#         #YOUR CODE HERE


#**************************************************************
# from web3 import Web3
# from web3.contract import Contract
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware #Necessary for POA chains
# import json
# import sys
# from pathlib import Path

# source_chain = 'avax'
# destination_chain = 'bsc'
# contract_info = "contract_info.json"

# def connectTo(chain):
#     if chain == 'avax':
#         api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

#     if chain == 'bsc':
#         api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

#     if chain in ['avax','bsc']:
#         w3 = Web3(Web3.HTTPProvider(api_url))
#         # inject the poa compatibility middleware to the innermost layer
#         w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#     return w3

# def getContractInfo(chain):
#     """
#         Load the contract_info file into a dictionary
#         This function is used by the autograder and will likely be useful to you
#     """
#     p = Path(__file__).with_name(contract_info)
#     try:
#         with p.open('r')  as f:
#             contracts = json.load(f)
#     except Exception as e:
#         print( "Failed to read contract info" )
#         print( "Please contact your instructor" )
#         print( e )
#         sys.exit(1)

#     return contracts[chain]

# def scanBlocks(chain):
#     """
#         chain - (string) should be either "source" or "destination"
#         Scan the last 5 blocks of the source and destination chains
#         Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
#         When Deposit events are found on the source chain, call the 'wrap' function on the destination chain
#         When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
#     """

#     if chain not in ['source','destination']:
#         print( f"Invalid chain: {chain}" )
#         return

#     # Load contract information
#     contracts = getContractInfo(chain)
#     if chain == 'source':
#         source_w3 = connectTo('avax')
#         destination_w3 = connectTo('bsc')
#         source_contract = source_w3.eth.contract(address=contracts['source_address'], abi=contracts['source_abi'])
#         destination_contract = destination_w3.eth.contract(address=contracts['destination_address'], abi=contracts['destination_abi'])
#     else:
#         source_w3 = connectTo('bsc')
#         destination_w3 = connectTo('avax')
#         source_contract = source_w3.eth.contract(address=contracts['destination_address'], abi=contracts['destination_abi'])
#         destination_contract = destination_w3.eth.contract(address=contracts['source_address'], abi=contracts['source_abi'])

#     latest_block = source_w3.eth.block_number
#     for block in range(latest_block - 5, latest_block + 1):
#         block = source_w3.eth.get_block(block, full_transactions=True)
#         for tx in block.transactions:
#             receipt = source_w3.eth.get_transaction_receipt(tx.hash)
#             if chain == 'source':
#                 for log in receipt.logs:
#                     if log.address.lower() == contracts['source_address'].lower() and 'Deposit' in log.topics:
#                         print(f"Found Deposit event: {log}")
#                         # Call wrap function on destination contract
#                         destination_contract.functions.wrap().transact({'from': contracts['warden_address']})
#             else:
#                 for log in receipt.logs:
#                     if log.address.lower() == contracts['destination_address'].lower() and 'Unwrap' in log.topics:
#                         print(f"Found Unwrap event: {log}")
#                         # Call withdraw function on source contract
#                         source_contract.functions.withdraw().transact({'from': contracts['warden_address']})

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python bridge.py [source|destination]")
#         sys.exit(1)

#     chain = sys.argv[1]
#     scanBlocks(chain)
# ****************************************************************

from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"
wallet_address = '0xeC7665898b9612714021fFf30fa177FF55A7772C'  # The account you want the funds in
private_key = '0xa7dee8d444ac14bf86f973ae3ee97f2a44e154b2267aec9796700342845c32b8'  # The secret key for your account

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts[chain]



def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return
    
        #YOUR CODE HERE
    def process_deposits(events):
        event_data = []
        for evt in events:
            data = {
                'chain': chain,
                'token': evt['args']['token'],
                'recipient': evt['args']['recipient'],
                'amount': evt['args']['amount'],
                'transactionHash': evt['transactionHash'].hex(),
                'address': evt['address'],
            }
            event_data.append(data)
        return event_data

    def process_unwraps(events):
        event_data = []
        for evt in events:
            data = {
                'chain': chain,
                'token': evt['args']['underlying_token'],
                'recipient': evt['args']['to'],
                'amount': evt['args']['amount'],
                'transactionHash': evt['transactionHash'].hex(),
                'address': evt['address'],
            }
            event_data.append(data)
        return event_data
        

    w3_src = connectTo('avax')
    w3_dst = connectTo('bsc')
    src_info = getContractInfo('source')
    dst_info = getContractInfo('destination')

    contract_src = w3_src.eth.contract(address=src_info['address'], abi=src_info['abi'])
    contract_dst = w3_dst.eth.contract(address=dst_info['address'], abi=dst_info['abi'])


    if chain == 'source':
      end_block = w3_src.eth.get_block_number()
      start_block = end_block - 5
      event_filter = contract_src.events.Deposit.create_filter(fromBlock=start_block, toBlock=end_block, argument_filters= {})
      events = event_filter.get_all_entries()
      event_data = process_deposits(events)
      for event in event_data:
        transaction=contract_dst.functions.wrap(event['token'], event['recipient'], event['amount']).build_transaction({
            'from': wallet_address,
            'nonce': w3_dst.eth.get_transaction_count(wallet_address),
            'gas': 200000,
            'gasPrice': w3_dst.to_wei('50', 'gwei')
        })

        signed_txn = w3_dst.eth.account.sign_transaction(transaction, private_key=private_key)
        txn_hash = w3_dst.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_dst.eth.wait_for_transaction_receipt(txn_hash)
    
    if chain == 'destination':
      end_block = w3_dst.eth.get_block_number()
      start_block = end_block - 5
      event_filter = contract_dst.events.Unwrap.create_filter(fromBlock=start_block, toBlock=end_block, argument_filters= {})
      events = event_filter.get_all_entries()
      #ADDDED START
      event_data = process_unwraps(events)
      for event in event_data:
          transaction=contract_src.functions.withdraw(event['token'], event['recipient'], event['amount']).build_transaction({
              'from': wallet_address,
              'nonce': w3_src.eth.get_transaction_count(wallet_address),
              'gas': 200000,
              'gasPrice': w3_src.to_wei('50', 'gwei')
          })

          signed_txn = w3_src.eth.account.sign_transaction(transaction, private_key=private_key)
          txn_hash = w3_src.eth.send_raw_transaction(signed_txn.rawTransaction)
          txn_receipt = w3_src.eth.wait_for_transaction_receipt(txn_hash)
      #ADDED END

 
      
