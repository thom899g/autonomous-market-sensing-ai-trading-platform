"""
Firebase Client for Sensorium - Primary state management and real-time streaming.
Implements the Firebase-first architectural constraint.
"""
import firebase_admin
from firebase_admin import credentials, firestore, db
from typing import Optional, Dict, Any, List
import logging
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FirebaseMode(Enum):
    """Firebase database modes"""
    FIRESTORE = "firestore"
    REALTIME_DB = "realtime_db"
    BOTH = "both"


@dataclass
class FirebaseConfig:
    """Firebase configuration dataclass"""
    project_id: str
    credentials_path: str = "firebase_credentials.json"
    mode: FirebaseMode = FirebaseMode.BOTH
    realtime_db_url: Optional[str] = None
    collections: Dict[str, str] = None  # Collection names mapping
    
    def __post_init__(self):
        if self.collections is None:
            self.collections = {
                "tick_data": "tick_layer",
                "orderbook": "orderbook_layer", 
                "ohlcv": "ohlcv_layer",
                "fundamentals": "fundamental_layer",
                "macroeconomics": "macro_layer",
                "sensorium_state": "sensorium_state"
            }


class FirebaseClient:
    """
    Robust Firebase client for Sensorium with dual database support.
    Handles Firestore (for structured data) and Realtime Database (for streaming).
    """
    
    def __init__(self, config: FirebaseConfig):
        """
        Initialize Firebase client with configuration.
        
        Args:
            config: FirebaseConfig object with project settings
            
        Raises:
            FileNotFoundError: If credentials file doesn't exist
            ValueError: If Firebase initialization fails
        """
        self.config = config
        self._firestore_client: Optional[firestore.Client] = None
        self._realtime_db = None
        self._initialized = False
        self._lock = threading.RLock()
        
        # Verify credentials file exists
        if not os.path.exists(config.credentials_path):
            logger.error(f"Firebase credentials file not found: {config.credentials_path}")
            raise FileNotFoundError(f"Credentials file not found: {config.credentials_path}")
        
        self._initialize_firebase()