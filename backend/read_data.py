import json
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import re

def read_json_file(filename="studocu_data.json"):
    """Read data from a JSON file."""
    try:
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            print(f"Current directory: {os.getcwd()}")
            print(f"Files in current directory: {os.listdir('.')}")
            return None
            
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyDTvXzkJgncNVU8g8rMBy_6dg0BUy95feg")

def format_superscripts(text):
    """Convert text with caret notation (x^y) to proper markdown superscripts."""
    # Pattern to find superscript notation like 5^3
    pattern = r'(\d+)\^(\d+)'
    
    # Replace with markdown superscript format
    return re.sub(pattern, r'\1<sup>\2</sup>', text)

def simplify_latex(text):
    """Convert LaTeX expressions to more readable plain text."""
    # Handle common LaTeX commands with unicode replacements
    common_patterns = [
        # Fractions
        (r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1)/(\2)'),
        
        # Common operators
        (r'\\cdot', r'·'),
        (r'\\times', r'×'),
        (r'\\div', r'÷'),
        (r'\\pm', r'±'),
        
        # Comparison operators
        (r'\\neq', r'≠'),
        (r'\\leq', r'≤'),
        (r'\\geq', r'≥'),
        (r'\\approx', r'≈'),
        
        # Greek letters
        (r'\\alpha', r'α'),
        (r'\\beta', r'β'),
        (r'\\gamma', r'γ'),
        (r'\\delta', r'δ'),
        (r'\\epsilon', r'ε'),
        (r'\\zeta', r'ζ'),
        (r'\\eta', r'η'),
        (r'\\theta', r'θ'),
        (r'\\iota', r'ι'),
        (r'\\kappa', r'κ'),
        (r'\\lambda', r'λ'),
        (r'\\mu', r'μ'),
        (r'\\nu', r'ν'),
        (r'\\xi', r'ξ'),
        (r'\\pi', r'π'),
        (r'\\rho', r'ρ'),
        (r'\\sigma', r'σ'),
        (r'\\tau', r'τ'),
        (r'\\upsilon', r'υ'),
        (r'\\phi', r'φ'),
        (r'\\chi', r'χ'),
        (r'\\psi', r'ψ'),
        (r'\\omega', r'ω'),
        
        # Capital Greek letters
        (r'\\Gamma', r'Γ'),
        (r'\\Delta', r'Δ'),
        (r'\\Theta', r'Θ'),
        (r'\\Lambda', r'Λ'),
        (r'\\Xi', r'Ξ'),
        (r'\\Pi', r'Π'),
        (r'\\Sigma', r'Σ'),
        (r'\\Phi', r'Φ'),
        (r'\\Psi', r'Ψ'),
        (r'\\Omega', r'Ω'),
        
        # Other symbols
        (r'\\infty', r'∞'),
        (r'\\nabla', r'∇'),
        (r'\\partial', r'∂'),
        (r'\\sum', r'∑'),
        (r'\\prod', r'∏'),
        (r'\\int', r'∫'),
        
        # Subscripts and superscripts
        (r'_{(.*?)}', r'_\1'),
        (r'\^{(.*?)}', r'^\1'),
        
        # Square roots
        (r'\\sqrt\{(.*?)\}', r'√(\1)'),
        
        # Remove LaTeX delimiters
        (r'\$\$(.*?)\$\$', r'\n\1\n'),
        (r'\$(.*?)\$', r'\1'),
        (r'\\\[(.*?)\\\]', r'\n\1\n'),
        (r'\\begin\{equation\}(.*?)\\end\{equation\}', r'\n\1\n')
    ]
    
    # Apply all replacements
    for pattern, replacement in common_patterns:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
    
    return text

def askQuestion(context, question, existingConversation):
    systemContext = """
    You are an AI expert explaining concepts to a uni student who wants to get full marks on their exam. 
    You are provided with expert notes as context, you should go through these to get context for your answers.
    
    Your answers should be informative but try to convey the information as concisely as possible while still ensuring the student gets the important information.
    
    Use markdown formatting for your answers:
    - Use **bold** for important terms
    - Use *italics* for emphasis
    - Use `code blocks` for code
    - Use bullet points and numbered lists where appropriate
    
    For mathematical expressions:
    - For simple expressions, use plain text with proper symbols (×, ÷, ≤, ≥, etc.)
    - For fractions, use (numerator)/(denominator) format
    - For exponents, use ^ notation (e.g., x^2)
    - For complex formulas, use a clear, readable format with proper spacing
    
    Keep your explanations clear, accurate, and focused on helping the student understand the concepts thoroughly.
    """

    # Format the conversation history
    conversation_history = ""
    if existingConversation:
        conversation_history = "Previous conversation:\n"
        for i, exchange in enumerate(existingConversation):
            conversation_history += f"Question {i+1}: {exchange['question']}\n"
            conversation_history += f"Answer {i+1}: {exchange['answer']}\n\n"

    contents = f"{systemContext}\n\n{context}\n\n{conversation_history}\nQuestion:{question}"

    response = genai.generate_content(
        model="gemini-2.0-flash",
        contents=contents
    )
    
    return response.text

def main():
    # Read the data from the JSON file
    data = read_json_file()
    
    # Initialize conversation history and Rich console
    conversation_history = []
    console = Console()
    
    console.print(Panel("[bold green]Study Assistant[/bold green]", subtitle="Ask questions about your notes. Type 'exit' to quit."))
    
    while True:
        query = input("[bold cyan]What is your question?[/bold cyan] ")
        
        if query.lower() == 'exit':
            console.print("[bold green]Goodbye! Happy studying![/bold green]")
            break
            
        # Get answer using conversation history as context
        answer = askQuestion(data, query, conversation_history)
        
        # Process the answer to handle formatting
        processed_answer = format_superscripts(answer)
        processed_answer = simplify_latex(processed_answer)
        
        # Display the answer with rich formatting
        console.print("\n[bold blue]Answer:[/bold blue]")
        
        try:
            # Try to render as markdown
            console.print(Markdown(processed_answer))
        except Exception as e:
            # Fallback to plain text if markdown rendering fails
            console.print(processed_answer)
            console.print(f"[dim](Rendering error: {str(e)})[/dim]")
            
        console.print("\n" + "-"*50 + "\n")
        
        # Add this exchange to conversation history
        conversation_history.append({
            "question": query,
            "answer": answer  # Store the original answer
        })
        
        # Optionally limit history length to prevent context window issues
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]

if __name__ == "__main__":
    main() 