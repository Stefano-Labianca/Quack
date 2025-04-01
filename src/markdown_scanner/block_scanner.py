from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6


HEADING_REGEX = r"^(#{1,6})\s+(.+)$"
CODE_REGEX = r"^```(?:\s*(\w+))?([\s\S]*?)^```$"
QUOTE_REGEX = r"^>\s*(.+)$"
UNOREDERE_REGEX = r"^\s*[-+*]\s+(.+)$"
ORDERED_REGEX = r"^\s*\d+\.\s+(.+)$"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: len(block) > 0, blocks))

    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH