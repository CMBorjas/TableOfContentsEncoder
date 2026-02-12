import asyncio
import os
from typing import List

from .models import TOCItem, EncodedItem, EncodingResult
from ..mnemonic.loci_engine import LociEngine
from ..mnemonic.actor_engine import ActorEngine
from ..mnemonic.scent_engine import ProustScentEngine
from ..mnemonic.imagery_engine import AbsurdImageryEngine
from ..pdf_parser import extract_toc, extract_text_from_pdf
from ..db.database import Database

class TOCController:
    
    def __init__(self):
        self.db = Database()

    async def process_file(self, filepath: str) -> EncodingResult:
        """
        Orchestrates the processing of a PDF file:
        1. Extract TOC
        2. Encode each item (Async) with DB persistence
        3. Return result
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        # Compute Book Hash for Persistence
        book_hash = self.db.compute_book_hash(filepath)
        print(f"Book Hash: {book_hash}")

        # 1. Extraction (Blocking I/O, run in thread if needed, but simple for now)
        print(f"Extracting TOC from {filepath}...")
        toc_data = extract_toc(filepath)
        
        # Convert dicts to TOCItems
        toc_items = [
            TOCItem(title=item['title'], page=item['page']) 
            for item in toc_data
        ]
        
        # 2. Encoding
        print(f"Encoding {len(toc_items)} items...")
        encoded_items = await self.encode_items(toc_items, book_hash)
        
        result = EncodingResult(source_file=filepath, items=encoded_items)
        return result

    async def encode_items(self, items: List[TOCItem], book_hash: str) -> List[EncodedItem]:
        """Encodes a list of TOC items concurrently."""
        tasks = [self.encode_single_item(item, idx, book_hash) for idx, item in enumerate(items)]
        return await asyncio.gather(*tasks)

    async def encode_single_item(self, item: TOCItem, index: int, book_hash: str) -> EncodedItem:
        """Encodes a single TOC item with mnemonic data, verifying against DB first."""
        
        # Check DB
        existing = self.db.get_encoding(book_hash, index)
        if existing:
            # (locus, actor, imagery, scent_pos, scent_neg)
            return EncodedItem(
                toc_item=item,
                locus=existing[0],
                actor=existing[1],
                imagery=existing[2],
                scent_positive=existing[3],
                scent_negative=existing[4]
            )

        # Generate new if not in DB
        locus = LociEngine.get_locus(item.page)
        actor = ActorEngine.get_actor(item.title)
        imagery = AbsurdImageryEngine.get_imagery(item.title)
        scent_pos, scent_neg = ProustScentEngine.get_scent_pair(item.title)
        
        encoded = EncodedItem(
            toc_item=item,
            locus=locus,
            actor=actor,
            imagery=imagery,
            scent_positive=scent_pos,
            scent_negative=scent_neg
        )
        
        # Save to DB
        self.db.save_encoding(book_hash, index, encoded)
        
        return encoded
