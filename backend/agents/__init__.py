"""
Healthcare Intelligence Platform - Agents Package
Multi-agent framework for clinical analytics
"""

from .orchestrator import AgentOrchestrator
from .base_agent import BaseAgent

__all__ = ["AgentOrchestrator", "BaseAgent"]
