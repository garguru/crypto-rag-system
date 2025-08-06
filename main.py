"""
RAG Project - Chat with Your Documents
A Retrieval-Augmented Generation system that lets you ask questions about your files
Author: mgarr
Started: 2025-01-06
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Project configuration
PROJECT_NAME = "Personal RAG System"
PROJECT_VERSION = "0.1.0"
PROJECT_DIR = Path(__file__).parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"
VECTOR_DB_DIR = PROJECT_DIR / "vector_db"
CACHE_DIR = PROJECT_DIR / "cache"

# Create necessary directories
for directory in [DOCUMENTS_DIR, VECTOR_DB_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

class RAGSystem:
    """Main RAG system for document Q&A"""
    
    def __init__(self):
        self.project_name = PROJECT_NAME
        self.version = PROJECT_VERSION
        print(f">>> Initializing {self.project_name} v{self.version}")
        print(f">>> Documents folder: {DOCUMENTS_DIR}")
        self.vector_store = None
        self.llm = None
        
    def load_documents(self):
        """Load documents from the documents folder"""
        print("\n[LOAD] Loading documents...")
        
        # Check what's in the documents folder
        docs = list(DOCUMENTS_DIR.glob("*"))
        if not docs:
            print("   No documents found. Add files to:", DOCUMENTS_DIR)
            return False
        
        print(f"   Found {len(docs)} files:")
        for doc in docs[:5]:  # Show first 5
            print(f"   - {doc.name}")
        
        # TODO: Implement actual document loading
        print("   [TODO] Document loading will be implemented next")
        return True
    
    def create_embeddings(self):
        """Create embeddings for all documents"""
        print("\n[EMBED] Creating embeddings...")
        # TODO: Implement embedding creation
        print("   [TODO] Embedding creation will be implemented")
        
    def setup_vector_store(self):
        """Initialize vector database"""
        print("\n[VECTOR] Setting up vector store...")
        # TODO: Setup ChromaDB or similar
        print("   [TODO] Vector store setup will be implemented")
        
    def ask_question(self, question):
        """Ask a question about the documents"""
        print(f"\n[QUERY] Question: {question}")
        
        if not self.vector_store:
            print("   [ERROR] Vector store not initialized. Load documents first.")
            return None
        
        # TODO: Implement RAG query
        print("   [TODO] RAG query will be implemented")
        return "Answer will appear here once implemented"
    
    def add_document(self, filepath):
        """Add a new document to the system"""
        print(f"\n[ADD] Adding document: {filepath}")
        # TODO: Implement document addition
        print("   [TODO] Document addition will be implemented")
    
    def list_documents(self):
        """List all indexed documents"""
        print("\n[LIST] Indexed documents:")
        docs = list(DOCUMENTS_DIR.glob("*"))
        if not docs:
            print("   No documents indexed yet")
        else:
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc.name}")
        return docs
    
    def clear_database(self):
        """Clear the vector database"""
        print("\n[CLEAR] Clearing vector database...")
        # TODO: Implement database clearing
        print("   [TODO] Database clearing will be implemented")

def print_menu():
    """Display menu options"""
    print("\n" + "="*50)
    print("RAG SYSTEM - Chat with Your Documents")
    print("="*50)
    print("1. Load documents")
    print("2. Ask a question")
    print("3. Add new document")
    print("4. List documents")
    print("5. Setup vector store")
    print("6. Clear database")
    print("0. Exit")
    print("-"*50)

def main():
    """Main entry point"""
    print("""
========================================
   RAG System - Chat with Your Docs
   Learn by Building
========================================
    """)
    
    # Create RAG system instance
    rag = RAGSystem()
    
    # Main loop
    while True:
        print_menu()
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == "1":
            rag.load_documents()
        elif choice == "2":
            question = input("\nEnter your question: ").strip()
            if question:
                answer = rag.ask_question(question)
                if answer:
                    print(f"\n[ANSWER] {answer}")
        elif choice == "3":
            filepath = input("\nEnter document path: ").strip()
            if filepath:
                rag.add_document(filepath)
        elif choice == "4":
            rag.list_documents()
        elif choice == "5":
            rag.setup_vector_store()
        elif choice == "6":
            confirm = input("\nAre you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                rag.clear_database()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()