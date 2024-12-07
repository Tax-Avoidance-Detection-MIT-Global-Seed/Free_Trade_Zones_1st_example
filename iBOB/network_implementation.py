class Asset:
    """
    Represents an asset owned by an entity, tracking its name, type, basis, and fair market value (FMV).
    """

    def __init__(self, name, type_of_asset, basis, fmv=None):
        """
        Initialize an asset with its name, type, basis, and optional FMV.

        Args:
            name (str): The name of the asset (e.g., 'Promissory Note').
            type_of_asset (str): The category of the asset (e.g., 'Material', 'Annuity').
            basis (float): The original cost or tax basis of the asset.
            fmv (float, optional): The fair market value. Defaults to the basis if not provided.
        """
        self.name = name
        self.type_of_asset = type_of_asset
        self.basis = basis
        self.fmv = fmv if fmv is not None else basis  # Default FMV to basis if not specified

    def __repr__(self) -> str:
        """
        Return a string representation of the asset.

        Returns:
            str: A formatted string summarizing the asset's details.
        """
        return f"Asset({self.name}, type={self.type_of_asset}, basis={self.basis}, fmv={self.fmv})"
    


class PartnershipAsset:
    """
    Represents a partnership's share of an underlying asset, with dynamic FMV and static inside basis.
    """

    def __init__(self, original_asset, share, inside_basis):
        """
        Initialize a partnership asset.
        
        Args:
            original_asset: The underlying asset this partnership asset is derived from.
            share: The ownership share of this asset.
            inside_basis: The partnership's basis in this asset.
        """
        self.original_asset = original_asset  # Reference to the original asset for FMV updates.
        self.share = share  # Ownership percentage in the asset.
        self.inside_basis = inside_basis  # The basis attributed to this share.

    @property
    def fmv(self):
        """
        Calculate the fair market value (FMV) dynamically based on the share.
        """
        return self.original_asset.fmv * self.share

    @property
    def name(self):
        """
        Retrieve the name of the original asset, resolving through nested PartnershipAssets if needed.
        """
        current_asset = self.original_asset
        while isinstance(current_asset, PartnershipAsset):
            current_asset = current_asset.original_asset
        return current_asset.name

    @property
    def type_of_asset(self):
        """
        Retrieve the type of the original asset, resolving through nested PartnershipAssets if needed.
        """
        current_asset = self.original_asset
        while isinstance(current_asset, PartnershipAsset):
            current_asset = current_asset.original_asset
        return current_asset.type_of_asset

    def __repr__(self):
        """
        Return a string representation of the PartnershipAsset for debugging.
        """
        return f"PartnershipAsset({self.name}, Type of asset={self.type_of_asset}, Inside basis={self.inside_basis}, FMV={self.fmv})"
    


