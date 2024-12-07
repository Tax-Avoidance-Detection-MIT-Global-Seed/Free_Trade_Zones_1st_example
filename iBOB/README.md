# iBOB Implementation
[Based on iBOB Scheme, found here](iBOB%20Scheme.png)

[Network implementation, found here](network_implementation.py)

[Network test, found here](network_test.py)

## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
- [Initialization State](#initialization-state)
- [Processing a Transaction](#processing-a-transaction)
- [Adjusting Basis](#adjusting-basis)
- [Tax Liability Calculation](#tax-liability-calculation)
- [Measuring Fitness](#measuring-fitness)
- [Adjusting Ownership](#adjusting-ownership)
- [Key Assumptions and Limitations](#key-assumptions-and-limitations)
- [Next Steps](#next-steps)

---

## Overview

This project models a network of entities, assets, and partnerships to simulate transactions and evaluate their taxes. The workflow consists of initializing the network and processing proposed transactions. The key steps include:

1. **Initialize the Network**: 
   - Create entities (e.g., individuals, companies, trusts) and assign initial assets, cash balances, and partnerships.
   - Ensure all entities are set up with a tax liability of 0, direct assets with unique names, and partner assets based on their partnerships.

2. **Evaluate Proposed Transactions**:
   - **Transaction Validation**: Check if the entities involved own the goods they are attempting to trade or have sufficient cash.
   - **Adjust Partner Inside Basis**: If applicable, adjust the inside basis of partnership assets per Section 754 or when there is a substantial built-in loss.
   - **Determine Tax Liability**: Calculate the tax liability for the transaction based on the difference between FMV and basis. Tax liability is recursively propagated to upstream partners when applicable.
   - **Adjust Ownership and Network State**: Update ownership of assets, partnerships, or cash between the entities, and propagate changes to upstream partners

3. **Evaluate Fitness**:
   - Fitness is calculated as the difference between the total cash held by all entities and the total tax liability across the network. This ensures we maximize cash while minimizing tax liabilities.

Each step in the process is described in detail below.

---
## Classes

### Asset
Represents an individual asset owned by an entity.

- **Attributes**:
  - `name`: Name of the asset.
  - `type_of_asset`: Type of asset (e.g., material, annuity).
  - `basis`: The tax basis of the asset.
  - `fmv`: The fair market value of the asset (defaulted to `basis` if not provided).

- **Key Methods**:
  - `__repr__`: Provides a string representation of the asset.

### PartnershipAsset
Represents a fractional share of an asset owned through a partnership.

- **Attributes**:
  - `original_asset`: The underlying asset this share is derived from.
  - `share`: The percentage share of the original asset.
  - `inside_basis`: The share of the basis allocated to this partnership asset.

- **Key Properties**:
  - `fmv`: Dynamically calculates the fair market value based on the `share`.
  - `name`: Retrieves the name of the underlying asset.
  - `type_of_asset`: Retrieves the type of the underlying asset.

- **Key Methods**:
  - `__repr__`: Provides a string representation of the partnership asset.

### Entity
Represents an individual or business with assets and partnerships.

- **Attributes**:
  - `name`: Name of the entity.
  - `cash_balance`: Total cash available to the entity.
  - `direct_assets`: A list of directly owned assets.
  - `partnerships`: A dictionary where keys are partnerships, and values are lists of `PartnershipAsset` objects.

- **Key Methods**:
  - `add_asset(asset)`: Adds a direct asset to the entity.
  - `add_partnership(partnership, partner_entity)`: Adds a partnership and updates the associated partnership assets.
  - `update_partnership_assets(partnership, partner_entity)`: Updates partnership assets based on partner entity's assets.
  - `__repr__`: Provides a string representation of the entity.

### Transaction
Represents a transaction between two entities involving the exchange of goods or partnerships.

- **Attributes**:
  - `entity1`: The entity initiating the transaction.
  - `entity2`: The receiving entity.
  - `good1`: The item being transferred from `entity1`.
  - `good2`: The item being exchanged by `entity2`.
  - `election754`: Boolean indicating if Section 754 election applies.

- **Key Methods**:
  - `__repr__`: Provides a description of the transaction.


### Network
Manages all entities, assets, and transactions in the system.

- **Attributes**:
  - `entities`: A dictionary of all entities in the network.
  - `assets`: A dictionary of all assets in the network.
  - `tax_records`: A dictionary tracking tax liabilities for each entity.

- **Key Methods**:
  - `add_entity(name, cash_amount)`: Adds a new entity to the network.
  - `add_asset(owner, name, type_of_asset, basis, fmv)`: Adds a new asset to an entity.
  - `add_partnership(entity1, partner_entity, share)`: Creates a partnership and updates the associated partnership assets.
  - `process_transaction(transaction)`: Processes a transaction, updating ownership, basis, and tax liabilities.
  - `determine_tax(entity_from, good)`: Calculates and records tax liabilities for a transaction.
  - `fitness()`: Measures the overall financial health of the network.


---
## Initialization State

### Entities
The network starts with the following five entities:
- **Mr. Jones**
- **JonesCo**
- **NewCo**
- **FamilyTrust**
- **Mr. Brown**

Each entity is initialized with:
- A **cash balance** of `1,000,000`.
- **Three promissory notes** as direct assets:
  - Named uniquely (e.g., `Promissory Note 1 Mr. Jones`, `Promissory Note 2 Mr. Jones`, etc.).
  - **Type**: `"Annuity"`.
  - **Basis**: `100`, `200`, and `300`.

### Partnerships
The following partnerships are established:
1. **Mr. Jones** owns 99% of **JonesCo**.
2. **Mr. Jones** owns 99% of **FamilyTrust**.
3. **JonesCo** owns 99% of **NewCo**.

### Tax Liability
- Each entity begins with a **tax liability of 0**.

### Network Structure
The network maintains:
- A **global list of entities, assets, and tax liabilities**.

---
## Processing a Transaction (Overview)

The network processes transactions in the following steps:

1. **Assess Transaction Viability**
   - Ensure that entities hold the goods (assets, partnerships, or cash) they are attempting to trade.
   - Verify that entities have sufficient cash balances or ownership shares for the transaction.

2. **Adjust Partner Inside Basis (Section 743)**
   - If a transaction triggers a **Section 743 adjustment**, the network adjusts the inside basis of relevant partners' assets and partnerships.
   - For more details on Section 743, refer to [26 U.S. Code § 743](https://www.law.cornell.edu/uscode/text/26/743).
   - For details on how basis adjustments are handled, refer to the [Adjusting Basis](#adjusting-basis) section.  

3. **Determine and Update Tax Liability**
   - Calculate the tax liability incurred by each entity in the transaction.
   - Update the network’s tax records to reflect the new liabilities.
   - For details on how taxes are calculated, refer to the [Tax Liability Calculation](#tax-liability-calculation) section.  

4. **Execute the Transaction**
   - Transfer ownership of goods (assets, partnerships, or cash) between entities.
   - Propagate changes upward to adjust partnership assets and shares as necessary.
   - Ensure the state of the network is consistent after the transaction
   - For details on how the network is updated, refer to the [Adjusting Ownership](#adjusting-ownership) section.  


---
## Adjusting Basis
[To see an example of the adjusting basis decision tree, go here.](Adjust%20Basis%20Tree.jpg) 

 Basis adjustments occur under the following conditions:
1. A **Section 754 election** is made during the transaction, and at least one of the goods is a partnership.
2. The transaction involves a **substantial built-in loss**, as determined by the following conditions:
   - For an individual asset, the loss is calculated as the difference between its basis and fair market value (FMV).
   - For partnerships, the loss is the sum of differences between the inside basis and FMV of all partnership assets held by the entity.
   - A loss exceeding $250,000 triggers a substantial built-in loss

### Process of Adjusting Basis
When a basis adjustment is triggered, the following steps are performed:

1. **Evaluate the Transaction**:
   - Extract the entities and goods involved in the transaction.
   - Identify if a Section 754 election or substantial built-in loss is present.

2. **Adjust Inside Basis for Partnership Assets**:
   - If a partnership is being transferred, adjust the inside basis of its assets based on the basis of the exchanged good.
   - The adjustment is calculated as the difference between the exchanged good's basis and the partner asset's inside basis.
   - Adjust all partner assets in the portfolio.

3. **Propagate Changes Upstream**:
   - After adjusting the basis, propagate the changes upstream to all partnerships that hold an interest in the modified entity.
   - Use recursive methods to update the inside basis for all relevant upstream partnerships.

---
## Tax Liability Calculation

### Direct Tax Liability
[To see an example of the tax decision tree, go here.](Tax%20Tree.jpg)  

1. **For Assets**:
  [To see an example of a tax calculation, go here.](Tax%20Example%20Material.pdf)

   - **Entity's Liability**:
     The tax liability is calculated based on the entity's remaining share of the asset's FMV minus its basis:
     ```
     Tax Liability = (1 - Partner Shares) × (FMV - Basis)
     ```
   - **Partners' Liability**:
     For partners of the entity, the tax is calculated as:
     ```
     Tax Liability = (1 - Partner Shares) × (Internal FMV - Internal Basis)
     ```
     where the internal FMV and basis are derived by multiplying the asset's FMV and basis by the partner's share.

   - **Exclusion**:
     Annuities are excluded from tax calculations.

3. **For Partnerships**:
     [To see an example of a tax calculation, go here.](Tax%20Example%20Partnership.pdf)
   
   - The tax is determined by summing the **internal FMV** and **inside basis** of all non-annuity assets within the partnership:
     ```
     Tax Liability = (1 - Partner Shares) × (Total Internal FMV - Total Inside Basis)
     ```

### Storing Tax Liability
- Each entity's tax liability is updated in the `tax_records` dictionary after transactions involving their assets or partnerships.


### Recursive Partner Tax Liability

1. **For Assets**:
   - The `_calculate_partner_tax_asset` function computes tax liability for partners holding a share in the sold asset.
   - Liability is recursively propagated to upstream partners, ensuring multi-layer partnerships are fully accounted for.

2. **For Partnerships**:
   - The `_calculate_partner_tax_partnership` function computes tax liability for partners holding a share in the sold partnership.
   - Liability is recursively propagated through all upstream partnerships, ensuring accurate distribution across the network.
---

## Adjusting Ownership

The **Adjusting Ownership** section manages the transfer of assets, partnerships, or cash between entities. It ensures that changes in ownership are properly reflected across all direct and upstream partnerships. Here's a breakdown of the key functions:

### Adding Assets Upstream
The `add_asset_upstream` function propagates a transferred asset to all upstream partners of the receiving entity. For each upstream partner:
- A new `PartnershipAsset` is created, reflecting the partner's share in the asset.
- The function recursively propagates the asset further upstream.

### Removing Assets Upstream
The `remove_asset_upstream` function ensures that once an asset is removed from an entity, all upstream references to the asset are also removed. It:
- Iterates through all entities with partnerships pointing to the given entity.
- Removes matching assets and recursively propagates the removal.

### Adding Partnerships Upstream
The `add_partnership_upstream` function propagates new partnership assets to upstream partners. For each upstream partner:
- Partnership assets of the new partnership are shared proportionally.
- This is recursively applied to ensure all upstream partnerships are updated.

### Removing Partnerships Upstream
The `remove_partnership_upstream` function removes references to a partnership's assets from upstream partnerships. It:
- Identifies all assets associated with the partnership.
- Removes these assets from upstream entities recursively.

### Adjusting Ownership
The `adjust_ownership` function performs the core transfer of ownership for assets, partnerships, or cash:
1. **Assets**:
   - The basis of the asset is adjusted to its FMV.
   - The asset is added to the receiving entity and propagated upstream.
   - It is removed from the transferring entity and upstream partnerships.
2. **Partnerships**:
   - Partnership assets are transferred to the receiving entity.
   - These changes are propagated upstream and removed from the transferring entity.
3. **Cash**:
   - The cash balances of both entities are updated to reflect the transfer.

This process ensures that ownership transfers are seamless and consistent across the network, maintaining accurate records for direct and upstream relationships.

---
## Measuring Fitness

Fitness is calculated as the total cash balance of all entities minus their total tax liabilities:

This metric ensures we aim to maximize cash while minimizing tax liability, promoting an efficient and optimized network.

---


## Key Assumptions and Limitations

The implementation has the following key assumptions and limitations:

- **Unique Asset Names**:  
  All assets must have unique names to ensure proper tracking and avoid ambiguity. For example, promissory notes are distinctly named for each entity.

- **Inside Basis Propagation**:  
  Any change in the inside basis of a partner asset is propagated upwards to all upstream partners or entities linked through partnerships. This ensures accurate and consistent basis adjustments across the network.

- **Basis Adjustment on Sale**:  
  When an asset is sold, its basis is adjusted to match its Fair Market Value (FMV). This aligns with the assumption that the selling entity received compensation equal to the FMV.

- **Tax Calculation**:  
  Taxes are paid on the difference between the FMV and the Basis of the sold asset or partnership, assuming the selling price equals the FMV. This applies to all taxable transactions in the network.

These assumptions simplify the logic while capturing the essential tax and basis adjustment behaviors but may not cover more complex real-world scenarios.

---

## Next Steps

1. **GPT Agent**:  
   - Prompt GPT for transaction sequences and evaluate each sequence by returning errors and fitness results.  
   - Use GPT to mutate transactions from previous sequences.  
   - Train over generations to see if the system arrives at the iBOB sequence.

2. **Compare to Existing Tax Calculator**:  
   Evaluate the performance of the implementation against a standard tax calculator.

3. **Stretch Goal**:  
   Revisit the implementation to simplify or enhance functionality. Change the implementation of annuities. 







