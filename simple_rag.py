"""
Simple RAG - A minimal working example
This is a simplified version to get you started quickly
"""

import os
from pathlib import Path

# Simple in-memory storage (no database needed for starting)
class SimpleRAG:
    def __init__(self):
        self.documents = {}  # Store documents in memory
        self.doc_folder = Path("documents")
        self.doc_folder.mkdir(exist_ok=True)
        print("Simple RAG initialized!")
        print(f"Put your documents in: {self.doc_folder.absolute()}")
    
    def load_text_file(self, filepath):
        """Load a single text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def load_all_documents(self):
        """Load all text files from documents folder"""
        print("\nLoading documents...")
        
        # Find all text files
        text_files = list(self.doc_folder.glob("*.txt"))
        text_files.extend(self.doc_folder.glob("*.md"))
        
        if not text_files:
            print("No text files found. Add some .txt or .md files to 'documents' folder")
            return
        
        # Load each file
        for filepath in text_files:
            content = self.load_text_file(filepath)
            if content:
                self.documents[filepath.name] = content
                print(f"  Loaded: {filepath.name} ({len(content)} characters)")
        
        print(f"Total documents loaded: {len(self.documents)}")
    
    def search(self, query):
        """Simple keyword search in documents"""
        if not self.documents:
            return "No documents loaded. Please load documents first."
        
        results = []
        query_lower = query.lower()
        
        # Search each document
        for doc_name, content in self.documents.items():
            # Find sentences containing the query
            sentences = content.split('.')
            matching_sentences = []
            
            for sentence in sentences:
                if query_lower in sentence.lower():
                    matching_sentences.append(sentence.strip())
            
            if matching_sentences:
                results.append({
                    'document': doc_name,
                    'matches': matching_sentences[:3]  # First 3 matches
                })
        
        return results
    
    def ask(self, question):
        """Answer a question based on documents"""
        print(f"\nQuestion: {question}")
        
        # Search for relevant content
        results = self.search(question)
        
        if not results:
            return "I couldn't find information about that in the documents."
        
        # Format the answer
        answer = "Based on the documents:\n\n"
        for result in results:
            answer += f"From '{result['document']}':\n"
            for match in result['matches']:
                answer += f"  • {match}\n"
            answer += "\n"
        
        return answer
    
    def list_documents(self):
        """Show loaded documents"""
        if not self.documents:
            print("No documents loaded")
            return
        
        print("\nLoaded documents:")
        for i, doc_name in enumerate(self.documents.keys(), 1):
            doc_size = len(self.documents[doc_name])
            print(f"  {i}. {doc_name} ({doc_size} characters)")
    
    def add_document_from_text(self, title, content):
        """Add a document directly from text"""
        self.documents[title] = content
        print(f"Added document: {title}")

def main():
    """Interactive mode"""
    print("""
╔════════════════════════════════════╗
║     Simple RAG System              ║
║     No API Key Required!           ║
╚════════════════════════════════════╝
    """)
    
    rag = SimpleRAG()
    
    # Add sample document if no documents exist
    if not list(rag.doc_folder.glob("*")):
        print("\nCreating sample document...")
        sample_content = """
RAG stands for Retrieval-Augmented Generation.
It is a technique that combines information retrieval with text generation.
RAG systems can answer questions by finding relevant information first.
The main components are: document storage, retrieval, and generation.
RAG is useful for building chatbots that can answer questions about specific documents.
Python is a great language for building RAG systems.
LangChain is a popular framework for RAG.
Vector databases store document embeddings for similarity search.
        """
        sample_path = rag.doc_folder / "sample_rag_info.txt"
        with open(sample_path, 'w') as f:
            f.write(sample_content)
        print(f"Created sample document: {sample_path}")
    
    # Load documents
    rag.load_all_documents()
    
    # Interactive loop
    while True:
        print("\n" + "="*40)
        print("Commands:")
        print("  1. Ask a question")
        print("  2. Search for keyword")
        print("  3. List documents")
        print("  4. Reload documents")
        print("  5. Add text directly")
        print("  0. Exit")
        print("-"*40)
        
        choice = input("Choose (0-5): ").strip()
        
        if choice == "1":
            question = input("\nAsk your question: ").strip()
            if question:
                answer = rag.ask(question)
                print("\n" + answer)
        
        elif choice == "2":
            keyword = input("\nEnter keyword to search: ").strip()
            if keyword:
                results = rag.search(keyword)
                if results:
                    print(f"\nFound in {len(results)} document(s)")
                    for r in results:
                        print(f"\n{r['document']}:")
                        for match in r['matches']:
                            print(f"  - {match}")
                else:
                    print("No matches found")
        
        elif choice == "3":
            rag.list_documents()
        
        elif choice == "4":
            rag.documents = {}
            rag.load_all_documents()
        
        elif choice == "5":
            title = input("\nDocument title: ").strip()
            print("Enter content (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            content = "\n".join(lines)
            rag.add_document_from_text(title, content)
        
        elif choice == "0":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()