class Entity:
    """
    Represents an entity with direct assets, partnerships, and a cash balance.
    """

    def __init__(self, name, cash_balance):
        """
        Initialize an entity with a name, cash balance, and empty asset/partnership records.
        
        Args:
            name: The name of the entity.
            cash_balance: Initial cash balance of the entity.
        """
        self.name = name
        self.direct_assets = []  # List of assets directly owned by the entity.
        self.partnerships = {}  # Dictionary mapping partnerships to lists of PartnershipAssets.
        self.cash_balance = cash_balance  # The cash balance of the entity.

    def add_asset(self, asset, cash_amount=None):
        """
        Add an asset to the entity's list of direct assets.
        
        Args:
            asset: The asset to add.
            cash_amount: (Optional) Cash involved in the transaction.
        """
        self.direct_assets.append(asset)

    def add_partnership(self, partnership, partner_entity):
        """
        Add a partnership and update associated partnership assets.
        
        Args:
            partnership: Partnership object representing the new partnership.
            partner_entity: Entity that is the partner in the partnership.
        """
        if partnership not in self.partnerships:
            self.partnerships[partnership] = []  # Initialize partnership asset list.
        self.update_partnership_assets(partnership, partner_entity)

    def remove_asset(self, asset, cash_amount=None):
        """
        Remove an asset from the entity's list of direct assets.
        
        Args:
            asset: The asset to remove.
            cash_amount: (Optional) Cash involved in the transaction.
        """
        self.direct_assets.remove(asset)

    def update_partnership_assets(self, partnership, partner_entity):
        """
        Update the entity's list of PartnershipAssets for a given partnership.
        
        Args:
            partnership: The partnership being updated.
            partner_entity: The entity associated with the partnership.
        """
        self.partnerships[partnership] = []  # Clear current partnership assets.

        # Combine direct assets and partnership assets of the partner entity.
        all_partner_assets = partner_entity.direct_assets + sum(partner_entity.partnerships.values(), [])

        # Create new PartnershipAssets and add them to the partnership's asset list.
        for asset in all_partner_assets:
            partnership_asset = PartnershipAsset(
                original_asset=asset,
                share=partnership.share,
                inside_basis=asset.basis * partnership.share if isinstance(asset, Asset) else asset.inside_basis * partnership.share
            )
            self.partnerships[partnership].append(partnership_asset)

    def __repr__(self):
        """
        Return a string representation of the entity for debugging.
        """
        return (f"Entity({self.name}, Direct Assets={self.direct_assets}, "
                f"Partnerships={self.partnerships})")


class Partnership:
    """
    Represents a partnership between entities, tracking the partner entity and share of ownership.
    """

    def __init__(self, partner_name, share):
        """
        Initialize a partnership with a partner entity name and ownership share.
        
        Args:
            partner_name: The name of the partner entity in the partnership.
            share: The ownership share of this partnership (as a fraction).
        """
        self.partner_name = partner_name  # Name of the partner entity.
        self.share = share  # Ownership share in the partnership.

    def __repr__(self):
        """
        Return a string representation of the partnership for debugging.
        """
        return f"Partnership(Partner={self.partner_name}, Share={self.share})"
    

class Transaction:
    """
    Represents a transaction between two entities involving an exchange of goods or assets.
    """

    def __init__(self, entity1, entity2, good1, good2, election754=False):
        """
        Initialize a transaction between two entities.

        Args:
            entity1: The entity initiating the transaction.
            entity2: The counterparty in the transaction.
            good1: The asset or item provided by entity1.
            good2: The asset or item provided by entity2.
            election754 (bool): Indicates if a Section 754 election is applied for basis adjustment.
        """
        self.entity1 = entity1  # Entity initiating the transaction.
        self.entity2 = entity2  # Counterparty in the transaction.
        self.good1 = good1  # Asset provided by entity1.
        self.good2 = good2  # Asset provided by entity2.
        self.election754 = election754  # Basis adjustment election.

    def __repr__(self):
        """
        Return a string representation of the transaction for debugging.
        """
        return f"{self.entity1.name} gives {self.good1} to {self.entity2.name} for {self.good2}"
    
