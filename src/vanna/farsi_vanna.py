#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from typing import Optional, Dict, Any

# Add the parent directory to the path to import vanna modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from vanna.base import VannaBase
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.ollama.ollama_chat import Ollama_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.pgvector.pgvector import PG_VectorStore

logger = logging.getLogger(__name__)

class FarsiVanna(VannaBase):
    """
    FarsiVanna class that supports both OpenAI and Ollama for chat,
    and both ChromaDB and PostgreSQL for vector storage.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize FarsiVanna with the specified configuration.
        
        Args:
            config: Configuration dictionary containing:
                - AI provider settings (openai/ollama)
                - Vector database settings (chromadb/pgvector)
                - Database connection settings
        """
        super().__init__(config=config)
        
        # Initialize AI provider
        self._init_ai_provider(config)
        
        # Initialize vector store
        self._init_vector_store(config)
        
        # Initialize Farsi prompts
        self.farsi_prompts = {
            "system": """شما یک دستیار هوشمند برای تولید کوئری SQL هستید. 
            لطفاً سوالات فارسی را به SQL تبدیل کنید.
            همیشه از بهترین شیوه‌های SQL استفاده کنید و نتایج را به فارسی توضیح دهید.""",
            
            "question_to_sql": """سوال کاربر: {question}
            
            لطفاً این سوال را به کوئری SQL تبدیل کنید. 
            فقط کوئری SQL را برگردانید، بدون توضیح اضافی.""",
            
            "explain_results": """نتایج کوئری SQL:
            {sql}
            
            داده‌های نتیجه:
            {data}
            
            لطفاً این نتایج را به فارسی توضیح دهید."""
        }
    
    def _init_ai_provider(self, config: Optional[Dict[str, Any]]):
        """Initialize the AI provider (OpenAI or Ollama)"""
        if not config:
            config = {}
        
        ai_provider = config.get('ai_provider', 'ollama')
        
        if ai_provider == 'openai':
            # Initialize OpenAI
            openai_config = {
                'api_key': config.get('api_key'),
                'model': config.get('model', 'gpt-3.5-turbo'),
                'temperature': config.get('temperature', 0.7)
            }
            self.ai_provider = OpenAI_Chat(config=openai_config)
            logger.info("Initialized OpenAI AI provider")
        else:
            # Initialize Ollama
            ollama_config = {
                'ollama_base_url': config.get('ollama_base_url', 'http://localhost:11434'),
                'model': config.get('model', 'llama2')
            }
            self.ai_provider = Ollama_Chat(config=ollama_config)
            logger.info("Initialized Ollama AI provider")
    
    def _init_vector_store(self, config: Optional[Dict[str, Any]]):
        """Initialize the vector store (ChromaDB or PostgreSQL)"""
        if not config:
            config = {}
        
        vector_db_type = config.get('vector_db_type', 'chromadb')
        
        if vector_db_type == 'pgvector':
            # Initialize PostgreSQL vector store
            pg_config = {
                'connection_string': config.get('connection_string')
            }
            self.vector_store = PG_VectorStore(config=pg_config)
            logger.info("Initialized PostgreSQL vector store")
        else:
            # Initialize ChromaDB vector store
            chroma_config = {
                'chroma_db_impl': config.get('chroma_db_impl', 'duckdb+parquet'),
                'persist_directory': config.get('persist_directory', './chroma_db')
            }
            self.vector_store = ChromaDB_VectorStore(config=chroma_config)
            logger.info("Initialized ChromaDB vector store")
    
    def generate_sql(self, question: str) -> str:
        """Generate SQL from a Farsi question"""
        try:
            # Use the AI provider to generate SQL
            prompt = self.farsi_prompts["question_to_sql"].format(question=question)
            
            # Create a simple prompt structure for the AI provider
            messages = [
                self.ai_provider.system_message(self.farsi_prompts["system"]),
                self.ai_provider.user_message(prompt)
            ]
            
            sql = self.ai_provider.submit_prompt(messages)
            
            # Clean up the SQL response
            if sql:
                sql = sql.strip()
                # Remove any markdown formatting
                if sql.startswith('```sql'):
                    sql = sql[6:]
                if sql.endswith('```'):
                    sql = sql[:-3]
                sql = sql.strip()
            
            return sql
            
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return None
    
    def train(self, question: str = None, sql: str = None, ddl: str = None, 
              documentation: str = None, **kwargs):
        """Train the model with new data"""
        try:
            self.vector_store.train(
                question=question,
                sql=sql,
                ddl=ddl,
                documentation=documentation,
                **kwargs
            )
            logger.info("Training completed successfully")
        except Exception as e:
            logger.error(f"Error during training: {e}")
            raise
    
    def get_similar_question_sql(self, question: str) -> list:
        """Get similar question-SQL pairs"""
        try:
            return self.vector_store.get_similar_question_sql(question)
        except Exception as e:
            logger.error(f"Error getting similar questions: {e}")
            return []
    
    def get_related_documentation(self, question: str, **kwargs) -> list:
        """Get related documentation"""
        try:
            return self.vector_store.get_related_documentation(question, **kwargs)
        except Exception as e:
            logger.error(f"Error getting related documentation: {e}")
            return []
    
    def get_training_data(self, **kwargs):
        """Get training data"""
        try:
            return self.vector_store.get_training_data(**kwargs)
        except Exception as e:
            logger.error(f"Error getting training data: {e}")
            return None
    
    def remove_training_data(self, id: str, **kwargs) -> bool:
        """Remove training data by ID"""
        try:
            return self.vector_store.remove_training_data(id, **kwargs)
        except Exception as e:
            logger.error(f"Error removing training data: {e}")
            return False
    
    def explain_results(self, sql: str, data: list) -> str:
        """Explain SQL results in Farsi"""
        try:
            prompt = self.farsi_prompts["explain_results"].format(
                sql=sql,
                data=str(data)
            )
            
            messages = [
                self.ai_provider.system_message(self.farsi_prompts["system"]),
                self.ai_provider.user_message(prompt)
            ]
            
            explanation = self.ai_provider.submit_prompt(messages)
            return explanation.strip()
            
        except Exception as e:
            logger.error(f"Error explaining results: {e}")
            return "خطا در توضیح نتایج"