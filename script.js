let expression = "";
const display = document.getElementById("display");

function updateDisplay() {
    let displayText = expression || "0";
    
    // Scale font size down if expression is long, similar to python implementation
    if (displayText.length > 12) {
        display.style.fontSize = "30px";
    } else {
        display.style.fontSize = "48px";
    }
    
    display.textContent = displayText;
}

function addToExpression(val) {
    if (expression === "Error") {
        expression = "";
    }
    
    // Ensure standard visual representations match mathematical operations
    expression += val;
    updateDisplay();
}

function clearExpression() {
    expression = "";
    updateDisplay();
}

function backspaceExpression() {
    if (expression === "Error") {
        expression = "";
    } else {
        expression = expression.slice(0, -1);
    }
    updateDisplay();
}

function evaluateExpression() {
    if (!expression) return;
    
    try {
        // Map operators and mathematical symbols to JavaScript counterparts
        let parseExpr = expression;
        
        // Exponents
        parseExpr = parseExpr.replace(/\^/g, "**");
        
        // Constants
        parseExpr = parseExpr.replace(/π/g, "Math.PI");
        parseExpr = parseExpr.replace(/e/g, "Math.E");
        
        // Functions (with regex to handle JS Math functions)
        parseExpr = parseExpr.replace(/sin\(/g, "Math.sin(");
        parseExpr = parseExpr.replace(/cos\(/g, "Math.cos(");
        parseExpr = parseExpr.replace(/tan\(/g, "Math.tan(");
        parseExpr = parseExpr.replace(/log\(/g, "Math.log(");
        parseExpr = parseExpr.replace(/sqrt\(/g, "Math.sqrt(");
        
        // Evaluate the mathematical expression safely
        // Using Function constructor instead of direct eval is slightly cleaner/safer
        const result = new Function(`return (${parseExpr})`)();
        
        if (result === undefined || isNaN(result) || !isFinite(result)) {
            throw new Error("Invalid output");
        }
        
        // Format decimal outputs nicely, matching Python: round(float(result), 8).rstrip('0').rstrip('.')
        let formattedResult = String(result);
        if (formattedResult.includes(".")) {
            // Round to 8 decimal places
            formattedResult = Number(result).toFixed(8);
            // Remove trailing zeros and trailing dot
            formattedResult = parseFloat(formattedResult).toString();
        }
        
        expression = formattedResult;
        updateDisplay();
    } catch (error) {
        expression = "Error";
        updateDisplay();
    }
}

// Keyboard support
document.addEventListener("keydown", function(event) {
    const key = event.key;
    
    // Numbers, simple operators, parentheses, and dot
    if (/^[0-9+\-*/.()]$/.test(key)) {
        event.preventDefault();
        addToExpression(key);
    } 
    // Return or Enter for Equals
    else if (key === "Enter") {
        event.preventDefault();
        evaluateExpression();
    } 
    // Backspace for deletion
    else if (key === "Backspace") {
        event.preventDefault();
        backspaceExpression();
    } 
    // Escape for All Clear (AC)
    else if (key === "Escape") {
        event.preventDefault();
        clearExpression();
    }
});
