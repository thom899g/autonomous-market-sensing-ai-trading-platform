"""
Sensorium Module: The reality-constructing data ingestion layer
of the Autonomous Market-Sensing AI Trading Platform.
Implements the digital mycelium metaphor with Firebase-first event streaming.
"""
from .firebase_client import FirebaseClient
from .reality_layers import RealityLayers, TemporalLayer
from .data_ingestors import CryptoIngestor, StockIngestor, ForexIngestor
from .sensorium_orchestrator import SensoriumOrchestrator

__all__ = [
    'FirebaseClient',
    'RealityLayers',
    'TemporalLayer',
    'CryptoIngestor',
    'StockIngestor',
    'ForexIngestor',
    'SensoriumOrchestrator'
]