class Network:
    """
    Represents a network of entities, assets, and partnerships with tax tracking.
    """

    def __init__(self):
        """
        Initialize the network with structures for entities, assets, and tax records.
        """
        self.entities = {}  # Dictionary of all entities in the network.
        self.assets = {}  # Dictionary of all assets in the network.
        self.tax_records = {}  # Tracks tax liabilities for each entity.

    def add_entity(self, name, cash_amount):
        """
        Add a new entity to the network.

        Args:
            name (str): Name of the entity.
            cash_amount (float): Initial cash balance of the entity.

        Returns:
            Entity: The newly created entity.
        """
        entity = Entity(name, cash_amount)
        self.entities[name] = entity
        self.tax_records[name] = 0  # Initialize the tax liability for the entity.
        return entity

    def add_asset(self, owner, name, type_of_asset, basis, fmv=None):
        """
        Add a new asset to an entity in the network.

        Args:
            owner (Entity): The entity that owns the asset.
            name (str): Name of the asset.
            type_of_asset (str): Type/category of the asset.
            basis (float): The asset's tax basis.
            fmv (float, optional): The asset's fair market value. Defaults to the basis if not provided.

        Returns:
            Asset: The newly created asset.
        """
        asset = Asset(name, type_of_asset, basis, fmv)
        owner.add_asset(asset)
        self.assets[name] = asset
        self.update_initial_partnership_assets()  # Recalculate partnerships after adding the asset.
        return asset

    def add_partnership(self, entity1, partner_entity, share):
        """
        Add a partnership between two entities in the network.

        Args:
            entity1 (Entity): The entity initiating the partnership.
            partner_entity (Entity): The entity being partnered with.
            share (float): Ownership share of the partnership.

        Returns:
            Partnership: The newly created partnership.
        """
        partnership = Partnership(partner_entity.name, share)
        entity1.add_partnership(partnership, partner_entity)
        self.update_initial_partnership_assets()  # Recalculate partnerships after adding the partnership.
        return partnership

    def update_initial_partnership_assets(self):
        """
        Recalculate and update all partnership assets for each entity in the network.
        Ensures all entities have an up-to-date view of their partnerships.
        """
        for entity in self.entities.values():
            for partnership, assets in entity.partnerships.items():
                partner_entity = self.entities[partnership.partner_name]
                entity.update_partnership_assets(partnership, partner_entity)


    def is_transaction_viable(self, entity, good):
      """
      Verifies if a transaction involving an entity and a good (asset, partnership, or cash) is valid.

      Args:
          entity (Entity): The entity involved in the transaction.
          good (Asset/Partnership/float): The item (asset, partnership, or cash amount) to check.

      Raises:
          ValueError: If the entity does not own the good or has insufficient cash balance.
      """
      if isinstance(good, Asset) and good not in entity.direct_assets:
          # Check if the entity owns the specified asset
          raise ValueError(f"{entity.name} does not own asset {good}.")
      elif isinstance(good, Partnership) and good not in entity.partnerships:
          # Check if the entity has a partnership with the specified partner
          raise ValueError(f"{entity.name} does not have a partnership with {good.partner_name}.")
      elif isinstance(good, (int, float)) and entity.cash_balance < good:
          # Check if the entity has enough cash balance for the transaction
          raise ValueError(f"{entity.name} does not have enough cash balance to perform the transaction.")


    def add_asset_upstream(self, entity, good):
      """
      Recursively propagate an asset's reference to all upstream partners of a given entity.

      Args:
          entity (Entity): The entity whose upstream partners will receive the asset reference.
          good (Asset/PartnershipAsset): The asset or partnership asset being propagated upstream.

      Purpose:
          Ensures that all upstream partners of an entity have an updated reference to the asset,
          reflecting the entity's ownership in their partnership assets.
      """
      for other_entity in self.entities.values():
          # Iterate over all entities in the network
          for partnership in other_entity.partnerships.keys():
              if partnership.partner_name == entity.name:
                  # If a partnership points to the given entity, propagate the asset upstream
                  new_asset = PartnershipAsset(
                      original_asset=good,
                      share=partnership.share,
                      inside_basis=(good.basis * partnership.share
                                    if isinstance(good, Asset) else
                                    good.inside_basis * partnership.share)
                  )
                  # Add the newly created partnership asset to the upstream partner's partnership
                  other_entity.partnerships[partnership].append(new_asset)

                  # Recursively propagate the asset further upstream
                  self.add_asset_upstream(other_entity, new_asset)


    def remove_asset_upstream(self, entity, good):
      """
      Recursively remove references to a specific asset from all upstream partners of a given entity.

      Args:
          entity (Entity): The entity whose upstream partners are checked for asset removal.
          good (Asset/PartnershipAsset): The asset or partnership asset to be removed.

      Purpose:
          Ensures that all upstream partners of an entity no longer reference the asset
          once it is removed from the entity.
      """
      for other_entity in self.entities.values():
          # Iterate through all entities in the network
          for partnership in other_entity.partnerships.keys():
              if partnership.partner_name == entity.name:
                  # Check if the partnership points to the given entity
                  for partner_asset in other_entity.partnerships[partnership]:
                      if partner_asset.name == good.name:
                          # Remove the asset if it matches the specified one
                          other_entity.partnerships[partnership].remove(partner_asset)

                          # Recursively remove the asset from further upstream partners
                          self.remove_asset_upstream(other_entity, partner_asset)


    def add_partnership_upstream(self, entity, partnership_of_interest):
      """
      Recursively propagate the addition of partnership assets to all upstream partners of a given entity.

      Args:
          entity (Entity): The entity whose upstream partners will receive the partnership assets.
          partnership_of_interest (Partnership): The specific partnership being propagated upstream.

      Purpose:
          Ensures that partnership assets are correctly propagated to all upstream entities 
          that have a share in the given entity.
      """
      for other_entity in self.entities.values():
          # Iterate through all entities in the network
          for partnership, assets in other_entity.partnerships.items():
              if partnership.partner_name == entity.name:
                  # Check if the partnership points to the given entity
                  new_partner_assets = entity.partnerships[partnership_of_interest]
                  for new_asset in new_partner_assets:
                      # Create a new PartnershipAsset for the upstream partner
                      partner_asset = PartnershipAsset(
                          original_asset=new_asset,
                          share=partnership.share,
                          inside_basis=new_asset.basis * partnership.share if isinstance(new_asset, Asset) else new_asset.inside_basis * partnership.share
                      )
                      # Append the newly created asset to the upstream partner's partnership list
                      other_entity.partnerships[partnership].append(partner_asset)

                  # Recursively propagate the partnership upstream
                  self.add_partnership_upstream(other_entity, partnership)


    def remove_partnership_upstream(self, entity, partnership_of_interest):
      """
      Recursively removes references to partnership assets in upstream partnerships.

      Args:
          entity (Entity): The entity whose upstream partners are checked for asset removal.
          partnership_of_interest (Partnership): The specific partnership whose assets are being removed.

      Purpose:
          Ensures that any assets associated with the given partnership are removed 
          from all upstream partners in the network.
      """
      # Retrieve the assets tied to the partnership of interest
      old_partner_assets = entity.partnerships.get(partnership_of_interest, [])
      # Create a set of asset names to identify assets to be removed
      asset_names_to_remove = {asset.name for asset in old_partner_assets}

      # Iterate through all entities in the network
      for other_entity in self.entities.values():
          # Check for partnerships pointing to the current entity
          for partnership, partner_assets in other_entity.partnerships.items():
              if partnership.partner_name == entity.name:
                  # Filter out assets matching the names in asset_names_to_remove
                  partner_assets[:] = [
                      pa for pa in partner_assets if pa.name not in asset_names_to_remove
                  ]
                  # Recursively remove assets from upstream partnerships
                  self.remove_partnership_upstream(other_entity, partnership)


    def adjust_ownership(self, entity_from, entity_to, good):
      """
      Adjusts the ownership of a good (asset, partnership, or cash) between two entities.

      Args:
          entity_from (Entity): The entity transferring ownership of the good.
          entity_to (Entity): The entity receiving ownership of the good.
          good: The item being transferred (Asset, Partnership, or cash).
          other_good: The item exchanged for the transferred good (used for basis adjustments).

      Purpose:
          Transfers ownership of an asset or partnership from one entity to another while updating
          related upstream and downstream partnerships. For cash, updates the balances of the involved entities.
      """

      if isinstance(good, Asset):
          # Adjust the basis of the asset to match the FMV of the exchanged good
          good.basis = good.fmv

          # Add the asset to the receiving entity
          entity_to.add_asset(good)  # Add to direct assets
          self.add_asset_upstream(entity_to, good)  # Add to upstream partnerships

          # Remove the asset from the transferring entity
          entity_from.remove_asset(good)  # Remove from direct assets
          self.remove_asset_upstream(entity_from, good)  # Remove from upstream partnerships

      elif isinstance(good, Partnership):
          # Transfer the partnership and its associated assets
          partner_assets = entity_from.partnerships[good]
          entity_to.partnerships[good] = partner_assets  # Add partnership assets to receiving entity
          self.add_partnership_upstream(entity_to, good)  # Add partnership assets upstream

          # Remove the partnership and its assets from the transferring entity
          self.remove_partnership_upstream(entity_from, good)  # Remove from upstream partnerships
          del entity_from.partnerships[good]  # Remove from direct partnerships

      elif isinstance(good, (int, float)):
          # Adjust the cash balances of the entities
          entity_from.cash_balance -= good  # Deduct cash from transferring entity
          entity_to.cash_balance += good  # Add cash to receiving entity



    def adjust_partner_basis(self, transaction):
      """
      Adjusts the basis of partnership assets in a transaction if a Section 754 election is in effect.

      Args:
          transaction (Transaction): The transaction containing entities, goods, and election information.

      Purpose:
          Handles the adjustment of inside basis for partnership assets when a Section 754 election is triggered.
          Ensures changes are propagated upstream to all relevant partnerships.

      Details:
          - Adjusts the inside basis for partnership assets held by the entity transferring the partnership.
          - Updates inside basis for partnerships upstream using recursive methods.
      """

      # Extract transaction details
      entity1, entity2, good1, good2 = transaction.entity1, transaction.entity2, transaction.good1, transaction.good2

      # Adjust inside basis for assets within a partnership held by entity1
      if isinstance(good1, Partnership):
          partnership_assets = entity1.partnerships[good1]
          for partner_asset in partnership_assets:
              # Calculate basis adjustment for each partner asset based on the type of the exchanged good
              if isinstance(good2, Asset):
                  adjustment1 = good2.basis - partner_asset.inside_basis
              elif isinstance(good2, PartnershipAsset):
                  adjustment1 = good2.inside_basis - partner_asset.inside_basis
              else:
                  adjustment1 = good2 - partner_asset.inside_basis
              # Apply the basis adjustment
              partner_asset.inside_basis += adjustment1

          # Update upstream partnerships for entity1
          self.remove_partnership_upstream(entity1, good1)
          self.add_partnership_upstream(entity1, good1)

      # Adjust inside basis for assets within a partnership held by entity2
      if isinstance(good2, Partnership):
          partnership_assets = entity2.partnerships[good2]
          for partner_asset in partnership_assets:
              # Calculate basis adjustment for each partner asset based on the type of the exchanged good
              if isinstance(good1, Asset):
                  adjustment2 = good1.basis - partner_asset.inside_basis
              elif isinstance(good1, PartnershipAsset):
                  adjustment2 = good1.inside_basis - partner_asset.inside_basis
              else:
                  adjustment2 = good1 - partner_asset.inside_basis
              # Apply the basis adjustment
              partner_asset.inside_basis += adjustment2

          # Update upstream partnerships for entity2
          self.remove_partnership_upstream(entity2, good2)
          self.add_partnership_upstream(entity2, good2)


    def has_substantial_built_in_loss(self, good, entity):
        """
        Determines whether there is a substantial built-in loss for a given good.

        Args:
            good (Asset or Partnership): The asset or partnership to evaluate.
            entity (Entity): The entity that owns the good.

        Returns:
            bool: True if the built-in loss exceeds $250,000, False otherwise.

        Purpose:
            Identifies whether a transaction involves a significant loss that may require
            special handling under tax rules (e.g., triggering Section 754 elections).

        Details:
            - For assets, the built-in loss is calculated as the difference between basis and FMV.
            - For partnerships, the built-in loss is the sum of differences between the inside basis
              and FMV of all partnership assets held by the entity.
        """
        loss = 0

        # Calculate loss for an individual asset
        if isinstance(good, Asset):
            loss = good.basis - good.fmv

        # Calculate aggregate loss for all assets in a partnership
        elif isinstance(good, Partnership):
            for partner_asset in entity.partnerships[good]:
                loss += partner_asset.inside_basis - partner_asset.fmv if partner_asset.type_of_asset != "Annuity" else 0

        # Return True if the total loss exceeds the threshold, otherwise False
        return loss > 250000


    def process_transaction(self, transaction):
        """
        Handles the processing of a transaction between two entities, including
        ownership adjustments, tax calculations, and basis updates.

        Args:
            transaction (Transaction): The transaction object containing details
            about the entities involved, the goods being exchanged, and election status.

        Purpose:
            - Ensures the transaction is valid.
            - Handles necessary basis adjustments.
            - Calculates and records any tax liability.
            - Updates ownership of the exchanged goods.

        Steps:
            1. Validate the transaction by checking ownership of the goods.
            2. Adjust the basis of assets or partnerships if conditions (e.g., Section 754 election) are met.
            3. Compute and record tax liabilities for each entity involved.
            4. Finalize the transaction by updating the ownership of the goods.

        Workflow:
        """
        entity1, entity2, good1, good2 = transaction.entity1, transaction.entity2, transaction.good1, transaction.good2

        # Step 1: Validate the transaction
        self.is_transaction_viable(entity1, good1)
        self.is_transaction_viable(entity2, good2)

        # Step 2: Adjust basis if needed
        if transaction.election754 or self.has_substantial_built_in_loss(good1, entity1) or self.has_substantial_built_in_loss(good2, entity2):
            self.adjust_partner_basis(transaction)

        # Step 3: Calculate tax liabilities for the involved entities
        self.determine_tax(entity1, good1)
        self.determine_tax(entity2, good2)

        # Step 4: Adjust ownership of the exchanged goods
        self.adjust_ownership(entity1, entity2, good1)
        self.adjust_ownership(entity2, entity1, good2)


    def determine_tax(self, entity_from, good):
        """
        Calculates the tax liability for a given entity and good (asset or partnership) being sold.

        Args:
            entity_from (Entity): The entity selling the asset or partnership.
            good (Asset/Partnership): The good being sold.

        Purpose:
            - Compute the tax liability for a sale based on the difference between FMV and basis.
            - Adjust for remaining shares not allocated to partners.
            - Recursively calculate tax for upstream partners.

        Workflow:
            1. For an asset, calculate tax directly unless it's an annuity.
            2. For a partnership, calculate tax based on its assets' FMV and basis.
            3. Recursively compute tax for upstream partners.
        """

        if isinstance(good, Asset):
            if good.type_of_asset != "Annuity":
                # Step 1: Calculate partner shares and remaining share
                partner_share_sum = sum(
                    partnership.share
                    for entity in self.entities.values()
                    for partnership in entity.partnerships
                    if partnership.partner_name == entity_from.name
                )
                remaining_share = 1 - partner_share_sum

                # Step 2: Compute tax liability
                tax_amount = remaining_share * (good.fmv - good.basis)

                # Step 3: Store tax liability
                self.tax_records[entity_from.name] += tax_amount

                # Step 4: Recursively calculate tax for upstream partners
                self._calculate_partner_tax_asset(entity_from, good)

        elif isinstance(good, Partnership):
            # Step 1: Calculate partner shares and remaining share
            partner_share_sum = sum(
                partnership.share
                for entity in self.entities.values()
                for partnership in entity.partnerships
                if partnership.partner_name == entity_from.name
            )
            remaining_share = 1 - partner_share_sum

            # Step 2: Sum FMV and inside basis of partnership assets (excluding annuities)
            total_fmv = sum(
                partner_asset.fmv
                for partner_asset in entity_from.partnerships[good]
                if partner_asset.type_of_asset != "Annuity"
            )
            total_inside_basis = sum(
                partner_asset.inside_basis
                for partner_asset in entity_from.partnerships[good]
                if partner_asset.type_of_asset != "Annuity"
            )

            # Step 3: Compute tax liability
            tax_amount = remaining_share * (total_fmv - total_inside_basis)

            # Step 4: Store tax liability
            self.tax_records[entity_from.name] += tax_amount

            # Step 5: Recursively calculate tax for upstream partners
            self._calculate_partner_tax_partnership(entity_from)


    def _calculate_partner_tax_asset(self, entity, asset):
      """
      Recursively calculates tax for partners who hold a share in the specified asset.

      Args:
          entity (Entity): The entity selling the asset or partnership asset.
          asset (Asset or PartnershipAsset): The asset or partnership asset being sold.

      Purpose:
          - Ensures tax liability is distributed among partners based on their share.
          - Recursively propagates tax calculations upstream to account for multi-layer partnerships.
      """
      for other_entity in self.entities.values():  # Iterate over all entities in the network
          for partnership in other_entity.partnerships:  # Check partnerships in each entity
              if partnership.partner_name == entity.name:
                  # Identify assets linked to the sold asset
                  for partner_asset in other_entity.partnerships[partnership]:
                      if partner_asset.name == asset.name:  # Match based on asset name
                          # Calculate partner's tax based on their share and inside basis
                          partner_share_sum = sum(
                              p.share
                              for e in self.entities.values()
                              for p in e.partnerships
                              if p.partner_name == other_entity.name
                          )
                          remaining_share = 1 - partner_share_sum
                          tax_amount = remaining_share * (partner_asset.fmv - partner_asset.inside_basis)
                          
                          # Update the tax record for the partner entity
                          self.tax_records[other_entity.name] += tax_amount

                          # Recursively propagate tax calculations to upstream partners
                          self._calculate_partner_tax_asset(other_entity, partner_asset)


    def _calculate_partner_tax_partnership(self, entity):
        """
        Recursively calculates tax for partners who hold a share in the partnership.

        Args:
            entity (Entity): The entity selling the partnership or partnership assets.

        Purpose:
            - Distribute tax liability among partners based on their share in the partnership.
            - Recursively propagate tax calculations upstream through partnerships.
        """
        for other_entity in self.entities.values():  # Iterate over all entities in the network
            for partnership in other_entity.partnerships:  # Check partnerships in each entity
                if partnership.partner_name == entity.name:  # Match partnerships pointing to the selling entity
                    # Calculate the sum of partner shares in the entity
                    partner_share_sum = sum(
                        p.share
                        for e in self.entities.values()
                        for p in e.partnerships
                        if p.partner_name == other_entity.name
                    )
                    remaining_share = 1 - partner_share_sum  # Determine the share not owned by other partners

                    # Compute FMV and inside basis for non-annuity assets in the partnership
                    total_fmv = sum(
                        partner_asset.fmv
                        for partner_asset in other_entity.partnerships[partnership]
                        if partner_asset.type_of_asset != "Annuity"
                    )
                    total_inside_basis = sum(
                        partner_asset.inside_basis
                        for partner_asset in other_entity.partnerships[partnership]
                        if partner_asset.type_of_asset != "Annuity"
                    )

                    # Calculate the tax liability for the remaining share
                    tax_amount = remaining_share * (total_fmv - total_inside_basis)

                    # Update the tax record for the partner entity
                    self.tax_records[other_entity.name] += tax_amount

                    # Recursively calculate tax for upstream partnerships
                    self._calculate_partner_tax_partnership(other_entity)

    def tax_liability(self):
        """
        Calculate the total tax liability across all entities in the network.

        Returns:
            float: Sum of all tax records in the network.
        """
        return sum(self.tax_records.values())


    def cash_balance(self):
        """
        Calculate the total cash balance across all entities in the network.

        Returns:
            float: Sum of cash balances for all entities.
        """
        return sum(entity.cash_balance for entity in self.entities.values())


    def fitness(self):
        """
        Compute the network's fitness as the difference between total cash balance and tax liability.

        Returns:
            float: The network's fitness, calculated as total cash - total tax.
        """
        return self.cash_balance() - self.tax_liability()


    def __repr__(self):
        return f"Network(Entities={list(self.entities.keys())}, Assets={list(self.assets.keys())}), Tax Records={self.tax_records})"
    

