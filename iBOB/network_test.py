from network_implementation import *

# Create the network
network = Network()

# Create entities
mr_jones = network.add_entity("Mr. Jones", 1000000)
jones_co = network.add_entity("JonesCo", 1000000)
new_co = network.add_entity("NewCo", 1000000)
family_trust = network.add_entity("FamilyTrust",1000000)
mr_brown = network.add_entity("Mr. Brown", 1000000)


#Add hotel and promissory note
hotel=network.add_asset(new_co, "Hotel", "Material", basis=120, fmv=200)
promissory1_mrjones=network.add_asset(mr_jones, "Promissory Note 1 Mr Jones", "Annuity", basis=100)
promissory2_mrjones=network.add_asset(mr_jones, "Promissory Note 2 Mr Jones", "Annuity", basis=200)
promissory3_mrjones=network.add_asset(mr_jones, "Promissory Note 3 Mr Jones", "Annuity", basis=300)

promissory1_jonesco=network.add_asset(jones_co, "Promissory Note 1 Jones Co", "Annuity", basis=100)
promissory2_jonesco=network.add_asset(jones_co, "Promissory Note 2 Jones Co", "Annuity", basis=200)
promissory3_jonesco=network.add_asset(jones_co, "Promissory Note 3 Jones Co", "Annuity", basis=300)

promissory1_newco=network.add_asset(new_co, "Promissory Note 1 New Co", "Annuity", basis=100)
promissory2_newco=network.add_asset(new_co, "Promissory Note 2 New Co", "Annuity", basis=200)
promissory3_newco=network.add_asset(new_co, "Promissory Note 3 New Co", "Annuity", basis=300)

promissory1_familytrust=network.add_asset(family_trust, "Promissory Note 1 Family Trust", "Annuity", basis=100)
promissory2_familytrust=network.add_asset(family_trust, "Promissory Note 2 Family Trust", "Annuity", basis=200)
promissory3_familytrust=network.add_asset(family_trust, "Promissory Note 3 Family Trust", "Annuity", basis=300)

promissory1_mrbrown=network.add_asset(mr_brown, "Promissory Note 1 Mr Brown", "Annuity", basis=100)
promissory2_mrbrown=network.add_asset(mr_brown, "Promissory Note 2 Mr Brown", "Annuity", basis=200)
promissory3_mrbrown=network.add_asset(mr_brown, "Promissory Note 3 Mr Brown", "Annuity", basis=300)

#Add partnerships
partnership1=network.add_partnership(mr_jones, jones_co, share=0.99)
partnership2=network.add_partnership(mr_jones, family_trust, share=0.99)
partnership3=network.add_partnership(jones_co, new_co, share=0.99)

#Proposed transaction sequence
transaction1=Transaction(jones_co, family_trust, good1=partnership3, good2=promissory2_familytrust, election754=False)
transaction2=Transaction(new_co, mr_brown, good1=hotel, good2=200)
transaction_sequence= [transaction1, transaction2]

# Display the network structure
print('BEFORE')
print('Network', network)
print('Total tax liability', network.tax_liability(), '\n')
print('Total cash balance', network.cash_balance(), '\n')
print('Total fitness (cash-tax)', network.fitness(), '\n')


for transaction in transaction_sequence:
  print('-----------------------------------')
  print('NEW TRANSACTION', transaction)
  network.process_transaction(transaction)
  print('Network', network)
  print('Total tax liability', network.tax_liability(), '\n')
  print('Total cash balance', network.cash_balance(), '\n')
  print('Total fitness (cash-tax)', network.fitness(), '\n')

  for entity_name, entity in network.entities.items():
    print(f"{entity.name} owns direct assets: {entity.direct_assets}")
    print(f"{entity.name} has cash balance: {entity.cash_balance}")
    print(f"{entity.name} has partnerships: {entity.partnerships}", '\n')
