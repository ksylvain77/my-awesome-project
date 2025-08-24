"""
Darth Vader Threat Generator - Core Module
Core business logic for Imperial threats

This module contains the core business logic for the Darth Vader threat generator.
"""

import random
from datetime import datetime
from typing import Dict, Any, List

# Imperial Threat Pool
VADER_THREATS = [
    "I find your lack of faith disturbing.",
    "You underestimate the power of the Dark Side.",
    "Your defiance will be your downfall.",
    "The Emperor is not as forgiving as I am.",
    "You have failed me for the last time.",
    "Resistance is futile. You will join us or die.",
    "Your rebel friends will share your fate.",
    "The dark side is stronger. Much stronger.",
    "You are beaten. It is useless to resist.",
    "Your destiny lies with me, young one.",
    "The circle is now complete.",
    "You will learn the true meaning of suffering.",
    "Your weakness betrays you. Your faith in your friends is yours!",
    "The Force is strong with you, but you are not a Jedi yet.",
    "Perhaps you refer to the imminent attack of your rebel fleet?"
]

def get_random_threat() -> Dict[str, Any]:
    """
    Get a random Darth Vader threat
    
    Returns:
        Dict containing threat data and metadata
    """
    threat = random.choice(VADER_THREATS)
    return {
        "threat": threat,
        "source": "Darth Vader",
        "empire": "Galactic Empire",
        "threat_level": "Imperial",
        "timestamp": datetime.now().isoformat()
    }

def get_threat_count() -> int:
    """
    Get total number of available threats
    
    Returns:
        Number of threats in the pool
    """
    return len(VADER_THREATS)

def process_data(data: Any) -> Dict[str, Any]:
    """
    Process incoming data (template function)
    
    Args:
        data: Input data to process
        
    Returns:
        Dict containing processed results
    """
    return {
        "processed": True,
        "input_type": type(data).__name__,
        "timestamp": datetime.now().isoformat(),
        "result": f"Processed: {data}"
    }

def validate_input(data: Any) -> bool:
    """
    Validate input data (template function)
    
    Args:
        data: Data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if data is None:
        return False
    if isinstance(data, str) and len(data.strip()) == 0:
        return False
    return True
